# Tic Tac Toe

import random
import time


class TicTacToe:
    def drawBoard(self, board):
        # This function prints out the board that it was passed.

        # "board" is a list of 10 strings representing the board (ignore index 0)
        print('   |   |')
        print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
        print('   |   |')

    def inputPlayerLetter(self, pref):
        # Lets the player type which letter they want to be.
        # Returns a list with the player's letter as the first item, and the computer's letter as the second.
        letter = ''
        if pref == 'c':
            while not (letter == 'X' or letter == 'O'):
                print('Do you want to be X or O?')
                letter = input().upper()

            # the first element in the tuple is the player's letter, the second is the computer's letter.
            if letter == 'X':
                return ['X', 'O']
            else:
                return ['O', 'X']
        elif pref == 'p':
            while not (letter == 'X' or letter == 'O'):
                print('Does Player 1 want to be X or O?')
                letter = input().upper()

            # the first element in the tuple is the player's letter, the second is the computer's letter.
            if letter == 'X':
                return ['X', 'O']
            else:
                return ['O', 'X']

    def whoGoesFirst(self, pref):
        # Randomly choose the player who goes first.
        if pref == 'c':
            if random.randint(0, 1) == 0:
                return 'Computer'
            else:
                return 'Player'
        else:
            if random.randint(0, 1) == 0:
                return 'Player 2'
            else:
                return 'Player 1'

    def playAgain(self):
        # This function returns True if the player wants to play again, otherwise it returns False.
        answer = 0
        while answer != 'yes' and answer != 'no' and answer != 'y' and answer != 'n':
            print('Do you want to play again? (yes or no)')
            answer = input().lower()
        return answer.startswith('y')

    def makeMove(self, board, letter, move):
        board[move] = letter

    def isWinner(self, bo, le):
        # Given a board and a player's letter, this function returns True if that player has won.
        # We use bo instead of board and le instead of letter so we don't have to type as much.
        return ((bo[7] == le and bo[8] == le and bo[9] == le) or  # across the top
                (bo[4] == le and bo[5] == le and bo[6] == le) or  # across the middle
                (bo[1] == le and bo[2] == le and bo[3] == le) or  # across the bottom
                (bo[7] == le and bo[4] == le and bo[1] == le) or  # down the left side
                (bo[8] == le and bo[5] == le and bo[2] == le) or  # down the middle
                (bo[9] == le and bo[6] == le and bo[3] == le) or  # down the right side
                (bo[7] == le and bo[5] == le and bo[3] == le) or  # diagonal
                (bo[9] == le and bo[5] == le and bo[1] == le))  # diagonal

    def getBoardCopy(self, board):
        # Make a duplicate of the board list and return it the duplicate.
        dupeBoard = []

        for i in board:
            dupeBoard.append(i)

        return dupeBoard

    def isSpaceFree(self, board, move):
        # Return true if the passed move is free on the passed board.
        return board[move] == ' '

    def getPlayerMove(self, board, pref):
        # Let the player type in his move.
        move = ' '
        while move not in '1 2 3 4 5 6 7 8 9'.split() or not self.isSpaceFree(board, int(move)):
            if pref == 'p':
                print('What is Player 1\'s move? (1-9)')
            else:
                print('What is your move? (1-9)')
            move = input()
        return int(move)

    def getPlayer2Move(self, board):
        # Let the player type in his move.
        move = ' '
        while move not in '1 2 3 4 5 6 7 8 9'.split() or not self.isSpaceFree(board, int(move)):
            print('What is Player 2\'s move? (1-9)')
            move = input()
        return int(move)

    def chooseRandomMoveFromList(self, board, movesList):
        # Returns a valid move from the passed list on the passed board.
        # Returns None if there is no valid move.
        possibleMoves = []
        for i in movesList:
            if self.isSpaceFree(board, i):
                possibleMoves.append(i)

        if len(possibleMoves) != 0:
            return random.choice(possibleMoves)
        else:
            return None

    def getComputerMove(self, board, computerLetter):
        # Given a board and the computer's letter, determine where to move and return that move.
        if computerLetter == 'X':
            playerLetter = 'O'
        else:
            playerLetter = 'X'

        # Here is our algorithm for our Tic Tac Toe AI:
        # First, check if we can win in the next move
        for i in range(1, 10):
            copy = self.getBoardCopy(board)
            if self.isSpaceFree(copy, i):
                self.makeMove(copy, computerLetter, i)
                if self.isWinner(copy, computerLetter):
                    return i

        # Check if the player could win on his next move, and block them.
        for i in range(1, 10):
            copy = self.getBoardCopy(board)
            if self.isSpaceFree(copy, i):
                self.makeMove(copy, playerLetter, i)
                if self.isWinner(copy, playerLetter):
                    return i

        # Try to take one of the corners, if they are free.
        move = self.chooseRandomMoveFromList(board, [1, 3, 7, 9])
        if move != None:
            return move

        # Try to take the center, if it is free.
        if self.isSpaceFree(board, 5):
            return 5

        # Move on one of the sides.
        return self.chooseRandomMoveFromList(board, [2, 4, 6, 8])

    def isBoardFull(self, board):
        # Return True if every space on the board has been taken. Otherwise return False.
        for i in range(1, 10):
            if self.isSpaceFree(board, i):
                return False
        return True


