# Jan 12, 0952 version

import random
import math

#### Othello Shell
#### P. White 2016-2018


EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'

# To refer to neighbor squares we can add a direction to a square.
N, S, E, W = -10, 10, 1, -1
NE, SE, NW, SW = N + E, S + E, N + W, S + W
DIRECTIONS = (N, NE, E, SE, S, SW, W, NW)
PLAYERS = {BLACK: "Black", WHITE: "White"}


########## ########## ########## ########## ########## ##########
# The strategy class for your AI
# You must implement this class
# and the method best_strategy
# Do not tamper with the init method's parameters, or best_strategy's parameters
# But you can change anything inside this you want otherwise
#############################################################

class Node():
    def __init__(self, board, move, score = 0):
        self.score = score
        self.board = board
        self.move = move
    def __lt__(self, other):
        return self.score < other.score

def change(board, index, value):
    return str(board)[:index] + str(value) + str(board)[index + 1:]

class Strategy():
    def __init__(self):
        self.board = self.get_starting_board()

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
        pretty_board = ""
        for i in range(0, 10):
            pretty_board += board[10 * i: 10 * (i + 1)] + "\n"
        return pretty_board

    def opponent(self, player):
        """Get player's opponent."""
        if player == "@":
            return "o"
        if player == "o":
            return "@"
        pass

    def find_match(self, board, player, square, direction):                             #CODED
        """
        Find a square that forms a match with `square` for `player` in the given
        `direction`.  Returns None if no such square exists.
        """
        check = False
        while board[square + direction] == self.opponent(player):
            square += direction
            check = True
        if board[square + direction] == EMPTY and check:
            return square + direction
        return None

    def find_match_inverse(self, board, player, square, direction):
        check = False
        # s = board[square]
        # e = E
        # var = board[square + E]
        while board[square + direction] == self.opponent(player):
            square += direction
            check = True
        if board[square + direction] == player and check:
            return square + direction
        return None

    def is_move_valid(self, board, player, move):
        """Is this a legal move for the player?"""
        pass

    def make_move(self, board, player, move):                                           #CODED
        """Update the board to reflect the move by the specified player."""
        orig = move
        #board = board.join("")
        for direction in DIRECTIONS:
            move = orig
            if self.find_match_inverse(board, player, move, direction) is not None:      #should be the exact same as find_match but should look for a square with player
                while board[move + direction] == self.opponent(player):
                    board = change(board, move + direction, player)
                    move += direction
        board = change(board, orig, player)
        return board

    def get_valid_moves(self, board, player):                                           #CODED
        """Get a list of all legal moves for player."""
        moves = set()
        for square in range(11, 89):        #11, 89
            if board[square] == player:
                for direction in DIRECTIONS:
                    new_move = self.find_match(board, player, square, direction)
                    if new_move is not None:
                        moves.add(new_move)
        return list(moves)

    def has_any_valid_moves(self, board, player):
        """Can player make any moves?"""
        return self.get_valid_moves(board, player) is not None

    def next_player(self, board, prev_player):
        """Which player should move next?  Returns None if no legal moves exist."""
        if len(self.get_valid_moves(board, self.opponent(prev_player))) != 0:
            return self.opponent(prev_player)
        if len(self.get_valid_moves(board, prev_player)) != 0:
            return prev_player
        return None

    def score(self, board, player=BLACK):
        """Compute player's score (number of player's pieces minus opponent's)."""
        opponent = self.opponent(player)
        play_count = 0
        opp_count = 0
        for i in board:
            if i == player:
                play_count += 1
            if i == opponent:
                opp_count += 1
        return play_count - opp_count

    global STABILITY
    STABILITY = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    def weighted_score(self, board, player = BLACK):
        global STABILITY
        standard_matrix = "0000000000011111111001111111100111111110011111111001111111100111111110011111111001111111100000000000"
        #print(board)
        matrix = [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,]
        if board.count(EMPTY) < 45:
            add = 0
            for i in range(11, 89):
                square = i
                if STABILITY[i] != 100:
                    stable = True
                    for dir in DIRECTIONS:
                        while (board[square + dir] != OUTER and stable == True):
                            if board[square + dir] == EMPTY:
                                stable = False
                            square += dir
                        if stable:
                            add += 10
                    if stable:
                        STABILITY[i] = add

        player_score = 0
        opponent_score = 0
        for i in range(11, 89):
            if board[i] == player:
                player_score += (int(matrix[i]) * STABILITY[i])
            if board[i] == self.opponent(player):
                opponent_score += (int(matrix[i]) * STABILITY[i])
        return player_score - opponent_score


    def game_over(self, board, player):
        """Return true if player and opponent have no valid moves"""
        return (not self.has_any_valid_moves(board, player)) and (not self.has_any_valid_moves(board, self.opponent(player)))

    def minmax(self, node, player, depth):
        best = {BLACK: max, WHITE: min}
        board = node.board
        if depth == 0:
            node.score = self.weighted_score(board)
            return node
        my_moves = self.get_valid_moves(board, player)
        children = []
        for move in my_moves:
            next_board = self.make_move(board, player, move)
            next_player = self.next_player(next_board, player)
            if next_player is None:
                c = Node(next_board, move, score = 1000 * self.score(next_board))
                children.append(c)
            else:
                c = Node(next_board, move)
                c.score = self.minmax(c, next_player, depth = depth - 1).score
                children.append(c)
        winner = best[player](children)
        node.score = winner.score
        return winner

    def alpha_beta_pruning(self, node, player, depth, alpha = -1 * float('inf'), beta = float('inf')):
        best = {BLACK: max, WHITE: min}
        board = node.board
        if depth == 0:
            node.score = self.weighted_score(board)
            return node
        my_moves = self.get_valid_moves(board, player)
        children = []
        for move in my_moves:
            next_board = self.make_move(board, player, move)
            next_player = self.next_player(next_board, player)
            if next_player is None:
                c = Node(next_board, move, score=1000 * self.score(next_board))
                children.append(c)
            else:
                c = Node(next_board, move)
                c.score = self.alpha_beta_pruning(c, next_player, depth=depth - 1, alpha=alpha, beta=beta).score + random.random()
                children.append(c)
                if player == BLACK:
                    alpha = max(alpha, c.score)
                if player == WHITE:
                    beta = min(beta, c.score)
                if alpha >= beta:
                    break
        winner = best[player](children)
        node.score = winner.score
        return winner

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
        return self.minmax(Node(board, None, 0), player, depth)

    def minmax_strategy(self, board, player, depth = 3):
        # calls minmax_search
        # feel free to adjust the parameters
        # returns an integer move
        return self.minmax_search(board, player, depth).move

    def alphabeta_search(self, board, player, depth):
        return self.alpha_beta_pruning(Node(board, None, 0), player, depth)

    def alphabeta_strategy(self, board, player, depth = 5):
        board = ''.join(board )
        return self.alphabeta_search(board, player, depth).move

    def random_strategy(self, board, player):
        return random.choice(self.get_valid_moves(board, player))

    def best_strategy(self, board, player, best_move, still_running):
        ## THIS IS the public function you must implement
        ## Run your best search in a loop and update best_move.value
        depth = 1
        while (True):
            ## doing random in a loop is pointless but it's just an example
            best_move.value = self.alphabeta_strategy(board, player)
            depth += 1

    standard_strategy = alphabeta_strategy

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
        strategy = {BLACK: black.standard_strategy, WHITE: white.random_strategy}
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
        strategy = lambda who: self.black.random_strategy if who == BLACK else self.white.best_strategy
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
