#bash
sudo apt-get update

# app
git clone https://github.com/Bekoko/cddesksig.git

# venv
python3 -m venv env_cddesksig
source env_cddesksig/bin/activate

# dependencies
pip install -r cddesksig/requirements.txt -y

# start local server
python3 cddesksig/manage.py runserver

