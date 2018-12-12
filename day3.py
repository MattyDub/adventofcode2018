import sys
import itertools
from collections import namedtuple

Claim = namedtuple('Claim', ['id', 'x', 'y', 'width', 'height'])

def parse_claim(line):
    """ Parse a claim from the format provided into a "Claim" namedtuple.
    Input format: #<claim id> @ <x>,<y>: <width>x<height>
    """
    id_str, rest = line.split('@')
    x_y_str, dim_str = rest.split(':')
    claim_id = int(id_str.strip().replace('#', ''))
    x, y = x_y_str.strip().split(',')
    width, height = dim_str.strip().split('x')
    return Claim(claim_id, int(x), int(y), int(width), int(height))

def calc_overlap(claim1, claim2):
    """ Return a set of tuples that represent the (x, y) points in the area of overlap
        between two claims """
    x1 = max(claim1.x, claim2.x)
    x2 = min((claim1.x + claim1.width), (claim2.x + claim2.width))
    y1 = max(claim1.y, claim2.y)
    y2 = min((claim1.y + claim1.height), (claim2.y + claim2.height))
    return [(x, y) for x in xrange(x1, x2) for y in xrange(y1, y2)]

def get_claim_overlaps(claims):
    """ Take a list of all claims, and convert them into a set of x,y coordinates
    that constitute the "overlaps"."""
    non_overlapping_id = 0
    overlaps = []

    for i, claim1 in enumerate(claims):
        overlapped = False
        for j, claim2 in enumerate(claims):
            if claim1.id != claim2.id:
                overlap = calc_overlap(claim1, claim2)
                if overlap:
                    overlapped = True
                    overlaps.extend(overlap)
        if not overlapped:
            non_overlapping_id = claims[i].id
    return set(itertools.chain(overlaps)), non_overlapping_id

def main(filename):
    claims = []
    with open(filename) as f:
        for line in f:
            claims.append(parse_claim(line.strip()))
        claim_overlaps, non_overlapping_id = get_claim_overlaps(claims)
        print "There are {} square inches in the overlaps; claim {} had no overlaps".format(len(claim_overlaps), non_overlapping_id)
    
if __name__ == '__main__':
    main(sys.argv[1])
