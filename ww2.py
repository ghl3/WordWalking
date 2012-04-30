#!/usr/bin/env python

import optparse
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
    Finds all shortest paths between words `start` and `dest`. Uses a very
    stupid algorithm which tries to brute-force breadth-first expand all paths
    leading from the start and ending points simultaneously, and hopes to God to
    stumble over the same word in both directions.
    """
    if len(start) != len(dest):
        print "words must be of equal length", start, dest
        return None

    space = collect_words_of_length(len(start))

    if start not in space:
        print start, "is not in the dictionary"
        return
    if dest not in space:
        print dest, "is not in the dictionary"
        return

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
    paths = set()

    while not paths and depth < max_depth:
        print "trying depth", depth
        gL = append_one_aways(gL)
        gR = append_one_aways(gR)

        for L, R in itertools.product(gL, gR):
            overlap = set(L) & set(R)
            if overlap:
                a = list(overlap)[0]
                paths.add(tuple(L[:L.index(a)+1]) +
                          tuple(reversed(R[:R.index(a)])))

        depth += 1

    for n, p in enumerate(paths):
        print ("path %d: (" % n) + " -> ".join(p) + ")"


def main():
    """
    Take two words of the same length and return a path between them using only
    1-letter pertubations. Every word in the path must be a valid word in the
    dictionary.
    """
    vers = "0.1-zrakey"

    desc = " ".join(main.__doc__.split())
    parser = optparse.OptionParser(description=desc, version=vers,
                                   usage="%prog golf bird [options]")
    parser.add_option( "-d", "--max-depth", dest="max_depth", type=int, default=3)
    opts, args = parser.parse_args()
    try:
        start, dest = args[0:2]
    except:
        print "usage: ww2.py golf bird"
    walk_from(start, dest, max_depth=opts.max_depth)


if __name__ == "__main__":
    from timeit import Timer
    t = Timer("main()", "from __main__ import main")
    print "ran in %f seconds" % t.timeit(number=1)
