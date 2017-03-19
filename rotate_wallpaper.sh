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

# Go to the specified directory
pushd $rotate_dir

# Get the next index in the array
count=0
for i in "${image_array[@]}"
do
	let "count+=1"
	if [[ $current_image == \'file://$1$i\' ]]; then
		let "next=$count"
	fi
done

# Reset the image loop
if [[ $next -ge $count ]]; then
	next=0
fi

$(gsettings set org.gnome.desktop.background picture-uri "file://$1${image_array[$next]}")



#for i in "${rotate_images[@]}"
#do 
#    fullpath=$1$i
#    echo $fullpath
#done
