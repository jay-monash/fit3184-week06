#!/bin/bash
sudo apt update && sudo apt install -y python3-venv ca-certificates curl
python3 -m venv ~/venv
source ~/venv/bin/activate
pip3 install fastapi uvicorn

sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update

sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin mariadb-client

# Add yourself to the docker group so that you can run docker commands
sudo usermod -aG docker $USER

# alternatively,refresh your current shell
exec sudo su -l $USER