import chess as ch
import chess.polyglot as polyglot
import random as rd


class Engine:
    """
    Class for evaluating the board position and picking the best move.
    
    """

    def __init__(self, board, maxDepth, color):
        self.board = board
        self.maxDepth = maxDepth
        self.color = color

    def getBestMove(self):
        return self.engine(None, 1)
    

    def mateOpponent(self):
        if (self.board.illegal_moves.count() == 0):
            if (self.board.turn == self.color):
                return -999
            else:
                return 999
        else:
            return 0
    
    # Takes a square as input and returns a value based on the piece on that square
    def pieceValue(self, square):
        value = 0
        if(self.board.piece_type_at(square) == ch.PAWN):
            value = 1
        elif(self.board.piece_type_at(square) == ch.KNIGHT):
            value = 3.2
        elif(self.board.piece_type_at(square) == ch.BISHOP):
            value = 3.33
        elif(self.board.piece_type_at(square) == ch.ROOK):
            value = 5.1
        elif(self.board.piece_type_at(square) == ch.QUEEN):
            value = 8.8
        elif(self.board.piece_type_at(square) == ch.KING): 
            value = 100
        return value



    def opening(self):
        with polyglot.open_reader("Human.bin") as reader:
            for entry in reader.find_all(self.board):
                return entry.move

    def openning(self):
        if (self.board.fullmove_number<10):
            if (self.board.turn == self.color):
                return 1/30 * self.board.legal_moves.count()
            else:
                return -1/30 * self.board.legal_moves.count()
        else:
            return 0
        
    def evaluate(self, candidate):
        # If the game is over
        if (self.board.is_game_over()):
            return self.mateOpponent()
        else:
            # Get the value of the board position
            value = 0
            for i in self.board.piece_map():
                if (self.board.piece_at(i).color == self.color):
                    value += self.pieceValue(i)
                else:
                    value -= self.pieceValue(i)
            return value
    
    def eval(self):
        compt = 0
        for i in range(64):
            compt += self.pieceValue(i)
        compt += self.mateOpponent() + self.openning() + 0.001 * rd.random()
        return compt




    def engine(self, candidate, depth):
        if ( depth == self.maxDepth or self.board.legal_moves.count() == 0 ):
            return self.evaluate(candidate)
        else:
            #list of legal moves for current board position
            moveList = list(self.board.legal_moves)

            #initialize candidate
            newCandidate = None

            if (depth % 2 != 0):
                newCandidate = float('-inf')
            else:
                newCandidate = float('inf')
            
            for i in moveList:
                # play move i
                self.board.push(i) 
                
                # Get the value of move i
                value = self.engine(newCandidate, depth + 1)

                #Maximize Algorithm for engine
                if(value > newCandidate and depth % 2 != 0):
                    newCandidate = value
                    if (depth == 1):
                        move = i
                    #
                #Minimizing Algorithm for human player
                elif(value < newCandidate and depth % 2 == 0):
                    newCandidate = value
                #Alpha Beta Pruning
                # Previous move made by engine
                if (candidate != None and value < candidate and depth % 2 == 0):
                    self.board.pop()
                    break
                # Previous move made by human player
                elif (candidate != None and value > candidate and depth % 2 != 0):
                    self.board.pop()
                    break


        if (depth > 1): 
            # return value of node in the decision tree
            return newCandidate
        else:
            return move
