import random
import math

#### Othello Shell
#### P. White 2016-2018


EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'

# To refer to neighbor squares we can add a direction to a square.
N, S, E, W = -10, 10, 1, -1
NE, SE, NW, SW = N + E, S + E, N + W, S + W
DIRECTIONS = (N, NE, E, SE, E, SW, W, NW)
PLAYERS = {BLACK: "Black", WHITE: "White"}

def change(board, index, value):
    return str(board)[:index] + str(value) + str(board)[index + 1:]

########## ########## ########## ########## ########## ##########
# The strategy class for your AI
# You must implement this class
# and the method best_strategy
# Do not tamper with the init method's parameters, or best_strategy's parameters
# But you can change anything inside this you want otherwise
#############################################################

class Strategy():
    def __init__(self):
        pass

    def get_starting_board(self):
        """Create a new board with the initial black and white positions filled."""
        board = ""
        board += "?" * 10
        board += "?........?" * 8
        board += "?" * 10
        board = change(board, 44, WHITE)
        board = change(board, 55, WHITE)
        board = change(board, 45, BLACK)
        board = change(board, 54, BLACK)
        return board

    def get_pretty_board(self, board):
        """Get a string representation of the board."""
        pass

    def opponent(self, player):
        """Get player's opponent."""
        if player == WHITE:
            return BLACK
        if player == BLACK:
            return WHITE

    def find_match(self, board, player, square, direction):
        """
        Find a square that forms a match with `square` for `player` in the given
        `direction`.  Returns None if no such square exists.
        """
        #should return the index of the square or None

        pass

    def is_move_valid(self, board, player, move):
        """Is this a legal move for the player?"""
        pass

    def make_move(self, board, player, move):                                           #CODED
        """Update the board to reflect the move by the specified player."""
        # returns a new board/string
        for direction in DIRECTIONS:
            if self.find_match(board, player, move, direction) is not None:
                while board[move + direction] == self.opponent(player):
                    board = change(board, move + direction, self.opponent(player))
        return board

    def get_valid_moves(self, board, player):                                           #CODED
        """Get a list of all legal moves for player."""
        moves = []
        for square in range(11, 89):
            for direction in DIRECTIONS:
                if self.find_match(board, player, square, direction) is not None:
                    moves.append(square)
        return moves

    def has_any_valid_moves(self, board, player):
        """Can player make any moves?"""
        pass

    def next_player(self, board, prev_player):
        """Which player should move next?  Returns None if no legal moves exist."""
        pass

    def score(self, board, player=BLACK):
        """Compute player's score (number of player's pieces minus opponent's)."""
        pass

    def game_over(self, board, player):
        """Return true if player and opponent have no valid moves"""
        pass


    ### Monitoring players

    class IllegalMoveError(Exception):
        def __init__(self, player, move, board):
            self.player = player
            self.move = move
            self.board = board

        def __str__(self):
            return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)

    ################ strategies #################

    def minmax_search(self, board, player, depth):
        # determine best move for player recursively
        # it may return a move, or a search node, depending on your design
        # feel free to adjust the parameters
        pass

    def minmax_strategy(self, board, player, depth):
        # calls minmax_search
        # feel free to adjust the parameters
        # returns an integer move
        pass

    def random_strategy(self, board, player):
        return random.choice(self.get_valid_moves(board, player))

    def best_strategy(self, board, player, best_move, still_running):
        ## THIS IS the public function you must implement
        ## Run your best search in a loop and update best_move.value
        depth = 1
        while (True):
            ## doing random in a loop is pointless but it's just an example
            best_move.value = self.random_strategy(board, player)
            depth += 1

    standard_strategy = random_strategy


###############################################
# The main game-playing code
# You can probably run this without modification
################################################
import time
from multiprocessing import Value, Process
import os, signal

silent = False


#################################################
# StandardPlayer runs a single game
# it calls Strategy.standard_strategy(board, player)
#################################################
class StandardPlayer():
    def __init__(self):
        pass

    def play(self):
        ### create 2 opponent objects and one referee to play the game
        ### these could all be from separate files
        ref = Strategy()
        black = Strategy()
        white = Strategy()

        print("Playing Standard Game")
        board = ref.get_starting_board()
        player = BLACK
        strategy = {BLACK: black.standard_strategy, WHITE: white.standard_strategy}
        print(ref.get_pretty_board(board))

        while player is not None:
            move = strategy[player](board, player)
            print("Player %s chooses %i" % (player, move))
            board = ref.make_move(board, player, move)
            print(ref.get_pretty_board(board))
            player = ref.next_player(board, player)

        print("Final Score %i." % ref.score(board), end=" ")
        print("%s wins" % ("Black" if ref.score(board) > 0 else "White"))


#################################################
# ParallelPlayer simulated tournament play
# With parallel processes and time limits
# this may not work on Windows, because, Windows is lame
# This calls Strategy.best_strategy(board, player, best_shared, running)
##################################################
class ParallelPlayer():
    def __init__(self, time_limit=5):
        self.black = Strategy()
        self.white = Strategy()
        self.time_limit = time_limit

    def play(self):
        ref = Strategy()
        print("play")
        board = ref.get_starting_board()
        player = BLACK

        print("Playing Parallel Game")
        strategy = lambda who: self.black.best_strategy if who == BLACK else self.white.best_strategy
        while player is not None:
            best_shared = Value("i", -99)
            best_shared.value = -99
            running = Value("i", 1)

            p = Process(target=strategy(player), args=(board, player, best_shared, running))
            # start the subprocess
            t1 = time.time()
            p.start()
            # run the subprocess for time_limit
            p.join(self.time_limit)
            # warn that we're about to stop and wait
            running.value = 0
            time.sleep(0.01)
            # kill the process
            p.terminate()
            time.sleep(0.01)
            # really REALLY kill the process
            if p.is_alive(): os.kill(p.pid, signal.SIGKILL)
            # see the best move it found
            move = best_shared.value
            if not silent: print("move = %i , time = %4.2f" % (move, time.time() - t1))
            if not silent: print(board, ref.get_valid_moves(board, player))
            # make the move
            board = ref.make_move(board, player, move)
            if not silent: print(ref.get_pretty_board(board))
            player = ref.next_player(board, player)

        print("Final Score %i." % ref.score(board), end=" ")
        print("%s wins" % ("Black" if ref.score(board) > 0 else "White"))


if __name__ == "__main__":
    # game =  ParallelPlayer(0.1)
    game = StandardPlayer()
    game.play()
