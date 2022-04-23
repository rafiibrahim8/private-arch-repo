from traceback import format_exc
import requests
import asyncio
import json
import os

from read_repo_db import ReadRepoDB
from discord_debug import DebugDiscord

class BuildQueue:
    def __init__(self, dest_dir='output', debug_discord=None):
        dest = os.path.normpath(os.path.join(os.getcwd(), dest_dir))
        self.__debug_discord = debug_discord
        self.__common_command = f'docker run -u builder --rm -v {dest}:/output arch-pkgbuild'
        self.__queue = asyncio.Queue()
    
    def put(self, command):
        self.__queue.put_nowait(f'{self.__common_command} {command}')
    
    def __run_impl(self, command):
        success = os.system(command) == 0
        if not success and self.__debug_discord:
            self.__debug_discord.error(f'Command failed with: {command}')
        
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
    def __init__(self, build_queue, repo_dir='output', repo_name='private-arch-repo', list_json='aur_packages.json', interval=3600, debug_discord=None):
        self._wait_time = interval
        self.__debug_discord = debug_discord
        self.__repo_dir = repo_dir
        self.__repo_name = repo_name
        self.__build_queue = build_queue
        with open(list_json, 'r') as f:
            self.__packages = json.load(f)
    
    def _run_impl(self):
        try:
            self.__run_implx()
        except KeyboardInterrupt:
            raise
        except:
            self.__debug_discord and self.__debug_discord.error(f'Running error occoured. Reason: {format_exc()}')

    def __run_implx(self):
        if not self.__packages:
            return
        
        url = 'https://aur.archlinux.org/rpc/?v=5&type=info'
        for i in self.__packages:
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
    def __init__(self, build_queue, repo_dir='output', repo_name='private-arch-repo', interval=3600, debug_discord=None):
        self._wait_time = interval
        self.__build_queue = build_queue
        self.__repo_dir = repo_dir
        self.__repo_name = repo_name
        self.__debug_discord = debug_discord
        self.__non_aur_dir = 'non-aur-packages'

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
                self.__debug_discord and self.__debug_discord.error(f'Running error occoured. Reason: {format_exc()}')

class Checker:
    def __init__(self, repo_dir='output', repo_name='private-arch-repo', aur_list_json='aur_packages.json', interval=3600, debug_discord_url=None):
        debug_discord = DebugDiscord(debug_discord_url) if debug_discord_url else None
        self.__buid_queue = BuildQueue(repo_dir, debug_discord)
        self.__check_aur = CheckAUR(self.__buid_queue, repo_dir, repo_name, aur_list_json, interval, debug_discord)
        self.__check_non_aur = CheckNonAUR(self.__buid_queue, repo_dir, repo_name, interval, debug_discord)

        os.makedirs(repo_dir, exist_ok=True)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.__buid_queue.run())
        loop.create_task(self.__check_aur.run())
        loop.create_task(self.__check_non_aur.run())
        loop.run_forever()
