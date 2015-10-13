import argparse
import shutil
import os

os.chdir(os.path.expanduser('~/Documents/ePubs'))


def split_filename(filename):
    series = False
    split = filename.split(' - ')
    author = split[-1].split('.')[0]
    if len(split) == 2:
        title = split[0]
    else:
        series = split[0]
        title = split[1]

    return author, series, title


def create_author_directory(author_name):
    if not os.path.isdir(author_name):
        os.mkdir(author_name)
    for filename in os.listdir('.'):
        if filename.split('.')[0] == author_name and os.path.isfile(filename):
            new_directory = split_filename(filename)[0]
            os.mkdir(new_directory)


def main():
    parser = argparse.ArgumentParser(
        description='Sort these nicely named epubs into a tree structure'
    )
    parser.add_argument(
        'author',
        type=str
    )
    args = parser.parse_args()
    author = args.author

    create_author_directory(author)

    for filename in os.listdir('.'):
        if filename.endswith(author + '.epub'):
            filename_sans_author = filename.replace(
                ' - ' + author + '.epub', '.epub')
            shutil.move(filename, os.path.join(author, filename_sans_author))
        

if __name__ == '__main__':
    main()