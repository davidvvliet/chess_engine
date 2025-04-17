import chess
import numpy as np
import random

class ChessBoard:

    def __init__(self, board=None):
        if board:
            self.board = board
        else:
            self.board = chess.Board()

    def fen(self):
        return self.board.fen

    def whose_turn(self):
        return self.board.turn

    def status(self):
        return self.board.is_game_over()

    def legal_moves(self):
        return list(self.board.legal_moves)

    def check_piece_type(self, square):
        return self.board.piece_at(square)
    
    def eval(self):
        
        piece_values = {
            chess.PAWN: 100,
            chess.ROOK: 500,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.QUEEN: 900,
            chess.KING: 20000
            }

        
        w_mat = 0
        b_mat = 0
        total_mat = 0 

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if not piece:
                continue
            val = piece_values[piece.piece_type]
            
            if piece.color == chess.WHITE:

                w_mat += val
                total_mat += val
            else:
                b_mat += piece_values[piece.piece_type]
                total_mat -= val

        return total_mat

    def move(self, move):
        if type(move) == str:
            move = chess.Move.from_uci(move)
    
        return self.board.push(move)

    def retract_move(self):
        return self.board.pop()

    def best_move(self):
        pass



