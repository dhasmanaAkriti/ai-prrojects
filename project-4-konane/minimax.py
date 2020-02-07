from konane import *

class MinimaxNode:
    """
    Black always goes first and is considered the maximizer.
    White always goes second and is considered the minimizer.
    """
    def __init__(self, state, operator, depth, player):
        self.state = state
        self.operator = operator
        self.player = player
        self.depth = depth

class MinimaxPlayer(Konane, Player):

    def __init__(self, size, depthLimit):
        Konane.__init__(self, size)
        Player.__init__(self, size)
        self.limit = depthLimit

    def initialize(self, side):
        """
	    Initializes the player's color and name.
	    """
        self.side = side
        self.name = "MinimaxDepth" + str(self.limit) + "Dhasmana"

    def getMove(self, board):
        """
        Returns the chosen move based on doing an alphaBetaMinimax 
	    search.
        """
        alpha = float("-inf")
        beta = float("inf")
        node = MinimaxNode(board, '', 0, self)
        best_score = alphaBetaMinimax(self, node, alpha, beta)
        for s in self.successors(node):
            if s.staticEval(s) == best_score:
                return s.operator

    def staticEval(self, node):
        """
	    Returns an estimate of the value of the state associated
	    with the given node.
        """


    def successors(self, node):
        """
        Returns a list of the successor nodes for the given node.
        """
        successors = []
        new_depth = node.depth + 1
        if len(node.state.generateMoves()) == 0:
            return []
        else:
            for i in node.state.generateMoves():
                successor_board = Konane.nextBoard(node.state, Player, i)
                succesor = MinimaxNode(successor_board, i, Player, new_depth)
                successors.append(succesor)
            return successors


    def alphaBetaMinimax(self, node, alpha, beta):
        """
	    Returns the best score for the player associated with the
	    given node.  Also sets the instance variable bestMove to the
        move associated with the best score at the root node.
	    Initialize alpha to -infinity and beta to +infinity.
        """
        successors = self.successors(node)
        if successors == []:
            return self.staticEval(node)
        elif node.player == "W":
            best_score = -inf
            for s in successors:
                best_score = min(best_score, self.maxVal(s, alpha, beta))
                if best_score <= alpha:
                    return best_score
                else:
                    beta = min(beta, best_score)
            return best_score
        elif node.player == "B":
            best_score = inf
            for s in successors:
                best_score = max(best_score, self.minVal(s, alpha, beta))
                if best_score >= beta:
                    return best_score
                else:
                    alpha = max(alpha, best_score)
            return best_score