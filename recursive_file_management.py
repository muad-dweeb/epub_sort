import argparse
import os
import shutil


def rename_files(directory_to_crawl, change_from, change_to):
    count = 0
    for root, dirs, files in os.walk(directory_to_crawl):
        for f in files:
            if f == change_from:
                os.rename(os.path.join(root, change_from), os.path.join(root, change_to))
                # print('{} renamed to {}'.format(change_from, change_to))
                count += 1
    print('{} files renamed\n{} >> {}'.format(count, change_from, change_to))


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


def aggregate_files(directory_to_crawl, filename_to_aggregate, destination):
    count = 0
    if not os.path.isdir(destination):
        os.mkdir(destination)
        print('{} created'.format(destination.upper()))
    for root, dirs, files in os.walk(directory_to_crawl):
        for f in files:
            if f == filename_to_aggregate:
                f_path = os.path.join(root, f)
                f_parent = os.path.split(os.path.split(f_path)[0])[1]
                f_destination = os.path.join(destination, f_parent)
                shutil.copy2(f_path, f_destination)
                print('{} copied to {}'.format(os.path.join(f_parent, f), f_destination))
                count += 1
    print('{} files aggregated'.format(count))


def redistribute_aggregated_files(aggregation_directory, filename_to_redistribute, destination):
    pass


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
    parser.add_argument(
        '-a', '--aggregate',
        type=str,
        help='Aggregate all occurrences of target_file_name in directory tree to SPECIFIED_DESTINATION'
    )
    args = parser.parse_args()

    #  probably a better way to handle the following check
    if (args.rename and args.delete and args.aggregate) or \
            (args.rename and args.delete) or \
            (args.rename and args.aggregate) or \
            (args.delete and args.aggregate):
        print('Too many options!')
        exit()
    elif args.rename:
        rename_files(args.directory,
                     args.target_file_name,
                     args.rename)
    elif args.delete:
        delete_files(args.directory,
                     args.target_file_name)
    elif args.aggregate:
        aggregate_files(args.directory,
                        args.target_file_name,
                        args.aggregate)


if __name__ == '__main__':
    main()
