#!/bin/bash

####################################################################
#                 ONE-OFF VIDEO CONVERSION SCRIPT                  #
#                                                                  #
# Convert a user-defined directory of videos to a hardcoded format #
#  This was made for a set of unreasonably large 1080p .MTS files  #
#     Assumes all directory contents are staged for conversion     #
#                   Creates .mkv files as output                   #
####################################################################

# Exit immediately if a simple command exits with a non-zero status...
set -e

# Print a trace of simple commands and their arguments...
#set -x

# Get dir in which to convert videos
# This is an unnamed argument to be passed at runtime
video_dir=$1

# Move to video directory
pushd $video_dir

# Assign the videos in the video directory to an array
videos=$(ls $video_dir)
video_array=($videos)

# Iterate through the videos
count=0
for i in "${video_array[@]}"
do
	let "count+=1"
	# Convert the video
	echo "Converting video: $i"
	filename="${i%.*}"
	COMMAND="ffmpeg -i $i -codec:v libx264 -preset medium -vf scale=1280:720:force_original_aspect_ratio=decrease -crf 24 -codec:a copy $filename.mkv"
	echo $COMMAND
	$COMMAND
done

echo "Finished converting $count videos."

# Exit video directory
popd
