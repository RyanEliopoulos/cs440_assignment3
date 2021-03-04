""""
    Ryan Paulos
    CS 440 - Artificial Intelligence
    Assignment 3
    Spring 2021

"""



"""MultiStrategy Search in TicTacToe

Warm up thought questions 
(not graded, just to get you going)... consider referring to the slides.

a. read the documentation for count_outcomes(). What should the 
   return value be for the input state 122122011? 
 
b. what should count_outcomes() return for an input state of
   102122001?



Graded questions (answer these):

1. Given an initially empty 3x3 board, how many end games result in
   a win for X?

    Evaluating all possible end game leaf nodes with count_outcomes, we can see that 131,184 end games result in an
    x win.


2. How early can X force a win assuming O plays randomly? (BR)

    X can force a win (that is, guarantee victory in subsequent moves) on their 2nd move when O plays randomly.
    

    The included check_quickest_bb method updates the MultiStrategySearch instance with a candidate node and the shortest
    path. This produces a TTTNode with board state (1, 0, -1, 1, 0, 0, 0, 0, 0)
    
    Running such a node through the evaluate_strategies method confirms the 'BR' outcomes as (0, 29, 0)
    



3. How early can X force a win assuming O plays the best strategy?


    X cannot force a win for themselves if O is playing the best strategy. If both players play using the best strategy
    the game will always end in a tie.  This is corroborated by the evaluate_strategies method when passed a
    blank board state.

"""

import sys
import math

class TicTacToe():
    Column = 0
    Row = 1
    Diagonal = 2
    StaleMate = 3
    Chrs = {0: ' ', 1: 'X', -1: 'O'}

from collections import namedtuple

#
# NOTE:  ** Be Careful Constructing These ! **
#
#       The 'nextplayer' field must be set appropriately for the board state
#       and no verification is performed to ensure that it is valid.
#       'nextplayer' should be 1 (if the nextplayer is X) and -1 otherwise
#       Although 'nextplayer' *could* be calculated from the board contents,
#       it is explicitly maintained in the state for efficiency.
#
#       Recall that this creates the class TTTNode which behaves like
#       a tuple (the instance variable references are immutable), but
#       unlike a tuple, you can access the instance variables ("slots")
#       with names instead of indicies. Here, each instance will have
#       the three instance variable names: 'nextplayer', 'board' and 'parent'
TTTNode = namedtuple('TTTNode', ['nextplayer', 'board', 'parent'])

