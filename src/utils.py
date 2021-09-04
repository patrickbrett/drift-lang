from argparse import ArgumentParser
import string


def flatten(t):
    return [item for sublist in t for item in sublist]


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                        help="Filename to load", metavar="FILE")
    args = parser.parse_args()
    return args


def is_variable(token):
    lw = set(string.ascii_lowercase)
    return all(char in lw for char in token)


def split_list(l, token):
    new_list = []
    curr = []
    for elem in l:
        if elem == token:
            new_list.append(curr)
            curr = []
        else:
            curr.append(elem)
    new_list.append(curr)
    return new_list
