import chessboard
import sys
import random 
import argparse
from engine import find_best_move

def parse_args():
    parser = argparse.ArgumentParser(description='Play chess against an AI')
    parser.add_argument('-color', choices=['white', 'black', 'random'], 
                       default='white', help='Choose your color (default: white)')
    parser.add_argument('-depth', type=int, default=4,
                       help='AI search depth (default: 2)')
    return parser.parse_args()

def print_help():
    print("\nCommands:")
    print("  help        - Show this help message")
    print("  retract     - Take back the last two moves (yours and AI's)")
    print("  quit        - End the game")
    print("  moves       - Show all legal moves")
    print("\nEnter moves in algebraic notation (e.g., e2e4)")

def print_board(board):
    print("\nCurrent board:")
    print(board.board)

def get_legal_moves(board):
    return [move.uci() for move in board.legal_moves()]

def game():
    args = parse_args()
    board = chessboard.ChessBoard()
    
    # Set initial turn
    if args.color == 'white':
        turn = True
    elif args.color == 'black':
        turn = False
    else:  # random
        turn = random.choice([True, False])
    
    print(f"\nYou are playing as {'White' if turn else 'Black'}")
    print_help()
    print_board(board)

    while not board.status():
        if turn:
            print("\nYour turn!")
            # print(f"Legal moves: {', '.join(get_legal_moves(board))}")
            
            while True:
                move = input("\nEnter your move (or 'help' for commands): ").strip().lower()
                
                if move == 'help':
                    print_help()
                    continue
                elif move == 'quit':
                    print("Game ended by user.")
                    return
                elif move == 'moves':
                    print(f"Legal moves: {', '.join(get_legal_moves(board))}")
                    continue
                elif move == 'retract':
                    if len(board.board.move_stack) < 2:
                        print("No moves to retract!")
                        continue
                    board.retract_move()  # AI's move
                    board.retract_move()  # Your move
                    print_board(board)
                    continue
                
                try:
                    if move not in get_legal_moves(board):
                        print("Invalid move! Please enter a legal move.")
                        continue
                    
                    board.move(move)
                    print_board(board)
                    break
                except Exception as e:
                    print(f"Error: {str(e)}")
                    continue
            
            turn = not turn
            
        else:
            print("\nAI's turn...")
            try:
                best_move = find_best_move(board, args.depth, turn)
                if best_move:
                    board.move(best_move)
                    print(f"AI moved: {best_move}")
                    print_board(board)
                else:
                    print("AI couldn't find a move!")
                    break
            except Exception as e:
                print(f"AI error: {str(e)}")
                break
            
            turn = not turn
    
    # Game over
    if board.status():
        print("\nGame Over!")
        if board.board.is_checkmate():
            print(f"{'Black' if turn else 'White'} wins by checkmate!")
        elif board.board.is_stalemate():
            print("Game ended in stalemate!")
        elif board.board.is_insufficient_material():
            print("Game ended due to insufficient material!")
        elif board.board.is_seventyfive_moves():
            print("Game ended by 75-move rule!")
        elif board.board.is_fivefold_repetition():
            print("Game ended by fivefold repetition!")

if __name__ == "__main__":
    try:
        game()
    except KeyboardInterrupt:
        print("\nGame ended by user.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")