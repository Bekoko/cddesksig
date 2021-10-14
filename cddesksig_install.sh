#bash
sudo apt-get update

# app
git clone https://github.com/Bekoko/cddesksig.git

# venv
python3 -m venv env_cddesksig
source "/home/kali/Desktop/env_cddesksig/bin/activate"

# dependencies
pip install -r "/home/kali/Desktop/cddesksig/requirements.txt"

# start local server
python3 cddesksig/manage.py runserver

