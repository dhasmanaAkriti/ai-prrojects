### File: missionary.py
### Implements the missionaries and cannibals problem for state
### space search

from search import *
from improvedSearch import *

class MissionaryState(ProblemState):
    """
    Three missionaries and three cannibals are on one side of the river,
    along with a boat that can hold one or two people. Find a way to get everyone to the other side of the river,
    without ever leaving a group of cannibals on one side of the river that are outnumbered by the missionaries
    (lest they become converted).

    The left and right side are denoted by tuples with (missionaries, #cannibals, 0/1 depending on whether the boat
    is there or not)
    """
    def __init__(self, LeftSide, RightSide, operator = None):
        self.l = LeftSide
        self.r = RightSide
        self.operator = operator
    def __str__(self):
        """
        Required method for use with the Search class.
        Returns a string representation of the state.
        """
        result = ""
        if self.operator is not None:
            result += "Operator: " + self.operator + "\n"
        result += str(self.l) + "," + str(self.r)
        return result
    def equals(self, state):
        """
        Required method for use with the Search class.
        Determines whether the state instance and the given
        state are equal.
        """
        return self.l == state.l and self.r == state.r
    def dictkey(self):
        """
        Required method for use with the Search class.
        Returns a string that can be used as a ditionary key to
        represent unique states.
        """
        return str(self.l) + "," + str(self.r)
    def leavesC1(self):
        newL = (self.l[0], self.l[1] - 1, 0)
        newR = (self.r[0], self.r[1] + 1, 1)
        return MissionaryState(newL, newR, "1 Cannibal leaves")

    def leavesM1(self):
        newL = (self.l[0] - 1, self.l[1], 0)
        newR = (self.r[0] + 1, self.r[1], 1)
        return MissionaryState(newL, newR, "1 Missionary leaves")


    def leavesM1C1(self):
        newL = (self.l[0] - 1, self.l[1] - 1, 0)
        newR = (self.r[0] + 1, self.r[1] + 1, 1)
        return MissionaryState(newL, newR, "1 Cannibal and 1 Missionary leave")


    def leavesM2(self):
          # reduces no. of missionaries on left by one.
        newL = (self.l[0] - 2, self.l[1], 0)
        newR = (self.r[0] + 2, self.r[1], 1)
        return MissionaryState(newL, newR, "2 missionaries leave")

    def leavesC2(self):
        newL = (self.l[0], self.l[1] - 2, 0)
        newR = (self.r[0], self.r[1] + 2, 1)
        return MissionaryState(newL, newR, "2 Cannibals leave")

    def comesbackC1(self):
        newL = (self.l[0], self.l[1] + 1, 1)
        newR = (self.r[0], self.r[1] - 1, 0)
        return MissionaryState(newL, newR, "1 Cannibal comes back")
    def comesbackM1(self):
            newL = (self.l[0] + 1, self.l[1], 1)
            newR = (self.r[0] - 1, self.r[1], 0)
            return MissionaryState(newL, newR, "1 Missionary comes back")
    def comesbackC1M1(self):
            newL = (self.l[0] + 1, self.l[1] + 1, 1)
            newR = (self.r[0] - 1, self.r[1] - 1, 0)
            return MissionaryState(newL, newR, "1 Cannibal and 1 Missionary come back")

    def comesbackC2(self):
            newL = (self.l[0], self.l[1] + 2, 1)
            newR = (self.r[0], self.r[1] - 2, 0)
            return MissionaryState(newL, newR, "2 Cannibals come back")

    def comesbackM2(self):
            newL = (self.l[0] + 2, self.l[1], 1)
            newR = (self.r[0] - 2, self.r[1], 0)
            return MissionaryState(newL, newR, "2 Missionaries come back")

    def applyOperators(self):
        """
        Required method for use with the Search class.
        Returns a list of valid successors to the current state
        Logic:
        0<=#m<=#c on both left and right sides.

        """
        successors = []
        l_m = self.l[0]  # no. of missionaries on the left side
        l_c = self.l[1]  #no. of cannibals on the left side
        r_m = self.r[0]  #no. of missionaries on the right side
        r_c = self.r[1]  #no. of cannibals on the right side
        if (l_c - 1 >= 0) and (l_c - 1 >= l_m) and (self.l[2] == 1):
            successors.append(self.leavesC1())
        if l_m - 1 >= 0 and r_m + 1 <= r_c and self.l[2] == 1:
            successors.append(self.leavesM1())
        if l_m - 1 >= 0 and l_c - 1 >= 0 and self.l[2] == 1:
            successors.append(self.leavesM1C1())
        if l_c - 2 >= 0 and l_c - 2 >= l_m and self.l[2] == 1:
            successors.append(self.leavesC2())
        if l_m - 2 >= 0 and r_m - 2 <= r_c and self.l[2] == 1:
            successors.append(self.leavesM2())
        if r_c - 1 >= 0 and r_c - 1 >= r_m and self.r[2] == 1:
            successors.append(self.comesbackC1())
        if r_m - 1 >= 0 and l_m + 1 <= l_c and self.r[2] == 1:
            successors.append(self.comesbackM1())
        if r_m - 1 >= 0 and r_c - 1 >= 0 and self.r[2] == 1 and self.r:
            successors.append(self.comesbackC1M1())
        if r_c - 2 >= 0 and r_c - 2 >= r_m and self.r[2] == 1:
            successors.append(self.comesbackC2())
        if r_m - 2 >= 0 and l_m + 2 <= l_c and self.r[2] == 1:
            successors.append(self.comesbackM2())
        return successors

improvedSearch(MissionaryState((3, 3, 1), (0, 0, 0)), MissionaryState((0, 0, 0), (3, 3, 1)), True)

