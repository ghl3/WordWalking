#!/usr/bin/env python



class TreeNode:
    def __init__(self, value, last=None):
        self._value = value
        self._last = last
        self._next = [ ]
        self._regv = set() # registry holding unique values of all nodes
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

def test_tree():
    head = TreeNode("head")
    child1 = head.add_node("child1")
    child2 = head.add_node("child2")
    gchild = child1.add_node("gchild")
    print child1.vlineage()
    print gchild.vlineage()
    print gchild.head()
    print head._regv


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


def walk_from(start, dest):

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

    walkerL = TreeNode(start)
    walkerR = TreeNode(dest)

    for word in get_neighbors(walkerL._value, space):
        walkerL.add_node(word)

    for word in get_neighbors(walkerR._value, space):
        walkerR.add_node(word)

    candL = sorted(walkerL.values(), key=lambda x: metric(x, walkerR._value))

    print candL, [metric(c, walkerR._value) for c in candL]


if __name__ == "__main__":
    if False:
        test_tree()
        test_metric()
        test_get_neighbors()
    walk_from("book", "nook")

