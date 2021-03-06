#!/usr/bin/env python

import sys
import optparse
import threading

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


def CleanPathList(path_list):
    """ Take a path list and shorten it if possible

    """

    short_path = []

    itr_first = 0
    while itr_first < len(path_list):
        
        word_first = path_list[itr_first]
        short_path.append(word_first)
        
        itr_second = len(path_list) - 1
        while itr_second > itr_first:
            word_second = path_list[itr_second]

            if OneAway(word_first, word_second):
                itr_first = itr_second - 1
                break
            else:
                itr_second -= 1
            
        
        itr_first += 1
        

    return short_path


def GoodPath( path, start, end ):
    """ Check that the path we produce is valid
    """

    if path[0] != start: return False
    if path[-1] != end: return False

    for i, word in enumerate(path):
        if i == len(path)-1: break
        if not OneAway(word, path[i+1]):
            return False
    
    return True


def WordWalk(start, dest, clean=True, verbose=False, reverse=False, 
             DeadEndWords=None, GlobalFlags=None):
    """
    Talk two words of the same length and find a path between them using real
    dictionary words
    """

    if len(start) != len(dest):
        print "Words have unequal length"
        raise Exception("WordWalk: unequal length words, idiot!")
    word_list = collect_words_of_length(len(start))

    if start not in word_list:
        print "Error: %s not in dictionary" % start
        return

    if dest not in word_list:
        print "Error: %s not in dictionary" % dest
        return

    # 'current' is the current node (the string name of the word') 'distance' is
    # the distance between the current word and 'dest', the target
    current = start
    if DeadEndWords==None:
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


    def node_metric( wordA, wordB ):
        """ Return the value difference between words 

        For now, simply uses the distance
        Can be made smarter in the future, so we
        keep it generic
        """
        return Overlap( wordA, wordB )


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

        # Excape if the EscapeFlag is true
        if GlobalFlags != None and GlobalFlags["StopFlag"]:
            raise Exception("Terminated")

        if verbose: print "\n",  path

        # Calculate the current distance to the target
        current_distance = node_metric(current, dest)

        """
        New Algorithm:
        Loop through all elements
        Calculate their distances
        If the distance is a jump > 1, 
        return right away.
        Else, take the maximum distance
        """
        
        match_found=False
        next_node_word_value = (None, None)

        for word in word_list:
            if not check_acceptable_node(word): continue
            match_found=True
            node_distance = node_metric(word, dest)

            """ Break right away if a large jump"""
            if node_distance - current_distance > 0:
                next_node_word_value = (word, node_distance)
                break
            
            """ Else, only change if we get an increase """
            next_node_word_value = max( (word, node_distance), next_node_word_value, 
                                       key=(lambda x: x[1]) )
            

        if next_node_word_value == (None, None):
            print "Ran into dead end with: %s" % current

            """ If the start is a dead end, we failed """
            if current == start:
                print "Error: Didn't find a path from %s to %s" % (start, dest)
                return

            DeadEndWords.add(current)

            # If we can, go back only one step
            current = path[-2]
            path = path[:-1]


        else:
            next_node = next_node_word_value[0]
            current = next_node
            path.append( next_node )

    """
    Now, try to shorten the path if possible
    Sometimes we take unnecessary steps:
    1 -> 2 -> 3, where we could just do 1 -> 3
    We here eliminate those steps from the path

    TO DO: For now, I only check 1 -> 2 -> 3 == 1 -> 3
    but I could do this with 1 -> N1 -> N2 -> ... -> M == 1 -> M
    """
    
    if not GoodPath(path, start, dest):
        print "Error: Found path, but it is invalid"
        raise Exception("Invalid Path")

    if clean:
        path = CleanPathList(path)

    if reverse:
        path.reverse()

    if path == None:
        raise Exception("path==None")
    
    return path

def threaded_walker(name="thread", GlobalPath=None, **kwargs):
    
    print "Starting thread: ", name
    
    # Get the GlobalFlags from the kwargs
    GlobalFlags = kwargs["GlobalFlags"]

    # Start the process using the global DeadEndWords
    try:
        path = WordWalk( **kwargs )
    except Exception:
        print "Terminating Thread:", name
        return
        
    # In case the stop flag wasn't seen by the process,
    # check it here
    if GlobalFlags["StopFlag"]:
        return

    # Else, set it to
    # kill the other threads
    GlobalFlags["StopFlag"] = True

    # After all the threads are dead, set the global path
    # This prevents other threads from messing it up
    GlobalPath.extend(path)
    
    print "Thread succeeded: ", name
        
    return


def main():
    """
    Take two words of the same length and return a path between them using only
    1-letter pertubations. Every word in the path must be a valid word in the
    dictionary.
    """

    vers = "0.1"

    desc = " ".join(main.__doc__.split())
    parser = optparse.OptionParser(description=desc, version=vers, usage="%prog [options]")

    parser.add_option( "-v", "--verbose", dest="verbose",
                       action="store_true", default=False,
                       help="Print the path as it is walked.")

    parser.add_option( "-c", "--clean", dest="clean",
                       action="store_true", default=True,
                       help="Clean the final path to reduce unnecessary steps." )

    parser.add_option( "-t", "--threads", dest="use_threads",
                       action="store_true", default=False,
                       help="Launch multiple parallel threads." )

    # Parse the command line options:
    options, args = parser.parse_args()
    if len(args) != 2:
        print "Error: Must supply two words as arguments"
        return

    start_word, dest = args[0:2]

    if len(start_word) != len(start_word):
        print "Error: Words must be the same length"
        return 255

    """
    To Do: Add (uncorrelated) threading which starts from both ends
    To Do: Add threading which walks from both ends and quits if they
           meet in the middle (ie if their paths intersect)
    """

    if not options.use_threads:
        print WordWalk(start=start_word, dest=dest,
                       verbose=options.verbose, clean=options.clean) 
        return

    
    # Create the global variables
    DeadEndWords = set()
    path = []
    GlobalFlags = {"StopFlag" : False}

    # Create the threads
    # threading_args = (path, StopFlag, DeadEndWords)
    common_options = {"verbose" : options.verbose, "clean" : options.clean,  
                      "DeadEndWords" : DeadEndWords, "GlobalFlags" : GlobalFlags,
                      "GlobalPath" : path}
                   
    forward_args = {"name" : "forward_walker", "start" : start_word, "dest" : dest, "reverse" : False}
    forward_args.update(common_options)
    forward_walker = threading.Thread(target=threaded_walker, kwargs=forward_args)

    backward_args = {"name" : "backward_walker", "start" : dest, "dest" : start_word, "reverse" : True}
    backward_args.update(common_options)
    backward_walker = threading.Thread(target=threaded_walker, kwargs=backward_args)

    # Start the threads and join
    forward_walker.start()
    backward_walker.start()

    forward_walker.join()
    backward_walker.join()

    print "All Threads Ended"
    print "Final Answer: ", path
    return



if __name__ == "__main__":
    from timeit import Timer
    t = Timer("main()", "from __main__ import main")
    print "ran in %f seconds" % t.timeit(number=1)
