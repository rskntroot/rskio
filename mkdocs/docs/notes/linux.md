# Linux Setup

## Brief

some setup guides

- by `rskntroot` on `2025-02-20`

## Preferences

### SSH

- see [K4YT3X's Hardened OpenSSH Server Configuration](https://github.com/k4yt3x/sshd_config)

``` bash
sudo -i
```

``` bash
cd /etc/ssh/
mv sshd_config sshd_config.backup
curl https://raw.githubusercontent.com/k4yt3x/sshd_config/master/sshd_config -o ./sshd_config
chmod 644 /etc/ssh/sshd_config
cat <<%% >> /etc/ssh/sshd_config
# Enable Public Key Auth
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
%%
systemctl restart ssh
exit
```

### Auth

=== "Existing Key"

    ``` bash
    key="ecdsa-sha2-nistp256 ASASDASDFsomekey user@whatever"
    ```

    ``` bash
    mkdir -p ~/.ssh && echo ${key} >> ~/.ssh/authorized_keys
    ```

=== "New Key"

    ``` bash
    ssh-keygen -t ecdsa
    cat id_ecdsa.pub >> ~/.ssh/authorized_keys
    ```

### Docker

- see [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)

``` bash
sudo -i
curl -fsSL https://get.docker.com | sh
systemctl enable --now docker
```

``` bash
usermod -aG docker ${SOME_USER}
docker ps
```

#### Completion

- see [https://docs.docker.com/config/completion/](https://docs.docker.com/config/completion/)

=== "docker"

    ``` bash
    mkdir -p ~/.local/share/bash-completion/completions
    docker completion bash > ~/.local/share/bash-completion/completions/docker
    source ~/.bashrc
    ```

=== "bash"

    ``` bash
    sudo apt install bash-completion -y
    ```

    ``` bash
    cat <<%% >> ~/.bashrc
    if [ -f /etc/bash_completion ]; then
        . /etc/bash_completion
    fi
    %%
    ```



### Tools

=== "Debian"

    ``` bash
    sudo apt install -y \
      curl \
      htop \
      iputils-ping \
      jq \
      tcpdump \
      traceroute \
      vim
    ```

=== "Fedora"

    ``` bash
    sudo dnf install -y \
      htop \
      sensors
    ```

### Shortcuts

#### fastfetch

- see [fastfetch](https://github.com/fastfetch-cli/fastfetch/releases) for more info

``` bash
url="https://github.com/fastfetch-cli/fastfetch/releases/download/2.47.0/fastfetch-linux-amd64.deb"
```

``` bash
mkdir -p ~/downloads/ && cd ~/downloads
curl -fsSL ${url} -o fastfetch.deb
sudo dpkg -i ./fastfetch.deb
```

#### Profile

``` bash
cat <<%% >> ~/.bashrc
# RSKIO
alias ..="cd .."
alias ...="cd ..."
alias q="exit"
alias ff="fastfetch"
%%
source ~/.bashrc
```
