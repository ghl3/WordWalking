#!/usr/bin/env python

import sys

from MakeDictionary import MakeDictionary


def Overlap( wordA, wordB ):
    """ Find the letter-overlap between two words

    Requre that the words be the same length, else
    throw an exception.
    """
    
    if( len(wordA) != len(wordB) ):
        raise Exception("Overlap - Non Equal Words")

    overlap = 0

    for i in range( len(wordA) ):
        if wordA[i] == wordB[i]:
            overlap += 1
        pass

    return overlap


def OneAway( wordA, wordB):
    """ Return whether two words differ by one letter

    """


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
        raise Exception("WordWalk - Unequal Words")


    Dictionary = MakeDictionary( len(begin) )
        

    if begin not in Dictionary:
        print "Error: %s not in dictionary" % begin
        return

    # 'current' is the current node (the string name of the word')
    # 'distance' is the distance between the current word and 'end', the target
    current = begin
    distance = Overlap( current, end )
    DeadEndWords = set()

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

        # Calculate the current distance to the target
        distance = Overlap( current, end )

        # If the current word is a DeadEnd, 
        # then we take one step backwords
        # We back up our path as well
        if current in DeadEndWords:
            current = path[ -1 ]
            path = path[ : -1 ]
            continue

        MatchFound = False

        " LOOK FOR STRICTLY > Words"
        for word in Dictionary:

            # Ignore the current word
            if word == current: 
                continue

            # Never jump to a Dead End
            if word in DeadEndWords:
                continue

            # Don't go backwords here
            if word in path:
                continue

            # Must of course be one away
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


                # Ignore the current word
                if word == current: 
                    continue

                # Never jump to a Dead End
                if word in DeadEndWords:
                    continue

                # Don't go backwords here
                if word in path:
                    continue

                # Must of course be one away
                if not OneAway( current, word ):
                    continue

                # Allow for traversing to an equivalant node
                if Overlap( word, end ) >= distance:
                    current = word
                    MatchFound = True
                    break
                pass


        # If we can't find a word that fulfills the above,
        # we must take action.  We call the current word
        # a "dead end" and we back out.
        if not MatchFound:
            print "Ran into dead end with: %s" % current
            if current == begin:
                print "Error: Didn't find a path from %s to %S" % (begin, end)
                return


            DeadEndWords.add( current )

            # If we can, go back only one step
            #current = begin
            #path = [ begin ]
            current = path[ -1 ]
            path = path[ : -1 ]

        # If we DID find a word, append it
        # to the path and keep looking
        else:
            path.append( current )

        pass

    

    # Now, try to shorten the path if possible
    # Sometimes we take unnecessary steps:
    # 1 -> 2 -> 3, where we could just do 1 -> 3
    # We here eliminate those steps from the path
    pathLength = len(path)

    for (i, step) in enumerate(path):
        if i > pathLength - 3:
            break

        if step == None: continue

        # If path[ i + 1 ] is unnecessary, 
        # we eliminate it (set it to None)
        # This will be cleaned up later
        if OneAway( step, path[ i + 2 ] ):
            print "Unnecessary step: %s" % path[i+1] 
            path[i+1] = None

        pass

    # Clean out the bad steps
    path = [x for x in path if x != None]
        
    print path


    return

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print "Error: Must supply two words"
        raise Exception("main - Bad Input")

    begin = sys.argv[1]
    end = sys.argv[2]
    WordWalk(begin, end)
    
