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


def walk_from(start, dest):
    print "attempting to walk from %s to %s" % (start, dest)
    if len(start) != len(dest):
        print "words must be of equal length", start, dest
        return None

    space = collect_words_of_length(len(start))

    def one_away_from(word):
        return [w for w in space if sum([a != b for a,b in zip(w, word)]) == 1]

    gen1L = one_away_from(start)
    gen1R = one_away_from(dest)

    gen2L = [{'seed': w, 'stem': one_away_from(w)} for w in gen1L]
    gen2R = [{'seed': w, 'stem': one_away_from(w)} for w in gen1R]

    intermed = set()

    for gL, gR in itertools.product(gen2L, gen2R):
        overlap = set(gL['stem']) & set(gR['stem'])
        if overlap:
            for o in overlap:
                print [start, gL['seed'], o, gR['seed'], dest]


if __name__ == "__main__":
    try:
        start, dest = sys.argv[1:3]
    except:
        print "usage: ww2.py golf bird"

    walk_from(start, dest)
