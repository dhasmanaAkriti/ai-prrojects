### File pitcher.py
### Implements the water pitcher puzzle for state space search

from search import *

class PitcherState(ProblemState):
    """
    The water pitcher puzzle: Suppose that you are given a 3 quart
    pitcher and a 4 quart pitcher.  Either pitcher can be filled
    from a faucet.  The contents of either pitcher can be poured
    down a drain.  Water may be poured from one pitcher to the other.
    When pouring, as soon as the pitcher being poured into is full,
    the pouring stops.  There is no additional measuring device and
    and the pitchers have no markings to show partial quantities.

    Each operator returns a new instance of this class representing
    the successor state.  
    """
    def __init__(self, q3, q4, operator = None):
        self.q3 = q3
        self.q4 = q4
        self.operator = operator
    def __str__(self):
        """
        Required method for use with the Search class.
        Returns a string representation of the state.
        """
        result = ""
        if self.operator is not None:
            result += "Operator: " + self.operator + "\n"
        result += str(self.q3) + "," + str(self.q4)
        return result
    def equals(self, state):
        """
        Required method for use with the Search class.
        Determines whether the state instance and the given
        state are equal.
        """
        return self.q3==state.q3 and self.q4==state.q4
    def dictkey(self):
        """
        Required method for use with the Search class.
        Returns a string that can be used as a ditionary key to
        represent unique states.
        """
        return str(self.q3) + "," + str(self.q4)
    def fillq3(self):
        return PitcherState(3, self.q4, "fillq3")
    def fillq4(self):
        return PitcherState(self.q3, 4, "fillq4")
    def drainq3(self):
        return PitcherState(0, self.q4, "drainq3")
    def drainq4(self):
        return PitcherState(self.q3, 0, "drainq4")
    def pourq3Toq4(self):
        capacity = 4 - self.q4
        if self.q3 > capacity:
            return PitcherState(self.q3-capacity, 4, "pourq3Toq4")
        else:
            return PitcherState(0, self.q4 + self.q3, "pourq3Toq4")
    def pourq4Toq3(self):
        capacity = 3 - self.q3
        if self.q4 > capacity:
            return PitcherState(3, self.q4-capacity, "pourq4Toq3")
        else:
            return PitcherState(self.q3 + self.q4, 0, "pourq4Toq3")
    def applyOperators(self):
        """
        Required method for use with the Search class.
        Returns a list of valid successors to the current state
        """
        return [self.fillq3(), self.fillq4(),
                self.drainq3(), self.drainq4(),
                self.pourq3Toq4(), self.pourq4Toq3()]

Search(PitcherState(0,0), PitcherState(0,2))
#Search(PitcherState(0,0), PitcherState(1,0), True) # verbose on
    
