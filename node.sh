# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl -y
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-compose -y

git clone https://rafliher:xx@github.com/rafliher/wreckitattdef-node.git
cd wreckitattdef-node
sudo python3 starter.py | sudo tee -a /var/log/node.log




cd wreckitattdef-node
git pull https://rafliher:xx@github.com/rafliher/wreckitattdef-node.git
sudo docker compose -f services/docker-compose.yml up --build -d
sudo docker compose -f services/docker-compose.yml up --build --force-recreate -d

sudo python3 starter.py | sudo tee -a /var/log/node.log
