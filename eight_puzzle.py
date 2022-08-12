from searcher import *
from timer import *

def create_searcher(algorithm, param):
    """ a function that creates and returns an appropriate
        searcher object, based on the specified inputs. 
        inputs:
          * algorithm - a string specifying which algorithm the searcher
              should implement
          * param - a parameter that can be used to specify either
            a depth limit or the name of a heuristic function
        Note: If an unknown value is passed in for the algorithm parameter,
        the function returns None.
    """
    searcher = None
    
    if algorithm == 'random':
        searcher = Searcher(param)

    elif algorithm == 'BFS':
        searcher = BFSearcher(param)
    elif algorithm == 'DFS':
        searcher = DFSearcher(param)
    elif algorithm == 'Greedy':
        searcher = GreedySearcher(param)
    elif algorithm == 'A*':
       searcher = AStarSearcher(param)
    else:  
        print('unknown algorithm:', algorithm)

    return searcher

def eight_puzzle(init_boardstr, algorithm, param):
    """ a driver function for solving Eight Puzzles using state-space search
        inputs:
          * init_boardstr - a string of digits specifying the configuration
            of the board in the initial state
          * algorithm - a string specifying which algorithm you want to use
          * param - a parameter that is used to specify either a depth limit
            or the name of a heuristic function
    """
    init_board = Board(init_boardstr)
    init_state = State(init_board, None, 'init')
    searcher = create_searcher(algorithm, param)
    if searcher == None:
        return

    soln = None
    timer = Timer(algorithm)
    timer.start()
    
    try:
        soln = searcher.find_solution(init_state)
    except KeyboardInterrupt:
        print('Search terminated.')

    timer.end()
    print(str(timer) + ', ', end='')
    print(searcher.num_tested, 'states')

    if soln == None:
        print('Failed to find a solution.')
    else:
        print('Found a solution requiring', soln.num_moves, 'moves.')
        show_steps = input('Show the moves (y/n)? ')
        if show_steps == 'y':
            soln.print_moves_to()


def process_file(filename, algorithm, param):
    """For each line of the file, the function should:
        obtain the digit string on that line (stripping off the newline 
        at the end of the line) take the steps needed to solve the eight puzzle for that digit 
        string using the algorithm and parameter specified by the second and third inputs to the function
        report the number of moves in the solution, and the number of states tested during the search for a solution
        In addition, the function should perform the cumulative computations needed to report the following summary statistics after processing the entire file:
        number of puzzles solved
        average number of moves in the solutions
        average number of states tested
    """
    file = open(filename, 'r')
    count = 0  
    states_moves = 0
    states_tested = 0
   
    for line in file:
        sols = line.split('\n')
        d_string = sols[0]
        init_board = Board(d_string)
        init_state = State(init_board, None, 'init')
        searcher = create_searcher(algorithm, param)
        if searcher == None:
            return
        
        soln = None
        
        try:
            soln = searcher.find_solution(init_state)
            if soln == None:
                print(str(d_string) + ':', 'no solution')
            else:
                count += 1
                print(str(d_string) + ':', soln.num_moves, 'moves,', searcher.num_tested, 'states tested')
                states_moves += soln.num_moves
                states_tested += searcher.num_tested
        
        except KeyboardInterrupt:
            print(str(d_string) + ':', 'search terminated, no solution')
         
    file.close()
    
    print()
    print('solved', count, 'puzzles')
    if count != 0:
        print('averages:', states_moves/count, 'moves,' , states_tested/count, 'states tested')
    else:
        return 
    
    
   
    