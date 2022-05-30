#!/bin/bash

cd ~
git clone "https://aur.archlinux.org/$1.git"
cd "$1"
sudo pacman -Sy
makepkg --syncdeps --sign --clean --needed --noconfirm
repoctl update

cd ~
rm -rf "$1"
