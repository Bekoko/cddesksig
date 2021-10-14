#bash
sudo apt-get update

# venv
python3 -m venv env_cddesksig
source env_cddesksig/bin/activate

# app
git clone https://github.com/Bekoko/cddesksig.git

# dependencies
pip install -r cddesksig/requirements.txt -y

# start local server
python3 cddesksig/manage.py runserver

