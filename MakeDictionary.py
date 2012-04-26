#!/usr/bin/env python

import sys

#from sets import Set

def MakeDictionary( WordSize=None ):
    """ Return a list of dictionary words

    If WordSize is supplied, only return words
    of that length
    """

    dictionary = set()

    inputDict = open( "/usr/share/dict/words", "r" )
    

    for word in inputDict:

        # Do any cleaning if necessary
        word = word.strip().lower()
        
        if WordSize != None:
            if len(word) != WordSize: 
                continue
            pass

        dictionary.add( word )

    inputDict.close()

    return dictionary


if __name__ == "__main__":
    WordSize=None
    if len(sys.argv) == 2:
        WordSize = int(sys.argv[1])
        print "Using Word Size: %s" % WordSize
    MakeDictionary(WordSize)
