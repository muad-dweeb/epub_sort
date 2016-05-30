#!/bin/bash

echo "Enabling MultiArch"
sudo dpkg --add-architecture i386

echo "Adding PPAs"
sudo apt-add-repository -y ppa:yktooo/ppa
sudo apt-add-repository -y "deb http://archive.canonical.com/ $(lsb_release -sc) partner"
sudo add-apt-repository -y ppa:webupd8team/sublime-text-3
sudo add-apt-repository -y ppa:noobslab/themes
sudo add-apt-repository -y ppa:noobslab/icons
sudo add-apt-repository -y ppa:moka/stable
sudo add-apt-repository -y ppa:numix/ppa

echo "Updating APT"
sudo apt-get update

echo "Installing Applications"
APPS="git \
indicator-sound-switcher \
skype \
sublime-text-installer \
gimp \
darktable \
htop \
unity-tweak-tool"
sudo apt-get install -y $APPS

echo "Installing Themes"
THEMES="hackstation-theme"
sudo apt-get install -y $THEMES

echo "Installing Icons"
ICONS="moka-icon-theme \
numix-icon-theme-circle \
ardis-icons"
sudo apt-get install -y $ICONS

cd /tmp

echo "Installing Google Chrome"
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb

echo "Installing TeamViewer"
wget http://download.teamviewer.com/download/teamviewer_i386.deb
sudo dpkg -i ./teamviewer_i386.deb

echo "Installing Steam"
wget https://steamcdn-a.akamaihd.net/client/installer/steam.deb
sudo dpkg -i steam.deb

cd

echo "Fixing Dependencies"
sudo apt-get -f install

echo "Installing PyCharm"
wget https://download.jetbrains.com/python/pycharm-community-2016.1.4.tar.gz
tar xfz pycharm-*.tar.gz
rm pycharm-*.tar.gz
cd pycharm-*
cd bin
./pycharm.sh