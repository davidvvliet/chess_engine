import os 
import math


def minimax(board, depth, turn, alpha=-math.inf, beta=math.inf):
    # Base case: if depth is 0 or game is over, return evaluation
    if depth == 0 or board.status():
        return board.eval()

    if turn:
        value = -math.inf
        for move in board.legal_moves():
            board.move(move)
            value = max(value, minimax(board, depth-1, not turn, alpha, beta))
            board.retract_move()
            alpha = max(alpha, value)
            if alpha >= beta:
                break  
        return value
    else:
        value = math.inf
        for move in board.legal_moves():
            board.move(move)
            value = min(value, minimax(board, depth-1, not turn, alpha, beta))
            board.retract_move()
            beta = min(beta, value)
            if alpha >= beta:
                break 
        return value



def find_best_move(board, depth, turn):
    best_move = None
    best_value = -math.inf if turn else math.inf
    alpha = -math.inf
    beta = math.inf

    for move in board.legal_moves():
        board.move(move)
        value = minimax(board, depth - 1, not turn, alpha, beta)
        board.retract_move()

        if turn and value > best_value:
            best_value = value
            best_move = move
            alpha = max(alpha, best_value)
        elif not turn and value < best_value:
            best_value = value
            best_move = move
            beta = min(beta, best_value)

    return best_move

