import subprocess
from argparse import ArgumentParser
from os import path, listdir, rename
from PIL import Image, ExifTags


def get_exif(filename):
    # https://stackoverflow.com/a/765403/3900915
    decoded_tags = {}
    i = Image.open(filename)
    info = i._getexif()
    for tag, value in info.items():
        decoded = ExifTags.TAGS.get(tag, tag)
        decoded_tags[decoded] = value
    return decoded_tags


def rename_images_in_dir(dir, extension):
    """
    IMAGES
    Extract EXIF data from image files
    Use the extracted data to assemble unique strings
    Rename the files with these strings
    """
    dir_path = path.expanduser(dir)
    for filename in listdir(dir_path):
        if filename.endswith(extension):
            file_path = path.join(dir_path, filename)
            exif_tags = get_exif(file_path)
            print(exif_tags)


def rename_videos_in_dir(dir, extension):
    """
    VIDEOS
    Extract metadata timestamp from video files
    Use the extracted data to assemble unique strings
    Rename the files with these strings
    """
    dir_path = path.expanduser(dir)
    mapping = {}
    for filename in listdir(dir_path):
        if filename.endswith(extension):
            file_path = path.join(dir_path, filename)
            media_info = subprocess.check_output('mediainfo {} | grep -E "Encoded date"'.format(file_path),
                                                 shell=True).decode('utf-8')
            encoded_date = media_info.splitlines()[0].split('UTC ')[1]
            mapping[file_path] = encoded_date.replace('-', '').replace(' ', '_').replace(':', '') + extension

    for video in mapping:
        print(video + ' | ' + mapping[video])
        new_file_path = path.join(dir_path, mapping[video])
        if path.isfile(new_file_path):
            print('WARNING: File already exists ({})'.format(new_file_path))
            print('SKIPPING: {}'.format(video))
        else:
            # print('DEBUG: rename({}, {})'.format(video, new_file_path))
            rename(video, new_file_path)


def get_media_type(extension):
    # TODO: make this less stupid
    image_extensions = ['jpg', 'jpeg', 'png', 'gif']
    video_extensions = ['mpg', 'mpeg', 'avi', 'mkv', 'mp4']
    audio_extensions = ['mp3']

    ext = extension.lower().strip('.')
    if ext in image_extensions:
        return 'image'
    elif ext in video_extensions:
        return 'video'
    elif ext in audio_extensions:
        return 'audio'
    else:
        raise Exception('Extension {} is not currently supported'.format(ext))



def main():
    parser = ArgumentParser(
        description='Rename all media files according to timestamps extracted from metadata'
    )
    parser.add_argument(
        '--directory',
        '-d',
        type=str,
        help='The directory from which to operate'
    )
    parser.add_argument(
        '--extension',
        '-e',
        type=str,
        help='The extension to operate on'
    )
    # TODO: Add a TEST Flag that prints out the operations without doing them
    args = parser.parse_args()

    ext = get_media_type(args.extension)
    try:
        if ext == 'image':
            rename_images_in_dir(args.directory, args.extension)
        elif ext == 'video':
            rename_videos_in_dir(args.directory, args.extension)
        else:
            raise Exception('Audio not supported yet')
    except Exception as e:
        print(e)



if __name__ == '__main__':
    main()
