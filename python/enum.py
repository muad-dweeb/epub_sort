def enum(*sequential, **named):
    """python 2.x does not support enums, this is a workaround
    http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python"""

    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)
