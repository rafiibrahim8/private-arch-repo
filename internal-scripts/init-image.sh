#!/bin/bash
## DO NOT RUN THIS FILE MANUALLY

## <Edit this values>
FULL_NAME="Ibrahim Rafi"
EMAIL="rafiibrahim8@hotmail.com"
KEY="88BCCC030B08626C"
REPO_NAME="private-arch-repo"
MIRRIRLIST_URL="https://gist.githubusercontent.com/rafiibrahim8/65092ab7bf8d9ebf416d160f002353a0/raw/dfb01c1fc96dadb4a278d8840a2486ba1d75bddc/mirrorlist-v20220530"
## </Edit this values>

REPO_DIR='/var/Repo'
PKG_LIST_DIR='/var/RepoPkgs'

echo -e "nameserver 8.8.8.8\nnameserver 1.1.1.1" > /etc/resolv.conf

curl -L -o /etc/pacman.d/mirrorlist "$MIRRIRLIST_URL"

pacman -Sy --noconfirm --needed sudo base-devel git python-pip

cp internal-scripts/build-aur-pkg.sh /usr/bin/build-aur-pkg
chmod +x /usr/bin/build-aur-pkg

cp internal-scripts/build-non-aur-pkg.sh /usr/bin/build-non-aur-pkg
chmod +x /usr/bin/build-non-aur-pkg

cp internal-scripts/start-builder.sh /usr/bin/start-builder
chmod +x /usr/bin/start-builder

echo "PACKAGER=\"$FULL_NAME <$EMAIL>\"" >> /etc/makepkg.conf
echo "GPGKEY=\"$KEY\"" >> /etc/makepkg.conf

mkdir /etc/private-arch-repo
echo "$REPO_NAME" > /etc/private-arch-repo/name
echo "$REPO_DIR" > /etc/private-arch-repo/repo_dir
echo "$PKG_LIST_DIR" > /etc/private-arch-repo/pkg_list_dir

mkdir -p "$REPO_DIR"
mkdir -p "$PKG_LIST_DIR"

echo 'builder ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/builder
useradd -m -s /bin/bash builder

curl -L -o /etc/pacman.d/mirrorlist "$MIRRIRLIST_URL"
