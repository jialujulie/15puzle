"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code
        boolean = True
        
        if self.get_number(target_row, target_col) != 0:
            boolean = False
        
        for row in range(target_row+1, self._height):
            for col in range(self._width):
                if self.current_position(row, col) != (row, col):
                    boolean = False
        
        for col in range(target_col+1, self._width):
            if self.current_position(target_row, col) != (target_row,col):
                boolean = False
                
        return boolean

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # replace with your code
        # 1. place "0" at the current position of the target tile
        # 2. and move the target tile horizontally to target col
        
        assert self.lower_row_invariant(target_row,target_col), "lower row invariant does not hold before solve interior"
        
        move_string = ""
        
        correcttile_pos = self.current_position(target_row, target_col)
        
        print "solve position:",target_row,target_col,"where is correct tile?",correcttile_pos
        distance_ver = target_row - correcttile_pos[0] 
        distance_hor = target_col - correcttile_pos[1]
        
    
        
        if distance_hor < 0:
            if correcttile_pos[0] == 0:
                move_string += "u"*(distance_ver-1)
                move_string += "r"*(-distance_hor) +"uld"
                #start recurring horizontal cyclic movement
                move_string += "rulld"*(-distance_hor)

            else:
                move_string += "u"*distance_ver
                move_string += "r"*(-distance_hor) +"ulld"
                #start recurring horizontal cyclic movement
                move_string += "rulld"*(-distance_hor-1)
            
        elif distance_hor == 0:
            move_string += "u"*distance_ver
            move_string += "ld"
                
        else: 
                
            move_string += "l"*(distance_hor)
            
            if distance_ver >0:
                move_string += "u"*distance_ver+"rdl"
            #start recurring horizontal cyclic movement
            move_string += "urrdl"*(distance_hor-1)
        
        
            
        # 3. move tile down vertically to target row
        #if correcttile_pos[0] == 0 and distance_hor <0:
        move_string += "druld"*(distance_ver-1)
        #else:
            #move_string += "druld"*distance_ver
        
        
        # update puzzle
        self.update_puzzle(move_string)
        
        assert self.lower_row_invariant(target_row,target_col-1), "lower row invariant does not hold after solve interior"

        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert self.lower_row_invariant(target_row,0), "lower row invariant does not hold before solve interior"
        
        move_string = ""
        
        correcttile_pos = self.current_position(target_row, 0)
        
        print "col0 correct tile pos", correcttile_pos
        distance_ver = target_row - correcttile_pos[0] 
        distance_hor = 0 - correcttile_pos[1]        
        
        move_string += "ur"
        if correcttile_pos == (target_row-1,0):
            move_string += "r"*(self.get_width()-2)
            #return move_string
        
        else:
            if correcttile_pos == (target_row-1,1) or correcttile_pos[1] == 0:
                move_string +="u"*(distance_ver-1)
                move_string += "l" +"druld"*(distance_ver-1)
            
            elif correcttile_pos[1]>1:
                move_string += "u"*(distance_ver-1)

                if correcttile_pos[0] == 0:
                    move_string += "r"*(-distance_hor-1) +"dllu"
                    #start recurring horizontal cyclic movement
                    move_string += "rdllu"*(-distance_hor-2)

                else:
                    move_string += "r"*(-distance_hor-1) +"ulld"
                    #start recurring horizontal cyclic movement
                    move_string += "rulld"*(-distance_hor-2) 
                
                move_string += "druld"*(distance_ver -1)
            else:
                move_string +="u"*(distance_ver-1)
                move_string +="ld" +"druld"*(distance_ver-2)
            

            # adding the fixed move string 
            move_string += "ruldrdlurdluurddlur"
            #move 0 to end of row
            move_string += "r"*(self.get_width()-2)
        
        # update puzzle
        self.update_puzzle(move_string)
        
        assert self.lower_row_invariant(target_row-1,self.get_width()-1), "lower row invariant does not hold after solve interior"

        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        boolean = True
        
        if self.get_number(0, target_col) != 0:
            boolean = False
        
        for row in range(2, self._height):
            for col in range(self._width):
                if self.current_position(row, col) != (row, col):
                    boolean = False
        
        for col in range(target_col+1, self._width):
            for row in range(2):
                if self.current_position(row, col) != (row,col):
                    boolean = False
         
        if self.current_position(1,target_col)!= (1, target_col):
            boolean = False
            
        return boolean         

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        boolean = True
        
        if self.get_number(1, target_col) != 0:
            boolean = False
        
        for row in range(2, self._height):
            for col in range(self._width):
                if self.current_position(row, col) != (row, col):
                    boolean = False
        
        for col in range(target_col+1, self._width):
            for row in range(2):
                if self.current_position(row, col) != (row,col):
                    boolean = False
                
        return boolean        

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert self.row0_invariant(target_col), "row0_invariant does not hold before solve row0 tile"
        
        move_string = ""
        
        correcttile_pos = self.current_position(0,target_col)
                
        #distance_ver = 0 - correcttile_pos[0] 
        distance_hor = target_col - correcttile_pos[1]        
        
        move_string += "ld"
        if correcttile_pos == (0,target_col-1):
            pass
        
        else:
            if correcttile_pos == (1,target_col-1) or correcttile_pos[0] == 0:
                move_string +="l"*(distance_hor-1)
                move_string += "u" +"rdlur"*(distance_hor-1)
                move_string += "ld"
                
