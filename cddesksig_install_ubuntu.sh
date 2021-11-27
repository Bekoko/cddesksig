#bash

sudo add-apt-repository universe

sudo apt-get update && sudo apt-get upgrade -y

sudo apt install git -y
sudo apt-get install python3-pip -y
sudo apt-get install python3-venv -y

sudo python3 -m pip install -U pip
sudo python3 -m pip install -U setuptools

sudo apt-get install libzbar0

git clone https://github.com/Bekoko/cddesksig.git

python3 -m venv env_cddesksig
source "/home/ubuntu/Desktop/env_cddesksig/bin/activate"

pip3 install --upgrade setuptools
pip3 install --upgrade pip

pip3 install -r "/home/ubuntu/Desktop/cddesksig/requirements.txt"

xdg-open http://localhost:8000

python3 "/home/ubuntu/Desktop/cddesksig/manage.py" runserver

