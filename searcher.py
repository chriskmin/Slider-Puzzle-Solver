import random
from state import *

class Searcher:
    """ A class for objects that perform random state-space
        search on an Eight Puzzle.
        This will also be used as a superclass of classes for
        other state-space search algorithms.
    """
    def __init__(self, depth_limit):
        """ constructs a new Searcher object by initializing the following
        attributes: an attribute states for the Searcher‘s list of untested 
        states; it should be initialized to an empty list an attribute 
        num_tested that will keep track of how many states the Searcher 
        tests; it should be initialized to 0 an attribute depth_limit that 
        specifies how deep in the state-space search tree the Searcher will 
        go; it should be initialized to the value specified by the parameter 
        depth_limit. (A depth_limit of -1 will be used to indicate that the 
        Searcher does not use a depth limit.)
        """
        self.states = []
        self.num_tested = 0
        self.depth_limit = depth_limit
    
    def __repr__(self):
        """ returns a string representation of the Searcher object
            referred to by self.
        """
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        if self.depth_limit == -1:
            s += 'no depth limit'
        else:
            s += 'depth limit = ' + str(self.depth_limit)
        return s

    def add_state(self, new_state):
        """takes a single State object called new_state 
        and adds it to the Searcher‘s list of untested 
        states.
        """
        self.states.append(new_state)
        
    def should_add(self, state):
        """takes a State object called state and returns True
        if the called Searcher should add state to its list 
        of untested states, and False otherwise.
        """
        if state.creates_cycle():
            return False
        else:
            if self.depth_limit == -1:
                return True
            else:
                if state.num_moves > self.depth_limit:
                    return False
                else:
                    return True
            
    def add_states(self, new_states):
        """takes a list State objects called new_states, 
        and that processes the elements of new_states 
        one at a time as follows
        """
        for s in new_states:
            if self.should_add(s):
                self.add_state(s)
                
    def next_state(self):
        """ chooses the next state to be tested from the list of 
        untested states, removing it from the list and returning it
        """
        s = random.choice(self.states)
        self.states.remove(s)
        return s

    def find_solution(self, init_state):
        """performs a full state-space search that begins at the 
        specified initial state init_state and ends when the goal
        state is found or when the Searcher runs out of untested states.
        """
        self.add_state(init_state)
        while len(self.states) > 0:
            test_state = self.next_state()
            self.num_tested += 1 
            if test_state.is_goal():
                return test_state
            else:
                self.add_states(test_state.generate_successors())
        return None
        
    #BFS and DFS searchers
class BFSearcher(Searcher):
    """ A class for objects that performs Breadth-First Search
        search on an Eight Puzzle.
        This will also be used as a superclass of classes for
        other state-space search algorithms.
    """
    def next_state(self):
        """ overrides (i.e., replaces) the next_state method 
        that is inherited from Searcher.
        """
        s = self.states[0]
        self.states.remove(s)
        return s
    
class DFSearcher(Searcher):
    """ A class for objects that performs Depth-First Search
        search on an Eight Puzzle.
        This will also be used as a superclass of classes for
        other state-space search algorithms.
    """
    def next_state(self):     
        """overrides (i.e., replaces) the next_state method 
        that is inherited from Searcher.
        """
        s = self.states[-1]
        self.states.remove(s)
        return s
                                     
#heuristic functions                   
def h0(state):
    """ a heuristic function that always returns 0 """
    return 0

def h1(state):
    """takes a State object called state, and that computes and 
    returns an estimate of how many additional moves are needed to 
    get from state to the goal state
    """
    return state.board.num_misplaced()




class GreedySearcher(Searcher):
    """ A class for objects that perform an informed greedy state-space
        search on an Eight Puzzle.
    """
    def __init__(self, heuristic):
        """The constructor should begin by calling the constructor 
            inherited from the superclass; this will allow that superclass 
            constructor to initialize the inherited attributes. Use the super() 
            function to access the __init__ method in the superclass (as we did 
            in the constructor for the Holiday class from lecture), and pass in
            a value of -1 to indicate that GreedySearcher objects will not use 
            a depth limit.
        """
        super().__init__(heuristic)
        self.heuristic = heuristic
        self.depth_limit = -1
        
    def __repr__(self):
        """ returns a string representation of the GreedySearcher object
            referred to by self.
        """
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        s += 'heuristic ' + self.heuristic.__name__
        return s

    def priority(self, state):
        """ computes and returns the priority of the specified state,
            based on the heuristic function used by the searcher
        """
        return -1 * self.heuristic(state)

    def add_state(self, state):
        """ overrides (i.e., replaces) the 
            add_state method that is inherited from Searcher.
        """
        self.states.append([self.priority(state),state])

    def next_state(self):
        """overrides (i.e., replaces) the next_state method 
            that is inherited from Searcher. 
        """
        s = max(self.states)
        self.states.remove(s)
        return s[1]

class AStarSearcher(GreedySearcher):
    """  A class for objects that performs A* State Search
             search on an Eight Puzzle.
             This will also be used as a superclass of classes for
             other state-space search algorithms.
    """
    def priority(self, state):
        """ computes and returns the priority of the specified state,
        based on the heuristic function used by the searcher
        """
        return -1 * (self.heuristic(state) + state.num_moves)