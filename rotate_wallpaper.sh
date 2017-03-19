#!/bin/bash

# Exit immediately if a simple command exits with a non-zero status...
set -e

# Print a trace of simple commands and their arguments...
#set -x

# Get dir to rotate wallpapers from
rotate_dir=$1

# Get the currently set wallpaper
current_image=$(gsettings get org.gnome.desktop.background picture-uri)
echo "Current Image: $current_image"

# Assign the images in the rotation directory to an array
rotate_images=$(ls $rotate_dir)
image_array=($rotate_images)

# Get the next index in the array
count=0
for i in "${image_array[@]}"
do
	let "count+=1"
	if [[ $current_image == \'file://$1$i\' ]]; then
		# let "next=$count"
		next=$count
	fi
done

# Reset the image loop
if [[ $next -ge $count ]]; then
	next=0
fi

# Get the next wallpaper to set
next_image="file://$1${image_array[$next]}"

# export DBUS_SESSION_BUS_ADDRESS environment variable
# http://stackoverflow.com/a/19666729/3900915
PID=$(pgrep gnome-session)
export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$PID/environ|cut -d= -f2-)

# Do the thing
echo "Next Image: $next_image"

command="gsettings set org.gnome.desktop.background picture-uri $next_image"
echo $command
$command
