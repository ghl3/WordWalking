#!/usr/bin/env python

import itertools
import optparse


class TreeNode:
    def __init__(self, value, last=None):
        self._value = value
        self._last = last
        self._next = [ ]
        self._regn = [ ] # registry holding all nodes
        self._regv = set() # registry holding unique values of all nodes
        self.head()._regn.append(self)
        self.head()._regv.add(value)
    def add_node(self, value):
        new_node = TreeNode(value, self)
        self._next.append(new_node)
        return new_node
    def vlineage(self):
        """
        Returns the successive ancestor values from this node, from youngest to oldest.
        """
        return [self._value] + (self._last.vlineage() if self._last else [ ])
    def nlineage(self):
        """
        Returns the successive ancestor nodes from this node, from youngest to oldest.
        """
        return [self] + (self._last.nlineage() if self._last else [ ])
    def head(self):
        return self.nlineage()[-1]
    def values(self):
        return [x._value for x in self._next]
    def all_values(self):
        return self.head()._regv
    def all_nodes(self):
        return self.head()._regn
    def size(self):
        return len(self.all_nodes())


def test_tree():
    head = TreeNode("head")
    child1 = head.add_node("child1")
    child2 = head.add_node("child2")
    gchild = child1.add_node("gchild")
    print child1.vlineage()
    print gchild.vlineage()
    print gchild.head()
    print head.all_values()
    print [n._value for n in head.all_nodes()]


def metric(word1, word2):
    return sum([a!=b for a, b in zip(word1, word2)])


def test_metric():
    print "golf and barf have distance", metric("golf", "barf")
    print "book and nook have distance", metric("book", "nook")


def collect_words_of_length(size, loc='/usr/share/dict/words'):
    """
    Return a list of dictionary words having length `size`.
    """
    try:
        inputDict = open(loc, "r")
    except:
        raise IoError("Could not find unix dictionary '%s'" % loc)
    return [w.strip() for w in inputDict if len(w.strip()) == size]


def get_neighbors(word, candidates, exclude=[], pred=list):
    return pred([w for w in candidates if metric(word, w) == 1 and
                 w not in exclude])


def test_get_neighbors():
    allwords = collect_words_of_length(4)
    print get_neighbors("barf", allwords, exclude=["barn", "zarf"])


def choose_next_target(sL, sR, space, exclude=[]):
    """
    Given two lists of nodes, finds the pair (tL, tR) such that tL in sL and tR
    in sR with the smallest metric distance. Expand the list of neighbors for
    those two nodes.
    """
    print "choosing next target pair...",
    print "L/R sniffer sizes are (%d, %d)" % (sL.size(), sR.size()),

    dist, tL, tR = sorted([(metric(s._value, t._value), s, t)
                           for s, t in itertools.product(sL.all_nodes(),
                                                         sR.all_nodes())
                           if (s._value, t._value) not in exclude])[0]

    print "best pair is (%s, %s) with distance %d" % (tL._value, tR._value, dist)

    candL = get_neighbors(tL._value, space, exclude=tL.all_values())
    candR = get_neighbors(tR._value, space, exclude=tR.all_values())

    if not tL._next:
        for s in candL: tL.add_node(s)
    if not tR._next:
        for s in candR: tR.add_node(s)

    return dist, (tL, tR)


def walk_from(start, dest):
    """
    Uses a slightly intelligent strategy to get from `start` to `dest`. It does
    a depth-first search from both ends. A list of all 'sniffed' words from both
    sides is maintained. Each iteration, the closest pair of words is
    identified, and that word expanded with all its neighbors on each side.
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

    snifferL = TreeNode(start)
    snifferR = TreeNode(dest)

    for s in get_neighbors(snifferL._value, space): snifferL.add_node(s)
    for s in get_neighbors(snifferR._value, space): snifferR.add_node(s)

    already_tried = set()

    while True:
        dist, best = choose_next_target(snifferL, snifferR, space, exclude=already_tried)
        already_tried.add((best[0]._value, best[1]._value))
        if dist == 0:
            print "got it!"
            p = list(reversed(best[0].vlineage())) + best[1].vlineage()[1:]
            print ("path %d: (" % len(p)) + " -> ".join(p) + ")"
            break


def main():
    """
    Take two words of the same length and return a path between them using only
    1-letter pertubations. Every word in the path must be a valid word in the
    dictionary.
    """
    vers = "0.2-zrakey"

    desc = " ".join(main.__doc__.split())
    parser = optparse.OptionParser(description=desc, version=vers,
                                   usage="%prog golf bird [options]")
    opts, args = parser.parse_args()
    try:
        start, dest = args[0:2]
    except:
        print "usage: ww3.py golf bird"
    walk_from(start, dest)


def run_tests():
    test_tree()
    test_metric()
    test_get_neighbors()


if __name__ == "__main__":
    main()

