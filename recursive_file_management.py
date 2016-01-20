import os
import argparse


def rename_files(directory_to_crawl, change_from, change_to):
    count = 0
    for root, dirs, files in os.walk(directory_to_crawl):
        for f in files:
            if f == change_from:
                os.rename(os.path.join(root, change_from), os.path.join(root, change_to))
                print('{} renamed to {}'.format(change_from, change_to))
                count += 1
    print('{} files modified'.format(count))


def delete_files(directory_to_crawl, filename_to_delete):
    count = 0
    for root, dirs, files in os.walk(directory_to_crawl):
        for f in files:
            if f == filename_to_delete:
                target = os.path.join(root, filename_to_delete)
                os.remove(target)
                print('{} deleted'.format(target))
                count += 1
    print('{} files deleted'.format(count))


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
        'target_file_name',
        type=str,
        help='The name of the file(s) on which you wish to operate'
    )
    parser.add_argument(
        '-r', '--rename',
        type=str,
        help='The name you wish to give your files'
    )
    parser.add_argument(
        '-d', '--delete',
        action='store_true',
        default=False,
        help='Delete all occurrences of target_file_name in directory tree'
    )
    args = parser.parse_args()

    if args.rename and args.delete:
        print('You make no sense')
        exit()
    elif args.rename:
        rename_files(args.directory,
                     args.target_file_name,
                     args.rename)
    elif args.delete:
        delete_files(args.directory,
                     args.target_file_name)


if __name__ == '__main__':
    main()
