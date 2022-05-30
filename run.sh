#!/bin/bash

## <Edit this values>
HOST_REPO_DIR='/var/Storage/Repo/private-arch-repo'
HOST_REPO_PKG_DIR='/var/Storage/Repo/private-arch-repo-pkgs'
## </Edit this values>

docker run -u builder --rm -v ${HOST_REPO_DIR}:/var/Repo -v ${HOST_REPO_PKG_DIR}:/var/RepoPkgs arch-pkgbuild start-builder
