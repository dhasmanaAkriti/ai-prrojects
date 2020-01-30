from informedSearch import *
from search import *
from copy import deepcopy



class EightPuzzle(InformedProblemState):
    """
    This code simulates an 8 puzzle as a 2 dimensional list. There is blank tile. Each tile number represents
    it's corresponding position in the grid while the blank tile is represented by " ".

    """
    def __init__(self, puzzle, BlankSpacePos,  heur = 0, operator = None):
        self.puzzle = puzzle
        self.pos = BlankSpacePos
        self.operator = operator
        self.heur = heur
    def __str__(self):
        """
        Required method for use with the Search class.
        Returns a string representation of the state.
        """
        result = ""
        if self.operator is not None:
            result += "Operator: " + self.operator + "\n"
        result += str(self.puzzle) # "," + str(self.pos)
        return result
    def equals(self, state):
        """
        Required method for use with the Search class.
        Determines whether the state instance and the given
        state are equal.
        """
        return self.puzzle == state.puzzle

    def heuristic(self, goalState):
        if self.heur == 0:
            return self.manhattan_distance(goalState)    #Select heuristic here
        else:
            return self.tiles_out_of_place(goalState)

    def manhattan_distance(self, goalState):
        moves_req = 0
        puz_dict = self.utility2DtoDict(self.puzzle)
        goalState_dict = self.utility2DtoDict(goalState.puzzle)
        for num in puz_dict:
            if num != " ":
                moves_req = moves_req + abs(goalState_dict[num][0] - puz_dict[num][0]) + \
                            abs(goalState_dict[num][1] - puz_dict[num][1])
        return moves_req

    def tiles_out_of_place(self, goalState):
        tiles_out_of_place = 0
        puz_dict = self.utility2DtoDict(self.puzzle)
        goalState_dict = self.utility2DtoDict(goalState.puzzle)
        for num in goalState_dict:
            if num != " ":
                if goalState_dict[num] != puz_dict[num]:
                        tiles_out_of_place += 1
        return tiles_out_of_place

    def utility2DtoDict(self, list):
        """
        Converts a 2D list into a dictionary with each element mapping to a tuple of its coordinates.
        :param list:
        :return:
        """
        d = dict()
        for i in enumerate(list):
            for j in enumerate(i[1]):
                d[j[1]] = (i[0], j[0])

        return d

    def dictkey(self):
        """
        Required method for use with the Search class.
        Returns a string that can be used as a ditionary key to
        represent unique states.
        """
        return str(self.puzzle)

    def moveLeft(self):
        newList = deepcopy(self.puzzle)
        x_pos = self.pos[0]
        y_pos = self.pos[1]
        newList[x_pos][y_pos - 1], \
        newList[x_pos][y_pos] =  \
            newList[x_pos][y_pos], \
            newList[x_pos][y_pos - 1]
        return EightPuzzle(newList, (x_pos, y_pos - 1), self.heur, "left")

    def moveRight(self):
        newList = deepcopy(self.puzzle)
        x_pos = self.pos[0]
        y_pos = self.pos[1]
        
        newList[x_pos][y_pos + 1], \
        newList[x_pos][y_pos] = \
            newList[x_pos][y_pos], \
            newList[x_pos][y_pos + 1]
        return EightPuzzle(newList, (x_pos, y_pos + 1), self.heur, "right")

    def moveUp(self):
        newList = deepcopy(self.puzzle)
        x_pos = self.pos[0]
        y_pos = self.pos[1]

        newList[x_pos - 1][y_pos], \
        newList[x_pos][y_pos] = \
            newList[x_pos][y_pos], \
            newList[x_pos - 1][y_pos]
        return EightPuzzle(newList, (x_pos - 1, y_pos), self.heur, "up")

    def moveDown(self):
        newList = deepcopy(self.puzzle)
        x_pos = self.pos[0]
        y_pos = self.pos[1]

        newList[x_pos + 1][y_pos], \
        newList[x_pos][y_pos] = \
            newList[x_pos][y_pos], \
            newList[x_pos + 1][y_pos]
        return EightPuzzle(newList, (x_pos + 1, y_pos), self.heur, "down")



    def applyOperators(self):
        """
        Required method for use with the Search class.
        Returns a list of valid successors to the current state
        Logic:
        0<=#m<=#c on both left and right sides.

        """
        successors = []
        puz_len = len(self.puzzle) - 1
        y_pos = self.pos[0]
        x_pos = self.pos[1]
        if y_pos != 0:
            successors.append(self.moveUp())
        if x_pos != puz_len:
            successors.append(self.moveRight())
        if y_pos != puz_len:
            successors.append(self.moveDown())
        if x_pos != 0:
            successors.append(self.moveLeft())
        return successors


"""
   Puzzle              A*(tiles)              A*(distance)
A           |          3            |          3
B           |          8            |          7
C           |          14            |          9
D           |          39            |          23
E           |          39            |          22
F           |          98            |          18
G           |          268            |          52
H           |          2664            |          167
"""