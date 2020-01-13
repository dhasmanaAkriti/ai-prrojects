import random
# tic-tac-toe.py
# TIC TAC TOE, computer vs user.No technique employed by the computer.

# Author: Akriti Dhasmana


# Initialize Game State
def playGame():
    N = 3  # Takes input for the dimensions of the board.
    # Provides a list for the game board.
    board = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(" ")
        board.append(row)
    print("You are X.")
    human_player = "X"  # Sets the string to be added to the board depending on the player.
    eliza_player = "O"
    current_player = human_player
    X_won = False  # Sets a boolean variable for checking whether player X won.
    O_won = False  # Sets a boolean variable for checking whether player Y won.
    game_over = False  # Sets a boolean variable for checking whether the game is over.
    turn = 0  # Initiates the variable turn to keep track of the number of turns as 0.

    # Main Game Loop
    while (not (X_won or O_won) and turn < N ** 2):

        turn = turn + 1

        # VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
        # Display Game
        def Display_Game():
            """Displays the game board by iterating through the list to print Xs and Os"""
            for row_index in range(N):  # Iterates through the list to access each nested list
                for col_index in range(N):  # Defines iterable i to
                    print(board[row_index][col_index], end='')
                    if col_index != N - 1:
                        print('|', end='')
                print()
                if row_index != N - 1:
                    for i in range(N - 1):
                        print('-+', end='')
                    print('-')

        Display_Game()

        # Get Input
        # Primed input, like rejection sampling & input validation.
        if(current_player == human_player):
            print("It's your turn, enter your move!")
            row = int(input('  Enter a row (1-' + str(N) + '): '))
            col = int(input('  Enter a col (1-' + str(N) + '): '))

            while (row > N or row < 1 or col > N or col < 1 or board[row - 1][col - 1] != " "):
                print('Invalid input!  Try again.')
                row = int(input('  Enter a row (1-' + str(N) + '): '))
                col = int(input('  Enter a col (1-' + str(N) + '): '))
        else:
            print("Hmmm... It's my turn, let me think!")
            row = random.randint(1, N)
            col = random.randint(1, N)
            while (row > N or row < 1 or col > N or col < 1 or board[row - 1][col - 1] != " "):
                row = random.randint(1, N)
                col = random.randint(1, N)

        # Update Game
        # 1. Make move
        board[row - 1][col - 1] = current_player
        # Displays board after the move

        # VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
        # 2. Check winner
        X_win_con = []  # Defines the condition for winning for X
        O_win_con = []  # Defines the condition for winning for O
        for i in range(N):
            X_win_con.append('X')
            O_win_con.append('O')

        for row_index in range(N):  # Iterates through the number of rows.
            if board[row_index] == X_win_con:  # Checks if the row is full of Xs.
                X_won = True
                break
            elif board[row_index] == O_win_con:  # Checks if the row is full of Os.
                O_won = True
                break
            else:
                col = []  # Creates an empty list col
                for col_index in range(N):
                    col.append(board[col_index][
                                   row_index])  # Interchanges col_index and row_index to form a list of all elements in a column.
                if col == O_win_con:  # Checks if the column is full of Os.
                    O_won = True
                    break
                elif col == X_win_con:  # Checks if the column is full of Xs.
                    X_won = True
                    break

        dia1 = []
        dia2 = []
        for row_index in range(N):
            dia1.append(board[row_index][row_index])
            if (dia1 == O_win_con):  # Checks if diagonal1 is full of Os.
                O_won = True
                break
            elif (dia1 == X_win_con):  # Checks if diagonal1 is full of Xs.
                X_won = True
                break
        for row_index in range(N):
            dia2.append(board[row_index][N - 1 - row_index])
            if (dia2 == O_win_con):  # Checks if diagonal2 is full of Os.
                O_won = True
                break
            elif (dia2 == X_win_con):  # Checks if diagonal2 is full of Xs.
                X_won = True
                break

        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        # 3. Change player
        if (current_player == "X"):
            current_player = "O"
        else:
            current_player = "X"

    # Game result after the game loop ends.
    Display_Game()
    if (X_won):
        print("You won! Wow, you are really smart!")
    elif (O_won):
        print("I won! Better luck next time!")
    else:
        print('It is a draw. We are equally intelligent.')



