#!/bin/bash
## DO NOT RUN THIS FILE MANUALLY

## <Edit this values>
FULL_NAME="Ibrahim Rafi"
EMAIL="rafiibrahim8@hotmail.com"
KEY="88BCCC030B08626C"
PRIORITY_MIRROR_LOC="sg"
REPO_NAME="private-arch-repo"
## </Edit this values>

echo -e "nameserver 8.8.8.8\nnameserver 1.1.1.1" > /etc/resolv.conf

mirrorlist=$(curl -Ls 'https://archlinux.org/mirrorlist/?country=all&protocol=http&ip_version=4&use_mirror_status=on')
mirrorlist=$(echo "$mirrorlist" | sed '/^## Bangladesh/,+1d' | sed '/#Server/s/^#//g')
priority=$(echo -e '##\n## Priority Mirrors\n##\n\n## Bangladesh\nServer = http://mirror.xeonbd.com/archlinux/$repo/os/$arch')
echo -e "$priority\n\n$mirrorlist" > /etc/pacman.d/mirrorlist

pacman -Sy --noconfirm --needed sudo base-devel git python-pip

curl -L -o /usr/bin/build-aur-pkg https://github.com/rafiibrahim8/private-arch-repo/raw/main/internal-scripts/build-aur-pkg.sh
chmod +x /usr/bin/build-aur-pkg

curl -L -o /usr/bin/build-non-aur-pkg https://github.com/rafiibrahim8/private-arch-repo/raw/main/internal-scripts/build-non-aur-pkg.sh
chmod +x /usr/bin/build-non-aur-pkg

curl -L -o /usr/bin/gen_mirrorlist.py https://gist.githubusercontent.com/rafiibrahim8/b27cc3970810c39b673db3b94df05768/raw/31506642f3fdd194fe441e8b821029ec75fe29e3/gen_mirrorlist.py
chmod +x /usr/bin/gen_mirrorlist.py

echo "$PRIORITY_MIRROR_LOC" > /etc/private-arch-repo-priority-mirror.name
echo "$REPO_NAME" > /etc/private-arch-repo.name
echo "PACKAGER=\"$FULL_NAME <$EMAIL>\"" >> /etc/makepkg.conf
echo "GPGKEY=\"$KEY\"" >> /etc/makepkg.conf

gen_mirrorlist.py "$(cat /etc/private-arch-repo-priority-mirror.name 2>/dev/null)"

echo 'builder ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/builder
useradd -m -s /bin/bash builder
