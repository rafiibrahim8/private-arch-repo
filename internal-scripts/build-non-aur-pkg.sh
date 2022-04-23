#!/bin/bash

cd
git clone "https://github.com/rafiibrahim8/private-arch-repo.git"
cd "private-arch-repo/non-aur-packages/$1"
python configure.py
makepkg --syncdeps --sign --clean --needed --noconfirm
cp *.pkg.tar.zst /output
cp *.pkg.tar.zst.sig /output

cd /output
repo_name=$(cat /etc/private-arch-repo.name 2>/dev/null)
if [[ "$?" == "0" ]]; then
    repo-add -R -n "$repo_name.db.tar.gz" *.zst
else
    repo-add -R -n "private-arch-repo.db.tar.gz" *.zst
fi