class MultiStrategySearch():
    def __init__(self, boardsize=3):
        self.n = boardsize
        self.n2 = boardsize**2

        # Answering #3
        self.quickest_bb_node = None
        self.quickest_bb_len = None

    def is_win(self, tttnode):
        """ _Part 1: Implement This Method_
        
        Use your code from TicTacToe to determine if the
        TTTNode instance represents a board in an end-game configuration. 
        Note that "tttnode" is an argument to the method here, it is 
        not an instance variable...

        For a board of size n, a win requires one player to have n tokens
        in a line (vertical, horizontal or diagonal). 

        Arguments:
         tttnode - an instance of TTTNode representing a particular node
                     in the search tree (this give you player information
                     along with the state in the search graph, which can 
                     help you improve the speed of this method). You can 
                     assume that any tttnode passed into this method
                     with encapsulate a board with self.n2 elements

        Returns:
         (TicTacToe.Column, c, player): if player wins in column c
         (TicTacToe.Row, r, player): if player wins in row r
         (TicTacToe.Diagonal, 0, player): if player wins via
           a diagonal in the upper-left corner
         (TicTacToe.Diagonal, 1, player): if player wins via a
           diagonal in the upper-right corner
         (TicTacToe.StaleMate, 0, 0): if the game is a stalemate
         False: if the outcome can't be determined yet
        """

        i = 0  # Beginning slice index
        j = self.n  # Trailing slice index
        made_last_move = 1 if tttnode.nextplayer == -1 else -1
        board = tttnode.board
        n = int(math.sqrt(len(board)))

        # Checking horizontal win
        for x in range(n):
            row = board[i:j]
            if sum(row) == (made_last_move * n):
                return TicTacToe.Row, x, made_last_move
            i += n
            j += n

        # Checking vertical win
        for x in range(n):
            column = board[x::n]
            if sum(column) == (made_last_move * n):
                return TicTacToe.Column, x, made_last_move

        # Checking first diagonal win
        diagonal = []
        for x in range(n):
            next_square_index = (n * x) + x
            diagonal.append(board[next_square_index])
        if sum(diagonal) == (made_last_move * n):
            return TicTacToe.Diagonal, 0, made_last_move
        # Checking second diagonal
        diagonal = []
        for x in range(n):
            complement = n - x
            next_square_index = (n * x) + complement - 1  # -1 adjusts for 0 indexing
            diagonal.append(board[next_square_index])
        if sum(diagonal) == (made_last_move * n):
            return TicTacToe.Diagonal, 1, made_last_move

        # Checking for stalemate
        if 0 not in board:
            return TicTacToe.StaleMate, 0, 0

        return False

    def show(self, state, stream=sys.stdout):
        """Prints a representation of the board on the specified stream."""
        
        for i in range(self.n):
            fmtstr = []
            for j in range(self.n-1):
                fmtstr.append( " %s |"%TicTacToe.Chrs[state.board[i*self.n+j]])
            fmtstr.append(" %s "%TicTacToe.Chrs[state.board[(i+1)*self.n-1]])
            line = "".join(fmtstr)
            print(line, file=stream)
            if i < self.n-1:
                print('-'*len(line), file=stream)

    def successors(self, tttnode):
        """Yield the successor nodes of the given parent node.
        
        Note that this successor function takes a TTTNode instance
        and yields TTTNode instances. These nodes don't track path/edge
        costs since we don't care about that in our search. But, they do
        maintain a reference to their parent so we can navigate the search
        tree.
        """
        for i in range(self.n**2):
            if tttnode.board[i] == 0:
                lstate = list(tttnode.board)  # create a list to manipulate
                lstate[i] = tttnode.nextplayer # fill an empty space
                
                # before we yield the successor, turn that child state back
                # into a tuple so no one can accidentally modify it...
                yield TTTNode(tttnode.nextplayer * -1,
                               tuple(lstate), tttnode)
                            
    def count_outcomes(self, tttnode, verbose=False):
        """ _ Part 4: Implement this method _ 

        Counts the distinct outcomes of tictactoe games.

        Hints: (1) it may be easiest to create a recursive helper method
        to do the heavy lifting. (2) you can turn a list into a tuple by
        calling tuple() with the list as an argument.

        args:
            tttnode - a TTTNode instance representing the 'initial state'
            verbose - True for debugging output

        returns:
            a tuple of (# of ties, # of X wins, # of O wins) for all possible
            games generated by starting at the initial state and playing until
            completion.
        """

        ties = 0
        wins_o = 0
        wins_x = 0

        win_check = self.is_win(tttnode)
        if win_check:
            if win_check[2] == 1:
                wins_x += 1
            elif win_check[2] == -1:
                wins_o += 1
            else:
                ties += 1

        else:
            for successor in self.successors(tttnode):
                child_ties, child_wins_x, child_wins_o = self.count_outcomes(successor)
                ties += child_ties
                wins_o += child_wins_o
                wins_x += child_wins_x

        return ties, wins_x, wins_o

    def evaluate_strategies(self, tttnode, verbose=False):
        """ _ Part 5: Implement this method _ 
        
        return a dictionary representing the strategic outcome table for
        a given input state (tttnode). If verbose is False, no
        output should be generated on stdout or stderr.
        
        the dictionary should have keys 'BB', 'RB', 'BR', and 'RR'
        representing the best ('B') and random ('R') strategies
        for player 1 (X) and player 2 (O) respectively. So 'RB'
        corresponds to X playing randomly and O playing its best.
        Values of this table should be a tuple of (ties, X-wins, O-wins).

        Hint: this method may be easiest to implement recursively.
        """

        # First checking for base case
        win_check = self.is_win(tttnode)
        if win_check:
            if win_check[2] == 1:
                tup = (0, 1, 0)
            elif win_check[2] == -1:
                tup = (0, 0, 1)
            elif win_check[2] == 0:
                tup = (1, 0, 0)

            frame_dict = {
                'BB': tup
                , 'BR': tup
                , 'RB': tup
                , 'RR': tup
            }

            return frame_dict

        # Not a winning state. Calling upon children for assistance.

        bb = None
        br = None
        rb = None
        rr = None

        first_node = None  # Not really best
        for successor in self.successors(tttnode):
            if first_node is None:  # Current node has no opinion yet
                first_node = successor
                ret_dict = self.evaluate_strategies(successor)
                bb = ret_dict['BB']
                br = ret_dict['BR']

                rb = ret_dict['RB']
                rr = ret_dict['RR']
            else:  # Considering at least a second successor node
                ret_dict = self.evaluate_strategies(successor)
                # Establishing random values
                successor_rr = ret_dict['RR']
                rr = addtuples(rr, successor_rr)
                # Deciding best values
                successor_bb = ret_dict['BB']
                bb = bestchoice(bb, successor_bb, tttnode.nextplayer)

                # Addressing mixed strategies
                successor_br = ret_dict['BR']
                successor_rb = ret_dict['RB']
                if tttnode.nextplayer == 1:
                    # Selecting best for x
                    br = bestchoice(br, successor_br, tttnode.nextplayer)
                    # Selecting random for x
                    rb = addtuples(rb, successor_rb)

                else:
                    # Selecting best for o
                    rb = bestchoice(rb, successor_rb, tttnode.nextplayer)
                    # Selecting random for o
                    br = addtuples(br, successor_br)
        # Done evaluating successors. Returning outcome table.
        outcome_table = {
            'BB': bb
            , 'BR': br
            , 'RB': rb
            , 'RR': rr
        }

        return outcome_table

    def check_quickest_bb(self, tttnode, verbose=False):
        """ _ Part 5: Implement this method _

        return a dictionary representing the strategic outcome table for
        a given input state (tttnode). If verbose is False, no
        output should be generated on stdout or stderr.

        the dictionary should have keys 'BB', 'RB', 'BR', and 'RR'
        representing the best ('B') and random ('R') strategies
        for player 1 (X) and player 2 (O) respectively. So 'RB'
        corresponds to X playing randomly and O playing its best.
        Values of this table should be a tuple of (ties, X-wins, O-wins).

        Hint: this method may be easiest to implement recursively.
        """

        # First checking for base case
        win_check = self.is_win(tttnode)
        if win_check:
            if win_check[2] == 1:
                tup = (0, 1, 0)
            elif win_check[2] == -1:
                tup = (0, 0, 1)
            elif win_check[2] == 0:
                tup = (1, 0, 0)

            frame_dict = {
                'BB': tup
                , 'BR': tup
                , 'RB': tup
                , 'RR': tup
            }

            return frame_dict

        # Not a winning state. Calling upon children for assistance.

        bb = None
        br = None
        rb = None
        rr = None

        first_node = None  # Not really best
        for successor in self.successors(tttnode):
            if first_node is None:  # Current node has no opinion yet
                first_node = successor
                ret_dict = self.check_quickest_bb(successor)
                bb = ret_dict['BB']
                br = ret_dict['BR']

                rb = ret_dict['RB']
                rr = ret_dict['RR']
            else:  # Considering at least a second successor node
                ret_dict = self.check_quickest_bb(successor)
                # Establishing random values
                successor_rr = ret_dict['RR']
                rr = addtuples(rr, successor_rr)
                # Deciding best values
                successor_bb = ret_dict['BB']
                bb = bestchoice(bb, successor_bb, tttnode.nextplayer)

                # Addressing mixed strategies
                successor_br = ret_dict['BR']
                successor_rb = ret_dict['RB']
                if tttnode.nextplayer == 1:
                    # Selecting best for x
                    br = bestchoice(br, successor_br, tttnode.nextplayer)
                    # Selecting random for x
                    rb = addtuples(rb, successor_rb)

                else:
                    # Selecting best for o
                    rb = bestchoice(rb, successor_rb, tttnode.nextplayer)
                    # Selecting random for o
                    br = addtuples(br, successor_br)

            # This version should be selecting the exact node that it considers the force win state
            if br[0] == 0 and br[2] == 0 and br[1] > 0:
                # Found a node where x is guaranteed to win
                quickest_len = 1
                if self.quickest_bb_node is None:
                    self.quickest_bb_node = successor
                    parent_node = tttnode
                    while parent_node is not None:
                        parent_node = parent_node.parent
                        quickest_len += 1
                    self.quickest_bb_len = quickest_len
                else:
                    parent_node = tttnode
                    while parent_node is not None:
                        parent_node = parent_node.parent
                        quickest_len += 1

                    if quickest_len < self.quickest_bb_len:
                        self.quickest_bb_node = successor
                        self.quickest_bb_len = quickest_len

        # if bb[0] == 0 and bb[2] == 0 and bb[1] > 0:
        #     # Found a node where x is guaranteed to win
        #     quickest_len = 1
        #     if self.quickest_bb_node is None:
        #         self.quickest_bb_node = tttnode
        #         parent_node = tttnode.parent
        #         while parent_node is not None:
        #             parent_node = parent_node.parent
        #             quickest_len += 1
        #         self.quickest_bb_len = quickest_len
        #     else:
        #         parent_node = tttnode.parent
        #         while parent_node is not None:
        #             parent_node = parent_node.parent
        #             quickest_len += 1
        #
        #         if quickest_len < self.quickest_bb_len:
        #             self.quickest_bb_node = tttnode
        #             self.quickest_bb_len = quickest_len

        # Done evaluating successors. Returning outcome table.
        outcome_table = {
            'BB': bb
            , 'BR': br
            , 'RB': rb
            , 'RR': rr
        }

        return outcome_table







