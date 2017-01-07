#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
from random import choice
from string import ascii_lowercase, ascii_letters, ascii_uppercase, printable
from subprocess import call, check_call, check_output
from argparse import ArgumentParser

import pexpect
from os import path


class Crack():
    def __init__(self):
        self.attempted_strings = []
        # self.password_mode = mode

    def brute_force_encfs(self, password_length, encrypted_dir, visible_dir):
        char_set = ['n','b','m','h','j','u','i','y','j','k',';','l','o','a','d','s','c','v','g','f','r','e','w','t']
        passwords_list = (itertools.product(char_set, repeat=password_length))
        for p in passwords_list:
            # log_file = 'brute_force.log'
            password = (''.join(p))
            print(password)
            # print(check_call('encfs', encrypted_dir, visible_dir))
            child = pexpect.spawn('encfs {} {}'.format(encrypted_dir, visible_dir))
            # child.logfile_read = open(log_file, 'ab')
            child.expect(['EncFS Password: '])
            child.sendline(password)
            print(child)


    #     # mode: alpha_lower, numeric, all, etc.
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

def permute(length):
    return itertools.product(ascii_lowercase, repeat=length)


def parse_args():
    parser = ArgumentParser(description='Password Get')
    parser.add_argument('--absolute_length', '-al', type=int, optional=True,
                        help='Known character length of the target password')
    parser.add_argument('--encfs', type=tuple, default=False,
                        help='A tuple of paths (strings) in the form: (encrypted_dir, visible_dir)')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    char_length = args.absolute_length

    recover_my_damn_password = Crack()

    if args.encfs:
        encrypted_dir = path.expanduser(args.encfs[0])
        visible_dir = path.expanduser(args.encfs[1])
        recover_my_damn_password.brute_force_encfs(char_length, encrypted_dir, visible_dir)


if __name__ == '__main__':
    main()