#            elif correcttile_pos[0]>1:
#                move_string += "u"*(distance_ver-1)
#
#                if correcttile_pos[0] == 0:
#                    move_string += "r"*(-distance_hor-1) +"dllu"
#                    #start recurring horizontal cyclic movement
#                    move_string += "rdllu"*(-distance_hor-2)
#
#                else:
#                    move_string += "r"*(-distance_hor-1) +"ulld"
#                    #start recurring horizontal cyclic movement
#                    move_string += "rulld"*(-distance_hor-2) 
#                
#                move_string += "druld"*(distance_ver -1)
            else:
                move_string +="l"*(distance_hor-1)
                move_string +="urrdl"*(distance_hor-2)
            

            # adding the fixed move string 
            move_string += "urdlurrdluldrruld"
            #move 0 to end of row
            #move_string += "r"*(self.get_width()-2)
        
        # update puzzle
        self.update_puzzle(move_string)
        
        assert self.row1_invariant(target_col-1), "row1 invariant does not hold after solve row0 tile"
        
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert self.row1_invariant(target_col), "row1 invariant does not hold before solve row1"
        
        move_string = ""
        
        correcttile_pos = self.current_position(1, target_col)
        
        #print correcttile_pos
        distance_ver = 1 - correcttile_pos[0] 
        distance_hor = target_col - correcttile_pos[1]
        
    
        
        if distance_hor < 0:
            if correcttile_pos[0] == 0:
                move_string += "u"*(distance_ver-1)
                move_string += "r"*(-distance_hor) +"uld"
                #start recurring horizontal cyclic movement
                move_string += "rulld"*(-distance_hor)

            else:
                move_string += "u"*distance_ver
                move_string += "r"*(-distance_hor) +"ulld"
                #start recurring horizontal cyclic movement
                move_string += "rulld"*(-distance_hor-1)
            
        elif distance_hor == 0:
            move_string += "u"*distance_ver
            move_string += "ld"
                
        else: 
                
            move_string += "l"*(distance_hor)
            
            if distance_ver >0:
                move_string += "u"*distance_ver+"rdl"
            #start recurring horizontal cyclic movement
            move_string += "urrdl"*(distance_hor-1)
        
        
            
        # 3. move tile down vertically to target row
        #if correcttile_pos[0] == 0 and distance_hor <0:
        move_string += "druld"*(distance_ver-1)
        #else:
            #move_string += "druld"*distance_ver
        move_string += "ur"
        
        # update puzzle
        self.update_puzzle(move_string)
        
        assert self.row0_invariant(target_col), "row0 does not hold after solve row1 tile"

        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        move_string = ""
        move_string += "lu"
        number_1 = self.get_number(0,1)
        number_2 = self.get_number(0,0)
        number_3 = self.get_number(1,0)
        
        if number_1 == 1 and number_2 < number_3:
            pass
        elif number_2 == 1 and number_1 > number_3:
            move_string += "rdlu"*2
        elif number_3 ==1 and number_1 < number_2:
            move_string +="rdlu"
        
        self.update_puzzle(move_string)
        
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        boolean = True
        for row in range(self._height):
            for col in range(self._width):
                if self.current_position(row, col) != (row, col):
                    boolean = False
                    break
        
        if boolean == True:
            return ""
        
        string = ""
        string0 = (self._width-1-self.current_position(0,0)[1])*"r" + \
                  (self._height-1-self.current_position(0,0)[0])*"d"
        
        self.update_puzzle(string0)
        print "0",self.current_position(0,0), string0
        
        for row in range(self._height-1,1,-1):
            for col in range(self._width-1,-1,-1):
                print "fix positon:", row,col
                if col == 0:
                    string += self.solve_col0_tile(row)
                else:
                    string += self.solve_interior_tile(row, col)
        
        for col in range(self._width-1,1,-1):
            print "fix positon:", col

            string += self.solve_row1_tile(col)
            print "fixed row 1", self
            string += self.solve_row0_tile(col)
            
            print "fixed row 0", self

        string += self.solve_2x2()
        
        print "fixed row 2x2", self

        
        #self.update_puzzle(string)
        
        return string0+string


    
#testpuzzle = Puzzle(3, 2, [[1, 4], [2,3], [0,5]])
#testpuzzle = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#print testpuzzle.solve_puzzle()

# Start interactive simulation

poc_fifteen_gui.FifteenGUI(Puzzle(2, 2))


