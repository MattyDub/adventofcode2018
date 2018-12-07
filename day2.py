import sys
import itertools
from collections import Counter


def letter_freqs(word):
    return {v:k for k, v in Counter(word).iteritems()}

def hamming_distance(s1, s2):
    """ Ripped straight from https://en.wikipedia.org/wiki/Hamming_distance#Algorithm_example """
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))


def calc_pseudo_checksums(filename):
    two_count = 0
    three_count = 0
    with open(filename) as f:
        for line in f:
            Freqs = letter_freqs(line)
            try:
                _ = freqs[2]
                two_count += 1
            except KeyError:
                pass
            try:
                _ = freqs[3]
                three_count += 1
            except KeyError:
                pass
        return two_count * three_count

def file_to_list(file_handle):
    ret = [line.strip() for line in file_handle]
    return ret


def find_similar_strings(filename):
    common_chars = ""
    with open(filename) as f:
        lines = file_to_list(f)
        for word1, word2 in itertools.product(lines, lines):
            try:
                h_d = hamming_distance(word1, word2)
                # print "word1 = {}\n1word2 = {}\nhamming distance = {}\n------------".format(word1, word2, h_d)
                if h_d == 1:
                    common_chars = "".join([el1 for el1, el2 in zip(word1, word2) if el1 == el2])
                    break
            except ValueError:
                pass
    return common_chars

def main(filename):
    print "'checksum' = {}".format(calc_pseudo_checksums(filename))
    print "common chars = {}".format(find_similar_strings(filename))

if __name__ == '__main__':
    main(sys.argv[1])
