# prints a simple tic tac toe game in the console
def print_board(board):
    print("\n")
    print(" {} | {} | {} ".format(board[0], board[1], board[2]))
    print("---+---+---")
    print(" {} | {} | {} ".format(board[3], board[4], board[5]))
    print("---+---+---")
    print(" {} | {} | {} ".format(board[6], board[7], board[8]))
    print("\n")

# A function to check if a player has won the game
def check_win(board, player):
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # horizontal wins
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # vertical wins
        (0, 4, 8), (2, 4, 6)              # diagonal wins
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

# A function to check if the game is a tie
def check_tie(board):
    return all(spot in ['X', 'O'] for spot in board)

# Main function to run the Tic Tac Toe game
def tic_tac_toe():
    board = [str(i) for i in range(1, 10)]
    current_player = 'X'
    game_running = True

    while game_running:
        print_board(board)
        try:
            move = int(input(f"Player {current_player}, choose a spot (1-9): "))
        except ValueError:
            print("Please enter a valid number from 1 to 9.")
            continue
        except (EOFError, KeyboardInterrupt):
            print("\nInput interrupted. Exiting the game.")
            break

        # Validate move
        if move < 1 or move > 9:
            print("Invalid move. Select a number from 1 to 9.")
            continue
        if board[move - 1] in ['X', 'O']:
            print("Spot already taken. Try a different one.")
            continue

        # Place player's move on the board
        board[move - 1] = current_player

        # Check for a win or a tie
        if check_win(board, current_player):
            print_board(board)
            print(f"Congratulations! Player {current_player} wins!")    
            game_running = False
        elif check_tie(board):
            print_board(board)
            print("It's a tie!")
            game_running = False
        else:
            # Switch players
            current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    tic_tac_toe()