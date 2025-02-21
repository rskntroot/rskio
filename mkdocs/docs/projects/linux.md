# Linux Setup

## Brief

some setup guides

- by `rskntroot` on `2025-02-20`

## Debian

### SSH

- see [K4YT3X's Hardened OpenSSH Server Configuration](https://github.com/k4yt3x/sshd_config)

``` bash
sudo -i
cd /etc/ssh/
mv sshd_config sshd_config.backup
curl https://raw.githubusercontent.com/k4yt3x/sshd_config/master/sshd_config -o ./sshd_config
sed -i 's/^#DebianB/DebianB/' sshd_config
chmod 644 /etc/ssh/sshd_config
systemctl restart ssh
exit
```

=== "New Key"

    ``` bash
    ssh-keygen -t ecdsa
    cat id_ecdsa.pub >> ~/.ssh/authorized_keys
    ```

=== "Existing Key"

    ``` bash
    key="ecdsa-sha2-nistp256 ASASDASDFsomekey user@whatever"
    ```

    ``` bash
    mkdir ~/.ssh && echo ${key} >> ~/.ssh/authorized_keys
    ```

``` bash
sudo -i
cat <<%% >> /etc/ssh/sshd_config
###RSKIO
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
%%
systemctl restart ssh
exit
```

### Docker

### Setup Docker

- see https://docs.docker.com/engine/install/ubuntu/

``` bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo systemctl enable --now docker
rm -f ./get-docker.sh
sudo usermod -a -G docker $(whoami)
docker ps
```

- see https://docs.docker.com/config/completion/

``` bash
sudo apt install bash-completion -y
cat <<%% >> ~/.bashrc
if [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
fi
%%
mkdir -p ~/.local/share/bash-completion/completions
docker completion bash > ~/.local/share/bash-completion/completions/docker
source ~/.bashrc
```

### Tools

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

### Shortcuts

- see [fastfetch](https://github.com/fastfetch-cli/fastfetch) for more info

=== "ARM_64"

    ``` bash
    mkdir ~/Downloads/ && cd Downloads
    curl -L https://github.com/fastfetch-cli/fastfetch/releases/download/2.37.0/fastfetch-linux-aarch64.deb -o fastfetch-linux-aarch64.deb
    sudo dpkg -i fastfetch-linux-aarch64.deb
    cd ~
    ```

=== "x86_64"

    ``` bash
    mkdir ~/Downloads/ && cd Downloads
    curl -L https://github.com/fastfetch-cli/fastfetch/releases/download/2.37.0/fastfetch-linux-amd64.deb -o fastfetch-linux-amd64.deb
    sudo dpkg -i fastfetch-linux-amd64.deb
    cd ~
    ```

``` bash
cat <<%% >> ~/.bashrc
# RSKIO
fastfetch
alias q="exit"
%%
source ~/.bashrc
```
