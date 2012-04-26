#!/usr/bin/env python

import sys
import optparse


def collect_words_of_length(size, loc='/usr/share/dict/words'):
    """
    Return a list of dictionary words having length `size`.
    """

    try:
        inputDict = open(loc, "r")
    except:
        raise IoError("Could not find unix dictionary '%s'" % loc)
    return set([w.strip() for w in inputDict if len(w.strip()) == size])


def Overlap(wordA, wordB):
    """
    Find the letter-overlap between two words

    Require that the words be the same length, else throw an exception.
    """
    if len(wordA) != len(wordB):
        raise Exception("Overlap - Non Equal Words")
    overlap = 0
    for a,b in zip(wordA, wordB):
        if a == b:
            overlap += 1
    return overlap


def OneAway(wordA, wordB):
    """
    Return whether two words differ by one letter
    """
    overlap = Overlap( wordA, wordB )
    if overlap == len(wordA) - 1:
        return True
    return False


def WordWalk(start, dest, clean=True, verbose=False):
    """
    Talk two words of the same length and find a path between them using real
    dictionary words
    """

    if len(start) != len(dest):
        print "Words have unequal length"
        raise Exception("WordWalk: unequal length words, idiot!")
    Dictionary = collect_words_of_length(len(start))

    if start not in Dictionary:
        print "Error: %s not in dictionary" % start
        return

    if dest not in Dictionary:
        print "Error: %s not in dictionary" % dest
        return

    # 'current' is the current node (the string name of the word') 'distance' is
    # the distance between the current word and 'dest', the target
    current = start
    DeadEndWords = set()
    path = [start]


    def check_acceptable_node(word):
        """ Determine if we can move to the node 'word'
        
        """
        # Ignore the current word
        if word == current: 
            return False
        
        # Never jump to a Dead End
        if word in DeadEndWords:
            return False

        # Don't go backwords here
        if word in path:
            return False

        # Must of course be one away
        if not OneAway(current, word):
            return False

        return True


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

    while current != dest:
        if verbose: print "\n",  path

        # Calculate the current distance to the target
        distance = Overlap(current, dest)
        
        '''
        if current in DeadEndWords:
            """
            If the current word is a DeadEnd, then we take one step backwords We
            back up our path as well.
            """
            current = path[-2]
            path = path[:-1]
            continue
        '''
        MatchFound = False


        """ look for strictly > nodes"""
        for word in Dictionary:
            if check_acceptable_node(word) and Overlap(word, dest) > distance:
                current = word
                MatchFound = True
                break

        """ look for >= nodes """
        if not MatchFound:
            for word in Dictionary:
                if check_acceptable_node(word) and Overlap(word, dest) >= distance:
                    current = word
                    MatchFound = True
                    break

        """ allow for any nodes """
        if not MatchFound:
            for word in Dictionary:
                if check_acceptable_node(word):
                    current = word
                    MatchFound = True
                    break

        # If we can't find a word that fulfills the above, we must take action.
        # We call the current word a "dead end" and we back out.
        if not MatchFound:
            print "Ran into dead end with: %s" % current

            # If the start is a dead end, we failed
            if current == start:
                print "Error: Didn't find a path from %s to %s" % (start, dest)
                return

            DeadEndWords.add(current)

            # If we can, go back only one step
            current = path[-2]
            path = path[:-1]

        # If we DID find a word, append it to the path and keep looking
        else:
            path.append(current)


    
    """
    Now, try to shorten the path if possible
    Sometimes we take unnecessary steps:
    1 -> 2 -> 3, where we could just do 1 -> 3
    We here eliminate those steps from the path

    TO DO: For now, I only check 1 -> 2 -> 3 == 1 -> 3
    but I could do this with 1 -> N1 -> N2 -> ... -> M == 1 -> M
    """

    if not clean:
        print path
        return

    pathLength = len(path)

    for i, step in enumerate(path):
        if i > pathLength - 3:
            break

        if step == None: continue

        # If path[ i + 1 ] is unnecessary, we eliminate it (set it to None) This
        # will be cleaned up later
        if OneAway( step, path[ i + 2 ] ):
            print "Unnecessary step: %s" % path[i+1] 
            path[i+1] = None

    # Clean out the bad steps
    path = [x for x in path if x != None]
    print path


def main():
    """
    Take two words of the same length and return a path between them using only
    1-letter pertubations. Every word in the path must be a valid word in the
    dictionary.
    """
    vers = "0.1"
    parser = optparse.OptionParser(description=main.__doc__.replace("    ", " "),
                                   version=vers,
                                   usage="%prog [options]")

    parser.add_option( "-v", "--verbose", dest="verbose",
                       action="store_true", default=False,
                       help="Print the path as it is walked.")

    parser.add_option( "-c", "--clean", dest="clean",
                       action="store_true", default=True,
                       help="Clean the final path to reduce unnecessary steps." )

    # Parse the command line options:
    options, args = parser.parse_args()
    start_word, dest = args[0:2]

    if len(start_word) != len(start_word):
        print "Error: Words must be the same length"
        return 255

    WordWalk(start=start_word,
             dest=dest,
             verbose=options.verbose, clean=options.clean) 


if __name__ == "__main__":
    main()
