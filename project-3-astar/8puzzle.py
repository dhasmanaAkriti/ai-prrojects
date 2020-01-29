from informedSearch import *
from search import *
from copy import deepcopy



class EightPuzzle(InformedProblemState):
    """
    This code simulates an 8 puzzle. There is blank tile. Each tile number represents
    it's corresponding position in the grid while the blank tile is represented by " ".

    """
    def __init__(self, puzzle, BlankSpacePos, operator = None):
        self.puzzle = puzzle
        self.pos = BlankSpacePos
        self.operator = operator
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
        return self.tiles_out_of_place(goalState)

    def manhattan_distance(self, goalState):
        moves_req = 0
        goalState_dict = self.utility2DtoDict(goalState.puzzle)
        len_puz = len(self.puzzle)
        breadth_puz = len(self.puzzle[0])
        for i in range(len_puz):
            for j in range(breadth_puz):
                num = self.puzzle[i][j]
                goalState_coordinates = goalState_dict[num]
                if num != " ":
                    moves_req = moves_req + abs(goalState_coordinates[0] - i) + abs(goalState_coordinates[1] - j)
        return moves_req

    def tiles_out_of_place(self, goalState):
        tiles_out_of_place = 0
        goalState_dict = self.utility2DtoDict(goalState.puzzle)
        len_puz = len(self.puzzle)
        breadth_puz = len(self.puzzle[0])
        for i in range(len_puz):
            for j in range(breadth_puz):
                num = self.puzzle[i][j]
                goalState_coordinates = goalState_dict[num]
                if num != " ":
                    if goalState_coordinates[0] != i or goalState_coordinates[1] != j:
                        tiles_out_of_place += 1
        return tiles_out_of_place

    def utility2DtoDict(self, list):
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
        newList[self.pos[0]][self.pos[1] - 1], \
        newList[self.pos[0]][self.pos[1]] =  \
            newList[self.pos[0]][self.pos[1]], \
            newList[self.pos[0]][self.pos[1] - 1]
        return EightPuzzle(newList, (self.pos[0], self.pos[1] - 1), "left")

    def moveRight(self):
        newList = deepcopy(self.puzzle)
        newList[self.pos[0]][self.pos[1] + 1], \
        newList[self.pos[0]][self.pos[1]] = \
            newList[self.pos[0]][self.pos[1]], \
            newList[self.pos[0]][self.pos[1] + 1]
        return EightPuzzle(newList, (self.pos[0], self.pos[1] + 1), "right")

    def moveUp(self):
        newList = deepcopy(self.puzzle)
        newList[self.pos[0] - 1][self.pos[1]], \
        newList[self.pos[0]][self.pos[1]] = \
            newList[self.pos[0]][self.pos[1]], \
            newList[self.pos[0] - 1][self.pos[1]]
        return EightPuzzle(newList, (self.pos[0] - 1, self.pos[1]), "up")

    def moveDown(self):
        newList = deepcopy(self.puzzle)
        newList[self.pos[0] + 1][self.pos[1]], \
        newList[self.pos[0]][self.pos[1]] = \
            newList[self.pos[0]][self.pos[1]], \
            newList[self.pos[0] + 1][self.pos[1]]
        return EightPuzzle(newList, (self.pos[0] + 1, self.pos[1]), "down")



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

if __name__ == "__main__":
    print("A")
    InformedSearch(EightPuzzle([[' ', 1, 3], [8, 2, 4], [7, 6, 5]], (0, 0)),
                   EightPuzzle([[1, 2, 3], [8, ' ', 4], [7, 6, 5]], (1, 1)), True)  #A
    print("------------------------------------------------------------------------------------------------------------")
    print("B")
    InformedSearch(EightPuzzle([[1, 3, 4], [8, 6, 2], [" ", 7, 5]], (2, 0)),
                   EightPuzzle([[1, 2, 3], [8, ' ', 4], [7, 6, 5]], (1, 1)), True)  #B
    print("------------------------------------------------------------------------------------------------------------")
    print("C")
    InformedSearch(EightPuzzle([[1, 3, " "], [4, 2, 5], [8, 7, 6]], (0, 2)),
                   EightPuzzle([[1, 2, 3], [8, ' ', 4], [7, 6, 5]], (1, 1)), True)  #C
    print("------------------------------------------------------------------------------------------------------------")
    print("D")
    InformedSearch(EightPuzzle([[7, 1, 2], [8, " ", 3], [6, 5, 4]], (1, 1)),
                   EightPuzzle([[1, 2, 3], [8, ' ', 4], [7, 6, 5]], (1, 1)), True) #D
    print("------------------------------------------------------------------------------------------------------------")
    print("E")
    InformedSearch(EightPuzzle([[8, 1, 2], [7, " ", 4], [6, 5, 3]], (1, 1)),
                  EightPuzzle([[1, 2, 3], [8, ' ', 4], [7, 6, 5]], (1, 1)), True)  #E

    print("------------------------------------------------------------------------------------------------------------")
    print("F")
    InformedSearch(EightPuzzle([[2, 6, 3], [4, " ", 5], [1, 8, 7]], (1, 1)),
                   EightPuzzle([[1, 2, 3], [8, ' ', 4], [7, 6, 5]], (1, 1)), True)  #F

    print("------------------------------------------------------------------------------------------------------------")
    print("G")
    InformedSearch(EightPuzzle([[7, 3, 4], [6, 1, 5], [8, " ", 2]], (2, 1)),
                   EightPuzzle([[1, 2, 3], [8, ' ', 4], [7, 6, 5]], (1, 1)), True)  #G

    print("------------------------------------------------------------------------------------------------------------")
    print("H")
    InformedSearch(EightPuzzle([[7, 4, 5], [6, " ", 3], [8, 1, 2]], (1, 1)),
                   EightPuzzle([[1, 2, 3], [8, ' ', 4], [7, 6, 5]], (1, 1)), True)  #H


    """
    Nodes               A*(distance)            A*(tiles)
    #A                          2                    2
    #B                          6                    7
    #C                          8                   13
    #D                         22                   38
    #E                         21                   37
    #F                         17                   96
    #G                         51                  267
    #H                        166                 2658
    """