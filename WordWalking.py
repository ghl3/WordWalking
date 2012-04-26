#!/usr/bin/env python

import sys

from MakeDictionary import MakeDictionary


def Overlap( wordA, wordB ):
    
    if( len(wordA) != len(wordB) ):
        raise Exception()

    overlap = 0

    for i in range( len(wordA) ):
        if wordA[i] == wordB[i]:
            overlap += 1
        pass

    return overlap


def OneAway( wordA, wordB):

    overlap = Overlap( wordA, wordB )
    if overlap == len(wordA) - 1:
        return True
    return False


def WordWalk(begin, end):
    """ Talk two words of the same length and
    find a path between them using real dictionary
    words

    """

    if len( begin ) != len(end ):
        print "Words have unequal length"
        raise Exception()
    
    Dictionary = MakeDictionary( len(begin) )


    if begin not in Dictionary:
        print "Error: %s not in dictionary" % begin
        return


    current = begin
    distance = Overlap( current, end )
    UsedWords = set()

    path = [ begin ]


    """

    Algorithm:  
    - Start with beginning
    - Loop through the dictionary and find the first word that is 1 letter away
    - Check if that word is as close or closer to our target word.  If so, continue with loop
    - Record the path and never choose a word already on the path
    - If we fail to find a new word fulfilling the above, put the last word we landed on
      on a blacklist and never move to that word again. Then, start at the top
      and clear the path.

    """

    while current != end:

        distance = Overlap( current, end )

        if current in UsedWords:
            current = path[ -1 ]
            path = path[ : -1 ]
            continue

        MatchFound = False

        " LOOK FOR STRICTLY > Words"
        for word in Dictionary:

            if word == current: 
                continue

            if word in UsedWords:
                continue

            if word in path:
                continue

            if not OneAway( current, word ):
                continue

            if Overlap( word, end ) > distance:
                current = word
                MatchFound = True
                break
            pass


        " LOOK FOR >= Words"
        if not MatchFound:
            for word in Dictionary:

                if word == current: 
                    continue

                if word in UsedWords:
                    continue

                if word in path:
                    continue

                if not OneAway( current, word ):
                    continue

                if Overlap( word, end ) >= distance:
                    current = word
                    MatchFound = True
                    break
                pass


        if not MatchFound:
            print "Ran into dead end with: %s" % current
            if current == begin:
                print "Error: Didn't find a path from %s to %S" % (begin, end)
                return


            UsedWords.add( current )

            # If we can, go back only one step
            #current = begin
            #path = [ begin ]
            current = path[ -1 ]
            path = path[ : -1 ]
            
        else:
            path.append( current )

        pass

    
    # print path

    # Now, try to shorten the path if possible

    pathLength = len(path)

    for (i, step) in enumerate(path):
        if i > pathLength - 3:
            break

        if step == None: continue


        if OneAway( step, path[ i + 2 ] ):
            print "Unnecessary step: %s" % path[i+1] 
            path[i+1] = None

        pass

    path = [x for x in path if x != None]
        
    print path


    return

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print "Error: Must supply two words"
        raise Exception()


    begin = sys.argv[1]
    end = sys.argv[2]
    WordWalk(begin, end)
