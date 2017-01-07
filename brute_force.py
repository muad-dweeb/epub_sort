#!usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
from argparse import ArgumentParser
from os import path
from string import ascii_lowercase, ascii_letters, ascii_uppercase, printable

import time

from datetime import datetime
from pexpect import spawn

from utility_exceptions import UtilityException


class Crack():
    def __init__(self):
        self.attempted_strings = []
        self.password = ''
        # self.password_mode = mode

    def brute_force_encfs(self, password_length, char_set, encrypted_dir, visible_dir):
        if password_length:
            passwords_list = (itertools.product(char_set, repeat=password_length))
        else:
            passwords_list = (itertools.product(char_set))
        for p in passwords_list:
            # log_file = 'brute_force.log'
            password = (''.join(p))
            if password not in self.attempted_strings:
                print(password)
                # print(check_call('encfs', encrypted_dir, visible_dir))
                try:
                    child = spawn('encfs {} {}'.format(encrypted_dir, visible_dir))
                    # print(child.before)  # DEBUG
                    # child.logfile_read = open(log_file, 'ab')
                    child.expect('EncFS Password: ')
                    # time.sleep(0.1)
                    child.sendline(password)
                    result = child.expect(['Error decoding volume key, password incorrect', '[#\S] '])
                    if result == 0:
                        # print('Killing child {}'.format(child.name))
                        child.kill(0)
                        self.attempted_strings += password
                    elif result == 1:
                        print('Password found: {}'.format(password))

                except Exception as e:
                    print(e.message)

    """
    mode: alpha_lower, numeric, all, etc.
    """
    # def random_password_generator(self, password_length, password_mode):
    #     if password_mode == 'alpha_lower':
    #         mode = ascii_lowercase
    #     else:
    #         mode = printable
    #     password = ''
    #     while len(password) <= password_length:
    #     if password in self.attempted_strings:
    #         password += choice(mode)
    #
    #     print('Generated Password: {}'.format(password))
    #     self.attempted_strings.append(password)
    #     return password


# def permute(length):
#     return itertools.product(ascii_lowercase, repeat=length)


def parse_args():
    parser = ArgumentParser(description='Password Get')
    parser.add_argument('--absolute_length', '-al', type=int, default=None,
                        help='Known character length of the target password')
    parser.add_argument('--encfs', type=str, default=False,
                        help='A string of paths delimited by space in the form: encrypted_dir visible_dir')
    parser.add_argument('--char_set', '-c', type=str, default='printable',
                        help='Set of characters from which to build passwords.')
    args = parser.parse_args()
    return args


def select_character_set(string_char_set):
    # ascii_lowercase, ascii_letters, ascii_uppercase, printable
    if string_char_set.lower().replace('_', ' ') == 'ascii lowercase':
        char_set = ascii_lowercase
    elif string_char_set.lower().replace('_', ' ') == 'ascii letters':
        char_set = ascii_letters
    elif string_char_set.lower().replace('_', ' ') == 'ascii uppercase':
        char_set = ascii_uppercase
    elif string_char_set.lower() == 'printable':
        char_set = printable
    else:
        char_set = string_char_set.split(' ')
        # raise UtilityException('Invalid String character set specified.')
    print('Character Set:\n\t{}'.format(char_set))
    return char_set


def main():
    args = parse_args()
    char_length = args.absolute_length
    char_set = select_character_set(args.char_set)

    start_time = datetime.now()
    recover_my_damn_password = Crack()

    if args.encfs:
        paths = args.encfs.split(' ')
        encrypted_dir = path.expanduser(paths[0])
        visible_dir = path.expanduser(paths[1])
        recover_my_damn_password.brute_force_encfs(char_length, char_set, encrypted_dir, visible_dir)

    end_time = datetime.now()
    run_time = end_time - start_time
    print('Time elapsed: {}'.format(run_time))


if __name__ == '__main__':
    main()
