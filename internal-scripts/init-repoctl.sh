#!/bin/bash

cd ~
git clone https://aur.archlinux.org/repoctl.git
cd repoctl
makepkg --syncdeps --needed --noconfirm --noprogressbar
sudo pacman -U --needed --noconfirm repoctl-*.zst

cd ~
rm -rf repoctl

repo_name=$(cat /etc/private-arch-repo/name)
repo_dir=$(cat /etc/private-arch-repo/repo_dir)
repoctl conf new "$repo_dir/$repo_name.db.tar.gz"

echo "PKGDEST=\"$repo_dir\"" | sudo tee -a /etc/makepkg.conf
