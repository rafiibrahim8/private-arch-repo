from traceback import format_exc
import requests
import asyncio
import json
import os

from read_repo_db import ReadRepoDB

class BuildQueue:
    def __init__(self):
        self.__queue = asyncio.Queue()
    
    def put(self, command):
        self.__queue.put_nowait(command)
    
    def __run_impl(self, command):
        success = os.system(command) == 0
        if not success and self.__debug_discord:
            print(f'Command Failed: {command}')
        
    async def run(self):
        while True:
            command = await self.__queue.get()
            self.__run_impl(command)

class CheckerCommon:
    async def run(self):
        while True:
            self._run_impl()
            await asyncio.sleep(self._wait_time)

class CheckAUR(CheckerCommon):
    def __init__(self, build_queue, repo_dir , repo_name, list_json, interval):
        self._wait_time = interval
        self.__repo_dir = repo_dir
        self.__repo_name = repo_name
        self.__build_queue = build_queue
        self.__list_json = list_json
    
    def _run_impl(self):
        try:
            self.__run_implx()
        except KeyboardInterrupt:
            raise
        except:
            print(f'Running error occoured. Reason: {format_exc()}')

    def __run_implx(self):
        with open(self.__list_json, 'r') as f:
            packages = json.load(f)
        if not packages:
            return
        
        url = 'https://aur.archlinux.org/rpc/?v=5&type=info'
        for i in packages:
            url += f'&arg[]={i}'
        aur_db = requests.get(url).json()['results']
        local_db = ReadRepoDB(os.path.join(self.__repo_dir, f'{self.__repo_name}.db.tar.gz')).read()
        for i in aur_db:
            package_name = i['Name']
            local_package = local_db.get(package_name)
            if local_package is None:
                self.__build_queue.put(f'build-aur-pkg {package_name}')
                continue
            if local_package['version'] < i['Version']:
                self.__build_queue.put(f'build-aur-pkg {package_name}')

class CheckNonAUR(CheckerCommon):
    def __init__(self, build_queue, repo_dir, repo_name, non_aur_dir, interval):
        self._wait_time = interval
        self.__build_queue = build_queue
        self.__repo_dir = repo_dir
        self.__repo_name = repo_name
        self.__non_aur_dir = non_aur_dir

    def __check_package(self, name):
        local_db = ReadRepoDB(os.path.join(self.__repo_dir, f'{self.__repo_name}.db.tar.gz')).read()
        if local_db.get(name) is None:
            self.__build_queue.put(f'build-non-aur-pkg {name}')
            return
        
        config = os.path.join(self.__non_aur_dir, name, 'config.json')
        with open(config, 'r') as f:
            config = json.load(f)
        repo_db = f'{config["repo_url"]}/{config["repo_name"]}.db.tar.gz'
        repo_db = ReadRepoDB(repo_db).read()

        if local_db[name]['version'] < repo_db[name]['version']:
            self.__build_queue.put(f'build-non-aur-pkg {name}')

    def _run_impl(self):
        for i in os.listdir(self.__non_aur_dir):
            try:
                self.__check_package(i)
            except KeyboardInterrupt:
                raise
            except:
                print(f'Running error occoured. Reason: {format_exc()}')

class Checker:
    def __init__(self, interval=14400):
        with open('/etc/private-arch-repo/name', 'r') as f:
            repo_name=f.read().strip()
        with open('/etc/private-arch-repo/repo_dir', 'r') as f:
            repo_dir=f.read().strip()
        with open('/etc/private-arch-repo/pkg_list_dir', 'r') as f:
            pkg_list_dir=f.read().strip()
        
        self.__buid_queue = BuildQueue()
        aur_list_json = os.path.join(pkg_list_dir, 'aur_packages.json')
        non_aur_dir = os.path.join(pkg_list_dir, 'non-aur-packages')

        self.__check_aur = CheckAUR(self.__buid_queue, repo_dir, repo_name, aur_list_json, interval)
        self.__check_non_aur = CheckNonAUR(self.__buid_queue, repo_dir, repo_name, non_aur_dir , interval)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.__buid_queue.run())
        loop.create_task(self.__check_aur.run())
        loop.create_task(self.__check_non_aur.run())
        loop.run_forever()
