#bash
sudo apt-get update

# base lib
sudo apt-get install python3.6
sudo apt install python3-pip
sudo apt-get install git
sudo curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt install nodejs
sudo apt-get install network-manager
systemctl start NetworkManager.service 
systemctl enable NetworkManager.service

# venv
python3 -m venv env_cddesksig
source env_cddesksig/bin/activate

# app
git clone https://github.com/Bekoko/cddesksig.git

# dependencies
pip install -r cddesksig/requirements.txt

# ganache-cli
git clone https://github.com/trufflesuite/ganache.git
cd ganache
npm install
npm start
cd ..

# desconect from internet
nmcli networking off

# start local server
python3 cddesksig/manage.py runserver

