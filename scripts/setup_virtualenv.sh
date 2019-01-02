#!/bin/bash

# Assumes no pre-existing virtualenv setup

# Install packages
sudo apt-get install python-pip
sudo pip install --upgrade pip
sudo pip install virtualenv virtualenvwrapper
sudo apt install virtualenv

echo "Add the following lines to .bashrc:"
echo 'export WORKON_HOME=$HOME/.virtualenvs'
echo 'export PIP_DOWNLOAD_CACHE=$HOME/.pip_download_cache'
echo 'source /usr/local/bin/virtualenvwrapper.sh'
