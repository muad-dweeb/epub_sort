#!/bin/bash

# Exit immediately if a simple command exits with a non-zero status...
set -e

# Print a trace of simple commands and their arguments...
#set -x

# Get dir to rotate wallpapers from
rotate_dir=$1

# Get the currently set wallpaper
current_image=$(gsettings get org.gnome.desktop.background picture-uri)

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

# Do the thing
$(gsettings set org.gnome.desktop.background picture-uri "file://$1${image_array[$next]}")
