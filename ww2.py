#!/usr/bin/env python

import sys
import itertools


def collect_words_of_length(size, loc='/usr/share/dict/words'):
    """
    Return a list of dictionary words having length `size`.
    """
    try:
        inputDict = open(loc, "r")
    except:
        raise IoError("Could not find unix dictionary '%s'" % loc)
    return [w.strip() for w in inputDict if len(w.strip()) == size]


def walk_from(start, dest, max_depth=4):
    """
    Finds all shortest paths between words `start` and `dest`. Only generates
    paths of odd length.
    """
    if len(start) != len(dest):
        print "words must be of equal length", start, dest
        return None

    space = collect_words_of_length(len(start))

    def append_one_aways(seq):
        """
        `seq` is a list of lists: [['dog', 'dag'], ['dog', 'bog'], ...]
        """
        new_seq = [ ]
        for s in seq:
            new_seq += [s + [w] for w in space if
                        sum([a != b for a,b in zip(w, s[-1])]) == 1]
        return new_seq

    gL = [[start]]
    gR = [[dest]]

    depth = 0
    npaths = 0

    while npaths == 0 and depth < max_depth:
        print "trying depth", depth
        gL = append_one_aways(gL)
        gR = append_one_aways(gR)

        for L, R in itertools.product(gL, gR):
            if L[-1] == R[-1]:
                path = L + list(reversed(R))[1:]
                npaths += 1
                print ' -> '.join(path)
        depth += 1

    print ("found %d paths of length %d from %s to %s" %
           (npaths, 2*depth + 1, start, dest))


if __name__ == "__main__":
    try:
        start, dest = sys.argv[1:3]
    except:
        print "usage: ww2.py golf bird"

    walk_from(start, dest)
