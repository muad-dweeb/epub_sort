import os
import json
from argparse import ArgumentParser


def read_tsv(input_file):
    """
    Opens a provided TSV input file and yields line JSON using the header as keys
    :param input_file: Valid TSV file path. The first line will be considered the header
    :yield: line_jsons assembled by mapping the line values to the header keys by index
    """
    try:
        with open(input_file, 'r') as input:
            # first line in a tsv (the header)
            header_text = input.readline()
            # ordered list of header keys
            key_list = header_text.strip('\n').split('\t')
            # starts on next line
            for line in input.readlines():
                line_json = {}
                # ordered list of line values
                line_list = line.strip('\n').split('\t')
                # map values to keys
                index = 0
                for key in key_list:
                    value = line_list[index]
                    # change empty strings to None (null)
                    if value == '':
                        value = None
                    line_json.update({key:value})
                    index += 1
                yield line_json
    except IOError as e:
        raise Exception('File {} invalid. Error: {}'.format(input_file, e))


def dump_to_file(lines, output_file):
    """
    Opens an output file and dumps JSON lines into it
    :param lines: A generator created using read_tsv()
    :param output_file: A provided file path to save output to
    """
    try:
        with open(output_file, 'w') as output:
            for line in lines:
                json.dump(line, output)
                output.write('\n')
    except IOError as e:
        raise Exception('JSON dumping failed to file {}. Error: {}'.format(output_file, e))


def main():
    parser = ArgumentParser(description='Take an input TSV file and generate a line JSON output file')
    parser.add_argument('--input-file', '-i', type=str, required=True,
                        help='A valid TSV file path including header')
    parser.add_argument('--output-file', '-o', type=str, required=True,
                        help='File path for the desired line JSON output')
    args = parser.parse_args()
    input = args.input_file
    output = args.output_file
    try:
        input_path = os.path.expanduser(input)
        output_path = os.path.expanduser(output)
        line_jsons = read_tsv(input_path)
        dump_to_file(line_jsons, output_path)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