def addtuples(t1, t2):
    """ _ Part 2: Implement this function _

    Given two tuples (of the same length) as input, 
    return a tuple that represents the element-wise sum
    of the inputs.  That is

    (out_0, ..., out_n) = (t1_0 + t2_0, ..., t1_n + t2_n)
    """
    sum_list = []
    for x in range(len(t1)):
        sum_list.append(t1[x] + t2[x])

    return tuple(sum_list)


def bestchoice(t1, t2, whom):
    """ _ Part 3: Implement this function _

    Given two tuples representing:
    (ties, p1-wins, p2-wins)
    
    return the 'best' choice for the player
    'whom'.

    The best choice decision is the one where
    the opponent is least likely to win. If the 
    likelihood (% wins) is insufficient to determine
    a 'best' choice, break ties by selecting the tuple
    in which the 'whom' has *won* the most games; if
    this is still insufficient, break ties further by
    selecting the tuple with the most stalemates.

    """

    # Summing games for ratio calculations
    total_games_first = t1[0] + t1[1] + t1[2]
    total_games_second = t2[0] + t2[1] + t2[2]

    # Setting node reference variables
    if whom == 1:
        enemy_index = 2
        our_index = 1
    else:
        enemy_index = 1
        our_index = 2

    # Evaluating win ratios
    enemy_ratio_first = t1[enemy_index] / total_games_first
    enemy_ratio_second = t2[enemy_index] / total_games_second

    if enemy_ratio_first > enemy_ratio_second:
        return t2
    elif enemy_ratio_second > enemy_ratio_first:
        return t1
    else:  # Tie on enemy win rate. Evaluating using our win rate.

        if t1[our_index] > t2[our_index]:
            return t1
        elif t2[our_index] > t1[our_index]:
            return t2
        else:  # Tie.
            if t1[0] > t2[0]:
                return t1
            else:
                return t2



