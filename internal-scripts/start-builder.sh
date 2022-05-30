#!/bin/bash

cd ~
repo_dir=$(cat /etc/private-arch-repo/repo_dir)
sudo chown -R builder:builder "$repo_dir"
/usr/bin/python pkgbuilder
