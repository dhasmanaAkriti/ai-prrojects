from updatedKonane import *
import math

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
        Player.__init__(self)
        self.limit = depthLimit

    def initialize(self, side):
        """
	    Initializes the player's color and name.
	    """
        self.side = side
        self.name = "MinimaxDepth" + str(self.limit) + "Dhasmana"

    @timed_out(3)
    def getMove(self, board):
        """
        Returns the chosen move based on doing an alphaBetaMinimax 
	    search.
        """

        alpha = float("-inf")
        beta = float("inf")
        node = MinimaxNode(board, [], 0, self.side)
        self.best_move = []
        best_score = self.alphaBetaMinimax(node, alpha, beta)
        return self.best_move



    def staticEval(self, node):
        """
	    Returns an estimate of the value of the state associated
	    with the given node.
        """
        # moves_me = len(self.generateMoves(node.state, node.player))
        moves_opponent = len(self.generateMoves(node.state, self.opponent(node.player)))
        # return  moves_me - moves_opponent
        return self.countSymbol(node.state, self.side) - self.countSymbol(node.state, self.opponent(self.side)) - moves_opponent




    def successors(self, node):
        """
        Returns a list of the successor nodes for the given node.
        """
        successors = []
        new_depth = node.depth + 1
        moves = self.generateMoves(node.state, node.player)
        if len(moves) == 0:
            return []
        else:
            for move in moves:
                #print(move)
                #print(moves)
                #print(node.state)
                successor_board = self.nextBoard(node.state, node.player, move)
                successor = MinimaxNode(successor_board, move, new_depth, self.opponent(node.player))
                successors.append(successor)
            return successors


    def alphaBetaMinimax(self, node, alpha, beta):
        """
	    Returns the best score for the player associated with the
	    given node.  Also sets the instance variable bestMove to the
        move associated with the best score at the root node.
	    Initialize alpha to -infinity and beta to +infinity.
        """
        successors = self.successors(node)
        if successors == [] or node.depth == self.limit:
            #self.best_move = node.operator
            return self.staticEval(node)
        elif node.player == self.side:
            best_score = -math.inf
            for s in successors:
                best_score = min(best_score, self.alphaBetaMinimax(s, alpha, beta))
                if best_score <= alpha:
                    self.best_move = s.operator
                    return best_score
                else:
                    beta = min(beta, best_score)
            return best_score
        else:
            best_score = math.inf
            for s in successors:
                best_score = max(best_score, self.alphaBetaMinimax(s, alpha, beta))
                if best_score >= beta:
                    self.best_move = s.operator
                    return best_score
                else:
                    alpha = max(alpha, best_score)
            return best_score

if __name__ == '__main__':
    game = Konane(8)
    game.playNGames(100, MinimaxPlayer(8, 2), MinimaxPlayer(8, 1), False)
    game.playNGames(100, MinimaxPlayer(8, 6), SimplePlayer(8), False)
    game.playNGames(100, MinimaxPlayer(8, 6), RandomPlayer(8), False)