play = TicTacToe()

print('Welcome to Tic Tac Toe!')
print()

while True:
    # Reset the board
    theBoard = [' '] * 10
    print('Do you want to do Player VS Player (input \'p\') or Computer VS Player (input \'c\'): ', end="")
    pref = input().lower()
    if pref == 'p':
        playerLetter, player2Letter = play.inputPlayerLetter(pref)
        turn = play.whoGoesFirst(pref)
        time.sleep(0.5)
        print('The ' + turn + ' will go first.')
        gameIsPlaying = True

        while gameIsPlaying:
            if turn == 'Player 1':
                # Player 1's turn.
                play.drawBoard(theBoard)
                move = play.getPlayerMove(theBoard, pref)
                play.makeMove(theBoard, playerLetter, move)

                if play.isWinner(theBoard, playerLetter):
                    play.drawBoard(theBoard)
                    print('Hooray! Player 1 has won the game!')
                    gameIsPlaying = False
                else:
                    if play.isBoardFull(theBoard):
                        play.drawBoard(theBoard)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'Player 2'

            else:
                # Player 2's turn.
                play.drawBoard(theBoard)
                move = play.getPlayer2Move(theBoard)
                play.makeMove(theBoard, player2Letter, move)

                if play.isWinner(theBoard, player2Letter):
                    play.drawBoard(theBoard)
                    print('Hooray! Player 2 has won the game!')
                    gameIsPlaying = False
                else:
                    if play.isBoardFull(theBoard):
                        play.drawBoard(theBoard)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'Player 1'

        if not play.playAgain():
            break

    elif pref == 'c':
        playerLetter, computerLetter = play.inputPlayerLetter(pref)
        turn = play.whoGoesFirst(pref)
        time.sleep(0.5)
        print('The ' + turn + ' will go first.')
        time.sleep(0.5)
        gameIsPlaying = True

        while gameIsPlaying:
            if turn == 'Player':
                # Player's turn.
                play.drawBoard(theBoard)
                time.sleep(0.5)
                move = play.getPlayerMove(theBoard, pref)
                play.makeMove(theBoard, playerLetter, move)

                if play.isWinner(theBoard, playerLetter):
                    play.drawBoard(theBoard)
                    time.sleep(0.5)
                    print('Hooray! You have won the game!')
                    gameIsPlaying = False
                else:
                    if play.isBoardFull(theBoard):
                        play.drawBoard(theBoard)
                        time.sleep(0.5)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'Computer'

            else:
                # Computer's turn.
                move = play.getComputerMove(theBoard, computerLetter)
                play.makeMove(theBoard, computerLetter, move)

                if play.isWinner(theBoard, computerLetter):
                    play.drawBoard(theBoard)
                    time.sleep(0.5)
                    print('The computer has beaten you! You lose.')
                    gameIsPlaying = False
                else:
                    if play.isBoardFull(theBoard):
                        play.drawBoard(theBoard)
                        time.sleep(0.5)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'Player'

        if not play.playAgain():
            print("Thanks for playing!")
            break
