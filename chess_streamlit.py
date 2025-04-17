import streamlit as st
import chessboard
from engine import find_best_move
import chess
import sys
import time

def init_session_state():
    if 'board' not in st.session_state:
        st.session_state.board = chessboard.ChessBoard()
    if 'selected_square' not in st.session_state:
        st.session_state.selected_square = None
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'error_message' not in st.session_state:
        st.session_state.error_message = None
    if 'move_history' not in st.session_state:
        st.session_state.move_history = []
    if 'thinking' not in st.session_state:
        st.session_state.thinking = False

def get_piece_symbol(piece):
    if not piece:
        return " "
    
    symbols = {
        chess.PAWN: '♟', chess.KNIGHT: '♞', chess.BISHOP: '♝',
        chess.ROOK: '♜', chess.QUEEN: '♛', chess.KING: '♚'
    }
    
    symbol = symbols[piece.piece_type]
    return symbol if piece.color == chess.WHITE else symbol.lower()

def draw_board():
    st.title("♟ Chess AI")
    
    # Display error message if any
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
        st.session_state.error_message = None
    
    # Create two columns for board and controls
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create an 8x8 grid
        cols = st.columns(8)
        
        for row in range(8):
            for col in range(8):
                with cols[col]:
                    # Calculate square name
                    file = chr(ord('a') + col)
                    rank = str(8 - row)
                    square_name = file + rank
                    
                    try:
                        # Get piece at square
                        piece = st.session_state.board.check_piece_type(
                            chess.Square(chess.SQUARE_NAMES.index(square_name))
                        )
                        
                        # Button styling
                        button_style = """
                            <style>
                                .square-button {
                                    width: 50px;
                                    height: 50px;
                                    font-size: 24px;
                                    background-color: %s;
                                    color: %s;
                                    border: 1px solid black;
                                    border-radius: 5px;
                                    transition: all 0.3s;
                                }
                                .square-button:hover {
                                    transform: scale(1.1);
                                }
                                .selected {
                                    border: 2px solid red;
                                    box-shadow: 0 0 10px rgba(255,0,0,0.5);
                                }
                            </style>
                        """ % (
                            "#f0d9b5" if (row + col) % 2 == 0 else "#b58863",
                            "black" if piece and piece.color == chess.WHITE else "black"
                        )
                        
                        st.markdown(button_style, unsafe_allow_html=True)
                        
                        # Create button
                        if st.button(
                            get_piece_symbol(piece),
                            key=f"square_{square_name}",
                            use_container_width=True,
                            on_click=handle_square_click,
                            args=(square_name,),
                            kwargs={"style": "square-button"}
                        ):
                            pass
                    except Exception as e:
                        st.error(f"Error drawing square {square_name}: {str(e)}")
    
    with col2:
        st.header("Game Controls")
        
        # Show current game status
        if st.session_state.game_over:
            st.warning("Game Over!")
            if st.session_state.board.board.is_checkmate():
                st.success(f"{'Black' if st.session_state.board.board.turn else 'White'} wins by checkmate!")
            elif st.session_state.board.board.is_stalemate():
                st.info("Game ended in stalemate!")
        
        # Show move history
        st.subheader("Move History")
        for i, move in enumerate(st.session_state.move_history):
            st.write(f"{i+1}. {move}")
        
        # Control buttons
        if st.button("Reset Game"):
            reset_game()
        
        if st.button("Show Legal Moves"):
            show_legal_moves()
        
        if st.button("Undo Last Move"):
            undo_move()
        
        # AI thinking indicator
        if st.session_state.thinking:
            st.info("AI is thinking...")
            st.spinner()

def show_legal_moves():
    legal_moves = [move.uci() for move in st.session_state.board.legal_moves()]
    st.info(f"Legal moves: {', '.join(legal_moves)}")

def undo_move():
    if len(st.session_state.board.board.move_stack) >= 2:
        st.session_state.board.retract_move()  # AI's move
        st.session_state.board.retract_move()  # Your move
        st.session_state.move_history = st.session_state.move_history[:-2]
        st.session_state.game_over = False
        st.experimental_rerun()
    else:
        st.warning("No moves to undo!")

def reset_game():
    st.session_state.board = chessboard.ChessBoard()
    st.session_state.selected_square = None
    st.session_state.game_over = False
    st.session_state.move_history = []
    st.session_state.thinking = False
    st.experimental_rerun()

def handle_square_click(square_name):
    try:
        if st.session_state.game_over:
            return
            
        if st.session_state.selected_square is None:
            # First click - select square
            st.session_state.selected_square = square_name
        else:
            # Second click - make move
            from_square = st.session_state.selected_square
            to_square = square_name
            move = from_square + to_square
            
            try:
                # Make the move
                st.session_state.board.move(move)
                st.session_state.move_history.append(f"Player: {move}")
                
                # Let AI make its move
                if not st.session_state.board.status():
                    st.session_state.thinking = True
                    st.experimental_rerun()
                    
                    time.sleep(0.5)  # Add a small delay for visual feedback
                    ai_move = find_best_move(st.session_state.board, 4, False)
                    if ai_move:
                        st.session_state.board.move(ai_move)
                        st.session_state.move_history.append(f"AI: {ai_move}")
                    
                    st.session_state.thinking = False
                
                # Check for game over
                if st.session_state.board.status():
                    st.session_state.game_over = True
                
            except Exception as e:
                st.session_state.error_message = f"Invalid move: {str(e)}"
            
            # Reset selection
            st.session_state.selected_square = None
            
    except Exception as e:
        st.session_state.error_message = f"Error handling move: {str(e)}"

def main():
    try:
        st.set_page_config(
            page_title="Chess AI",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        # Add custom CSS
        st.markdown("""
            <style>
                .main {
                    background-color: #f5f5f5;
                }
                .stButton>button {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 5px;
                    padding: 10px 20px;
                    font-size: 16px;
                    transition: all 0.3s;
                }
                .stButton>button:hover {
                    background-color: #45a049;
                    transform: scale(1.05);
                }
            </style>
        """, unsafe_allow_html=True)
        
        init_session_state()
        draw_board()
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.stop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error running application: {str(e)}", file=sys.stderr)
        sys.exit(1) 