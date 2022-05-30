[![License][License-shield]][License-url]

# private-arch-repo
#### A self hosted build system for Arch Linux packages

# DESCRIPTION
[Arch Linux](https://archlinux.org/) is one of the most popular Linux distros out there. But unfortunately, the official Arch repo has significantly fewer packages than Ubuntu or Debian. Users mostly rely on [AUR](https://aur.archlinux.org/) for the packages not available in the official repo. AUR comes with a catch- a user must build the packages locally using `makepkg` or an AUR helper. Although repo for prebuild AUR packages (like Chaotic AUR) exists. They do not contain all the packages a user wants. This program enables Arch Linux users to have their personal repo with packages they want.

# GETTING STARTED

1. [Install docker](https://docs.docker.com/engine/install/)

2. Clone the repo
    ```
    git clone https://github.com/rafiibrahim8/private-arch-repo.git && cd private-arch-repo
    ```

3. Create `gnupg.tar.gz` (see [CREATING/EDITING FILES](#creatingediting-files))

4. Edit `internal-scripts/init-image.sh` (see [CREATING/EDITING FILES](#editing-internal-scriptsinit-imagesh))

5. Run `make-image.sh`
    ```
    bash make-image.sh
    ```

6. Edit packages on `aur_packages.json` and `non-aur-packages` accoding to your need (see [EDITING PACKAGES](#editing-packages)).

7. Edit `run.sh` (see [CREATING/EDITING FILES](#creatingediting-files))

8. Copy/Move `aur_packages.json` and `non-aur-packages` to `HOST_REPO_PKG_DIR` of your `run.sh` file.

9. Run `run.sh`
    ```
    bash run.sh
    ```

10. [Configure NGINX](#configuring-nginx)

9. [Add Repo to PACMAN](#adding-repo-to-pacman)

# CONFIGURING NGINX

1. [Install NGINX](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)

2. Create a new file on `/etc/nginx/sites-available` named `arch-repo.conf` and paste following into it:
    ```
    server {
        listen 80;
        server_name arch-repo.local;
        
        location / {
            root <cloned repo path>/output/; 
            autoindex on;
       }
    }
    ```
    **N.B: Replace `<cloned repo path>` avobe with the absolute path where you cloned this repo.**

3. Run the following commands:
    ```
    echo "127.0.0.1 arch-repo.local" | sudo tee -a /etc/hosts
    sudo systemctl enable nginx
    sudo systemctl restart nginx
    ```

# ADDING REPO TO PACMAN
1. Add the following line at the end of `/etc/pacman.conf`:
    ```
    [private-arch-repo]
    Server = http://arch-repo.local
    ```

2. Run the following commands:
    ```
    sudo pacman-key --recv-keys <Key ID>
    sudo pacman-key --lsign-key <Key ID>
    ```
    **N.B: Replace `<Key ID>` avobe with the Key ID obtained during creating `gnupg.tar.gz`.**

# EDITING PACKAGES
You can add AUR and non-AUR packages to the build system.

* To add AUR packages simply edit `aur_packages.json` file. The file is a json array of packages.

* To add non-AUR packages make a folder in `non-aur-packages` with the package name. The folder must have two files `configure.py` and `config.json`. `configure.py` will genarate `PKGBUILD` file and `config.json` will contain config values.

# CREATING/EDITING FILES

## Creating gnupg.tar.gz
`gnupg.tar.gz` contains keys to sign packages.
To create it follow the steps
1. Backup your current keys:
    ```
    mv .gnupg .gnupg.bak
    ```
    
2. Create new key
    ```
    gpg --full-generate-key
    ```
    You will get output like:
    ```
    pub   rsa3072 2021-02-21 [SC] [expires: 2026-02-20]
      410B637614A906DFAA2B26DC9AE4D939F0C017EF
    uid                      John Doe <me@example.com>
    sub   rsa3072 2022-02-21 [E] [expires: 2027-02-20]
    ```
    Here `410B637614A906DFAA2B26DC9AE4D939F0C017EF` is your Key ID. We will need this later.

3. Upload Key
    ```
    gpg --send-keys <Key ID>
    ```

4. Create `gnupg.tar.gz`
    ```
    cd
    tar -cvf gnupg.tar.gz .gnupg
    rm -r .gnupg
    ```

5. Restore backup
    ```
    mv .gnupg.bak .gnupg
    ```

## Editing internal-scripts/init-image.sh
The lines between `<Edit this values>` and `</Edit this values>` on `internal-scripts/init-image.sh` contains editable parameters.

The parameters are follows:

* `FULL_NAME`: Your full name 
* `EMAIL`: Your email address
* `KEY`: Key ID
* `REPO_NAME`: Name of your repository
* `MIRRIRLIST_URL`: Pacman mirrorlist file url

## Editing run.sh
The lines between `<Edit this values>` and `</Edit this values>` on `run.sh` contains editable parameters.

The parameters are follows:

* `HOST_REPO_DIR`: Local Machine directory where the packages will be saved
* `HOST_REPO_PKG_DIR`: The local directory which will contain `aur_packages.json` and `non-aur-packages`

# ISSUES

This is very early stage of the program. It might be very buggy. You are always welcome to [create an issue](https://github.com/rafiibrahim8/private-arch-repo/issues) or [submit a pull request](https://github.com/rafiibrahim8/private-arch-repo/pulls).

[License-shield]: https://img.shields.io/github/license/rafiibrahim8/private-arch-repo
[License-url]: https://github.com/rafiibrahim8/private-arch-repo/blob/master/LICENSE

