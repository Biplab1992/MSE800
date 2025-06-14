import random

def display_board(board):
    """Display the current board state."""
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def check_win(board, player):
    """Return True if the player has a winning combination."""
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6)              # diagonals
    ]
    return any(board[a] == board[b] == board[c] == player for a, b, c in win_conditions)

def check_tie(board):
    """Return True if the board is full and there is no winner."""
    return all(spot in ['X', 'O'] for spot in board)

def get_player_move(board):
    """Prompt the player until a valid move is entered."""
    while True:
        try:
            move = int(input("Your move (choose a number 1-9): "))
            if move < 1 or move > 9:
                print("Invalid move! Please choose a number between 1 and 9.")
            elif board[move - 1] in ['X', 'O']:
                print("That spot is already taken. Try another one.")
            else:
                return move
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 9.")

def get_computer_move(board):
    """Randomly choose and return a valid move (spot number) for the computer."""
    available_moves = [i + 1 for i, spot in enumerate(board) if spot not in ['X', 'O']]
    return random.choice(available_moves)

def tic_tac_toe_single_player():
    """
    Main game loop for single-player Tic Tac Toe.
    
    - The human player is 'X' and always starts.
    - The computer is 'O' and picks moves randomly.
    """
    board = [str(i) for i in range(1, 10)]
    human, computer = 'X', 'O'
    current_player = human  # Human goes first

    while True:
        display_board(board)
        
        if current_player == human:
            move = get_player_move(board)
        else:
            move = get_computer_move(board)
            print(f"Computer chooses: {move}")
        
        board[move - 1] = current_player
        
        if check_win(board, current_player):
            display_board(board)
            if current_player == human:
                print("Congratulations! You beat the computer!")
            else:
                print("Sorry, the computer wins!")
            break
        
        if check_tie(board):
            display_board(board)
            print("It's a tie!")
            break
        
        # Switch turns: if human then computer, and vice versa.
        current_player = computer if current_player == human else human

if __name__ == "__main__":
    tic_tac_toe_single_player()