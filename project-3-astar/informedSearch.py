from pq import *
from search import *

class InformedProblemState(ProblemState):
    """"""
    def heuristic(self, goalState) :
        abstract()

class InformedNode(Node):
    """
    Implement this.
    """
    def __init__(self, state, parent, goalState, depth):
        super(InformedNode, self).__init__(state, parent, depth)
        self.goalState = goalState
    def priority(self):
        return self.depth + self.state.heuristic(self.goalState)

class InformedSearch(Search):
    """
    Implement this.
    """

    def __init__(self, initialState, goalState, verbose=False):
        self.uniqueStates = {}
        self.uniqueStates[initialState.dictkey()] = True
        self.q = PriorityQueue()
        self.q.enqueue(InformedNode(initialState, None, goalState, 0))
        self.goalState = goalState
        self.verbose = verbose
        self.expanded_nodes_num = 0
        solution = self.execute()
        if solution == None:
            print("Search failed")
        else:
            self.showPath(solution)


    def execute(self):
        while not self.q.empty():
            current = self.q.dequeue()
            self.expanded_nodes_num += 1
            if self.goalState.equals(current.state):
                return current
            else:
                successors = current.state.applyOperators()
                for nextState in successors:
                    n = InformedNode(nextState, current, self.goalState, current.depth + 1)
                    if nextState.dictkey() not in self.uniqueStates.keys() or self.uniqueStates[nextState.dictkey()] > n.priority():
                        self.q.enqueue(n)
                        self.uniqueStates[nextState.dictkey()] = n.priority()
                if self.verbose:
                    print("Expanded:", current)
                    print("Number of successors:", len(successors))
                    print("Expanded Nodes", self.expanded_nodes_num)
                    print("-------------------------------")

        return None



