import os
import argparse


def rename_files(directory_to_crawl, change_from, change_to):
    for root, dirs, files in os.walk(directory_to_crawl):
        for f in files:
            if f == change_from:
                os.rename(os.path.join(root, change_from), os.path.join(root, change_to))
                print('{} renamed to {}'.format(change_from, change_to))


def main():
    parser = argparse.ArgumentParser(
        description='Rename all occurrences of FILE_NAME to NEW_NAME'
    )
    parser.add_argument(
        'directory',
        type=str,
        help='The directory from which to crawl'
    )
    parser.add_argument(
        'current_file_name',
        type=str,
        help='The name of the file(s) you wish to rename'
    )
    parser.add_argument(
        'intended_file_name',
        type=str,
        help='The name you wish to give your files'
    )
    args = parser.parse_args()

    rename_files(args.directory,
                 args.current_file_name,
                 args.intended_file_name)


if __name__ == '__main__':
    main()
