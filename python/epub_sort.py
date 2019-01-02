#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from os import path, listdir, mkdir, rename

# def main():
#     parser = argparse.ArgumentParser(
#         description='Sort these nicely named epubs into a nested directory structure'
#     )
#     parser.add_argument(
#         'author',
#         type=str
#     )
#     args = parser.parse_args()
#     author = args.author
#
#     create_author_directory(author)
#
#     for filename in os.listdir('.'):
#         if filename.endswith(author + '.epub'):
#             filename_sans_author = filename.replace(
#                 ' - ' + author + '.epub', '.epub')
#             shutil.move(filename, os.path.join(author, filename_sans_author))
from utility_exceptions import UtilityException


# def split_filename(filename):
#     series = False
#     split = filename.split(' - ')
#     author = split[-1].split('.')[0]
#     if len(split) == 2:
#         title = split[0]
#     else:
#         series = split[0]
#         title = split[1]
#
#     return author, series, title


def main():
    """
    One-off script
    Sort relatively conveniently-named epub files into a nested directory structure
    """
    parser = ArgumentParser(
        description='Sorts flat dir of epubs into nested directory structure'
    )
    parser.add_argument('--base-dir', type=str, required=True)
    parser.add_argument('--simulate-output', '-s', action='store_true', required=False)
    parser.add_argument('--exclude', '-e', type=str, required=False)
    args = parser.parse_args()
    base_dir = path.expanduser(args.base_dir)
    simulate = args.simulate_output
    exclude = args.exclude

    if simulate is True:
        print('SIMULATED RUN!')
    else:
        print('HERE WE GO!')

    if exclude:
        print('Excluding {}'.format(exclude))

    # Get unsorted ePubs
    library = sorted(listdir(base_dir))
    if len(library) < 1:
        raise UtilityException('Yo dawg this dir is empty: {}'.format(base_dir))

    # Sort books
    sorted_count = 0
    for content in library:
        source_path = path.join(base_dir, content)
        if path.isfile(source_path) and not content.startswith(exclude) and content.endswith('.epub'):
            sorted_count += 1
            split_filename = content.split('- ')

            # Create author dirs
            author = split_filename[-1].rsplit('.', 1)[0].strip()
            author_dir = path.join(base_dir, author)
            if not path.isdir(author_dir):
                if simulate is True:
                    print('Simulate dir creation: {}'.format(author_dir))
                else:
                    mkdir(author_dir)
                    print('Created {}'.format(author_dir))

            # Create series dirs
            if len(split_filename) == 3:
                numbered_series = split_filename[0].strip()
                series = numbered_series.rsplit(' ', 1)[0]
                series_dir = path.join(author_dir, series)
                if not path.isdir(series_dir):
                    if simulate is True:
                        print('Simulate dir creation: {}'.format(series_dir))
                    else:
                        mkdir(series_dir)
                        print('Created {}'.format(series_dir))

                # Move series books into series dirs
                book_title = split_filename[1].rstrip()
                new_file = book_title + '.epub'
                dest_path = path.join(series_dir, new_file)
                if simulate is True:
                    print(dest_path)
                else:
                    rename(source_path, dest_path)

            # Move remaining books into author dirs
            elif len(split_filename) == 2:
                book_title = split_filename[0].rstrip()
                new_file = book_title + '.epub'
                dest_path = path.join(author_dir, new_file)
                if simulate is True:
                    print(dest_path)
                else:
                    rename(source_path, dest_path)

            else:
                print('SKIPPING: {}'.format(content))

    print('Sorted {} books'.format(sorted_count))

if __name__ == '__main__':
    main()