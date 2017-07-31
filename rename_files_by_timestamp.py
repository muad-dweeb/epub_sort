import subprocess
from argparse import ArgumentParser
from os import path, listdir, rename

"""
IMAGES
Extract EXIF data from image files
Use the extracted data to assemble unique strings
Rename the files with these strings
"""


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
    args = parser.parse_args()

    rename_videos_in_dir(args.directory, args.extension)


if __name__ == '__main__':
    main()