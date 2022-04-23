#!/usr/bin/python
import os
import re
import glob
import json

with open('config.json','r') as f:
    config = json.load(f)

url = config['repo_url']
db_name = config['repo_name'] + '.db.tar.gz'

system_cmd = [
    f'curl -L -o /tmp/{db_name} {url}/{db_name}',
    f'tar --directory=/tmp -xf  /tmp/{db_name}',
    'gpg --receive-keys 7568D9BB55FF9E5287D586017AE645C0CF8E292A',
    'touch install.sh'
]

for i in system_cmd:
    r = os.system(i)
    if r:
        exit(1)

db_file = list(glob.glob('/tmp/pritunl-client-electron-*/desc'))[0]

with open(db_file, 'r') as f:
    db = f.read()

file_name = re.findall(r'%FILENAME%\n([^\n]+)', db)[0]

sha256sum = re.findall(r'%SHA256SUM%\n([^\n]+)', db)[0]

depends = re.findall(r'%DEPENDS%\n([^%]+)', db)[0]
depends = [f'"{i.strip()}"' for i in depends.split('\n') if i.strip()]
depends = ' '.join(depends)

with open('PKGBUILD.proto', 'r') as f:
    pkgbuild = f.read()

pkgbuild = pkgbuild.replace('###SRC###', f'{url}/{file_name}')
pkgbuild = pkgbuild.replace('###SRC_SIG###', f'{url}/{file_name}.sig')
pkgbuild = pkgbuild.replace('###SHA256SUM###', sha256sum)
pkgbuild = pkgbuild.replace('###DEPENDS###', depends)

with open('PKGBUILD', 'w') as f:
    f.write(pkgbuild)
