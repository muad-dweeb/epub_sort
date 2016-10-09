import json
from os import path
from collections import Counter, OrderedDict
from string import ascii_lowercase, punctuation, whitespace


class Target():
    def __init__(self, file_to_be_compressed):
        self.original_path = path.expanduser(file_to_be_compressed)
        self.contents = self.get_contents()
        self.mapping = {}

    def get_contents(self):
        with open(self.original_path, 'r') as source:
            contents = source.read()
        return contents

    def compress(self):
        key_counts = {}
        for key in self.contents.split():
            if len(key) > 2:
                key_counts[key] += 1
        for key, value in key_counts:
            if value <= 2:
                del key_counts[key]
        json_keys = json.dumps(key_counts)
        # print(json_keys)  # DEBUG
        # dictionary sorted by value
        ordered_count = [sorted(key_counts)]
        # print(ordered_count)  # DEBUG
        # find top ten counts, assign [0-9] to keys in mapping
        for i in range(10):
            key = ordered_count[-i]
            self.mapping[key] = i
            del ordered_count[key]
        # find up to 26 next top counts, assign [a-z] to keys in mapping
        followers = ordered_count[:-26]
        for i in range(len(followers)):
            key = ascii_lowercase[i]
            self.mapping[key] = i
            del ordered_count[key]
        # create a copy of file contents
        new_contents = self.contents
        for key, value in self.mapping:
            new_contents.replace(key, value)
        return(new_contents)

    def decompress(self):
        pass


def test_compress_file(file_path):
    target = Target(file_path)
    print(target.compress())


if __name__ == '__main__':
    test_compress_file("~/muad-dweeb/utilities/data/youth.txt")