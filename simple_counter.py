#!/usr/bin/env python
# -*- coding: utf-8 -*-


# http://stackoverflow.com/a/510364/6364
class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""

    def __init__(self):
        try:
            self.impl = _GetchWindows()

        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

c = 0
while True:
    ch = getch()
    if ch == '\x03':
        print()
        break
    c += 1
    print("\r", c, end='')


# class Clicker(object):
#     def __init__(self):
#         self.count = 0
#
#     def click(self):
#         self.count += 1
#         if self.count > 0:
#             print(self.count, end='\r', )
#
#
# def main():
#     clicky = Clicker()
#     while True:
#         clack = input()
#         if not clack:
#             clicky.click()
#         else:
#             exit()
#
#
# if __name__ == '__main__':
#     main()
