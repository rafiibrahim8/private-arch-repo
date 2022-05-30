#!/bin/bash

cd ~
pkg_list_dir=$(cat /etc/private-arch-repo/pkg_list_dir)
cp -r "$pkg_list_dir/non-aur-packages/$1" .
cd "$1"
sudo pacman -Sy
python configure.py
makepkg --syncdeps --sign --clean --needed --noconfirm
repoctl update

cd ~
rm -rf "$1"