if __name__ == "__main__":
    import argparse
    import random
    parser = argparse.ArgumentParser()
    parser.add_argument("--state")
    parser.add_argument("--verbose", action='store_true')
    parser.add_argument("do_what", choices=['count', 'evaluate'])
    args = parser.parse_args()

    if args.state:
        assert len(args.state) == 9, "Expected string with 9 elements"
        
        state = [int(z) for z in args.state]
        state = [-1 if s == 2 else s for s in state]
        stateset = set(state)
        assert not stateset.issuperset(set([0,1,2])), \
            "Expected string with elements 0,1,2"
        state = tuple(state)
        assert sum(state) == 0 or sum(state) == 1, \
            "Doesn't look like moves are alternating!"
        
        if sum(state) == 1:
            nextturn = -1
        elif sum(state) == 0:
            nextturn = 1
        else:
            print("state is invalid...")
            sys.exit(1)

        if args.verbose:
            print("".join(TicTacToe.Chrs[i] for i in state[:3]))
            print("".join(TicTacToe.Chrs[i] for i in state[3:6]))
            print("".join(TicTacToe.Chrs[i] for i in state[6:]))

        t3s = TTTNode(nextturn, state, None)

        mss = MultiStrategySearch()
        mss.show(t3s)
        if args.do_what == 'evaluate':
            pm = mss.evaluate_strategies(t3s)
            for key in sorted(pm):
                print("%s:%s"%(str(key), str(pm[key])))
            
        elif args.do_what == 'count':
            wins = mss.count_outcomes(t3s, args.verbose)
            print("Wins:", wins)
                
