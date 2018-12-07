import sys
import itertools


def file_to_list(file_handle):
    ret = [line for line in file_handle]
    return ret

def main(filename):
    print "opening {}".format(filename)
    total = 0
    seen_freqs = set()
    with open(filename) as f:
        file_values = file_to_list(f)
        for elem in itertools.cycle(file_values):
            total += int(elem)
            if total in seen_freqs:
                print "first repeated frequency: {}".format(total)
                break
            else:
                seen_freqs.add(total)

    print "total = {}; ".format(total)

if __name__ == '__main__':
    main(sys.argv[1])
