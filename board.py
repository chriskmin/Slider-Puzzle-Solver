GOAL_TILES = [['0', '1', '2'],
              ['3', '4', '5'],
              ['6', '7', '8']]

class Board:
    """ A class for objects that represent an Eight Puzzle board.
    """
    def __init__(self, digitstr):
        """ a constructor for a Board object whose configuration
            is specified by the input digitstr
            input: digitstr is a permutation of the digits 0-9
        """
    
        assert(len(digitstr) == 9)
        for x in range(9):
            assert(str(x) in digitstr)

        self.tiles = [[''] * 3 for x in range(3)]
        self.blank_r = -1
        self.blank_c = -1

    
        for i in range(len(digitstr)):
            self.tiles[i//3][i%3] = digitstr[i]
            if digitstr[i] ==  '0':
                self.blank_c = i%3
                self.blank_r = i//3


    def __repr__(self):
        """returns a string representation of a Board object
        """
        s = ''
        for r in range(len(self.tiles)):
            for c in range(len(self.tiles[0])):
                if self.tiles[r][c] == '0':
                    s += '_ '
                else:
                    s += self.tiles[r][c] + ' '
            s += '\n' 
        return s
    
    
    def move_blank(self, direction):
        """takes as input a string direction that specifies 
        the direction in which the blank should move, and that 
        attempts to modify the contents of the called Board object
        accordingly. 
        """
        if direction == 'up':
            blank_up = self.blank_r - 1
            if blank_up < 0:
                return False
            else: 
                up_copy = self.tiles[blank_up][self.blank_c]
                self.tiles[self.blank_r][self.blank_c] = up_copy
                self.tiles[blank_up][self.blank_c] = '0'
                self.blank_r -= 1
                return True
                
        if direction == 'down':
            blank_down = self.blank_r + 1
            if blank_down > 2:
                return False
            else: 
                down_copy = self.tiles[blank_down][self.blank_c]
                self.tiles[self.blank_r][self.blank_c] = down_copy
                self.tiles[blank_down][self.blank_c] = '0'
                self.blank_r += 1
                return True
        if direction == 'left':
            blank_left = self.blank_c - 1
            if blank_left < 0:
                return False
            else: 
                left_copy = self.tiles[self.blank_r][blank_left]
                self.tiles[self.blank_r][self.blank_c] = left_copy
                self.tiles[self.blank_r][blank_left] = '0'
                self.blank_c -= 1
                return True
        if direction == 'right':
            blank_right = self.blank_c + 1
            if blank_right > 2:
                return False
            else: 
                right_copy = self.tiles[self.blank_r][blank_right]
                self.tiles[self.blank_r][self.blank_c] = right_copy
                self.tiles[self.blank_r][blank_right] = '0'
                self.blank_c += 1
                return True
        else:
            return False

    def digit_string(self): 
        """ creates and returns a string of digits that corresponds 
        to the current contents of the called Board object’s tiles 
        attribute
        """
        s = ''
        for r in range(len(self.tiles)):
            for c in range(len(self.tiles[0])):
                s += str(self.tiles[r][c])
        return s

    def copy(self):
        """ returns a newly-constructed Board object that
        is a deep copy of the called object 
        """
        new_board = Board(self.digit_string())
        return new_board
    
    def num_misplaced(self):
        """counts and returns the number of tiles in the 
        called Board object that are not where they should 
        be in the goal state.
        """
        nums = 0 
        for r in range(len(self.tiles)):
            for c in range(len(self.tiles[0])):
                if self.tiles[r][c] != GOAL_TILES[r][c]:
                    nums += 1 
                if self.tiles[r][c] == '0':
                    nums -= 1
        return nums
    
    def __eq__(self, other):
        """can be called when the == operator is used to 
        compare two Board objects. 
        """
        if self.digit_string() == other.digit_string():
            return True
        else:
            return False
   
       
        
        