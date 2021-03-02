import re
import unittest
from msttt import *
import subprocess
#import timeout_decorator
import time

class MultiStrategyTestCase(unittest.TestCase):
    def test_is_win_from_slides(self):
        t3s = TTTNode(1, (0,0,0,0,0,0,0,0,0), None)
        mss = MultiStrategySearch()
        wins = mss.is_win(t3s)
        msg = "The starting game isn't a win..."
        self.assertEqual(False, wins, msg)

        t3s = TTTNode(1, (1,0,1,-1,-1,1,1,-1,-1), None)
        wins = mss.is_win(t3s)
        msg = "One of the situations displayed in the slides is not properly evaluated by is_win"
        self.assertEqual(False, wins, msg)

        t3s = TTTNode(-1, (1,1,1,-1,-1,1,1,-1,-1), None)
        wins = mss.is_win(t3s)
        self.assertEqual((TicTacToe.Row,0,1), wins, msg)

        t3s = TTTNode(1, (1,-1,1,-1,-1,1,1,-1,-1), None)
        wins = mss.is_win(t3s)
        self.assertEqual((TicTacToe.Column, 1, -1), wins, msg)

        t3s = TTTNode(-1, (1,0,1,-1,-1,1,0,-1,1), None)
        wins = mss.is_win(t3s)
        self.assertEqual((TicTacToe.Column,2,1), wins, msg)

        t3s = TTTNode(-1, (1,-1,1,-1,1,1,1,-1,-1), None)
        wins = mss.is_win(t3s)
        self.assertEqual((TicTacToe.Diagonal,1,1), wins, msg)

    def test_count_outcomes_easy(self):
        mss = MultiStrategySearch()
        t3s = TTTNode(1, (1,0,1,-1,-1,1,1,-1,-1), None)
        wins = mss.count_outcomes(t3s, False)
        msg = f"Unexpected outcome for state: {t3s.board}" 
        self.assertEqual((0,1,0), wins, msg)

        t3s = TTTNode(1, (1,-1,1,-1,-1,1,1,-1,0), None)
        wins = mss.count_outcomes(t3s, False)
        msg = f"Unexpected outcome for state: {t3s.board}" 
        self.assertEqual((0,0,1), wins, msg)

        t3s = TTTNode(-1, (1,0,1,-1,-1,1,1,-1,0), None)
        wins = mss.count_outcomes(t3s, False)
        msg = f"Unexpected outcome for state: {t3s.board}" 
        self.assertEqual((0,1,1), wins, msg)

        t3s = TTTNode(1, (1,0,1,-1,-1,1,0,-1,0), None)
        wins = mss.count_outcomes(t3s, False)
        msg = f"Unexpected outcome for state: {t3s.board}" 
        self.assertEqual((0,3,1), wins, msg)

    def test_bestchoice(self):

        tup1 = (0, 5, 5)
        tup2 = (8, 1, 3)
        ret = bestchoice(tup1, tup2, 1)
        self.assertEqual(ret, tup2)

        tup1 = (8, 5, 5)
        tup2 = (8, 4, 5)
        ret = bestchoice(tup1, tup2, 1)
        self.assertEqual(ret, tup1)

        tup1 = (8, 5, 5)
        tup2 = (9, 5, 5)
        ret = bestchoice(tup1, tup2, 1)
        self.assertEqual(tup2, ret)


    def test_evaluate_strategies_from_slides(self):
        mss = MultiStrategySearch()

        # X_X
        # OOX  x's turn
        # XOO
        t3s = TTTNode(1, (1,0,1,-1,-1,1,1,-1,-1), None)
        wins = mss.evaluate_strategies(t3s, False)
        expected = {'BB': (0,1,0), 'BR': (0,1,0), 'RB': (0,1,0), 'RR': (0,1,0)}
        msg = f"Unexpected strategy outcome for state: {t3s.board}"
        self.assertEqual(expected, wins, msg)

        # XOX
        # OOX  x's turn
        # XO_
        t3s = TTTNode(1, (1,-1,1,-1,-1,1,1,-1,0), None)
        wins = mss.evaluate_strategies(t3s, False)
        expected = {'BB': (0,0,1), 'BR': (0,0,1), 'RB': (0,0,1), 'RR': (0,0,1)}
        msg = f"Unexpected strategy outcome for state: {t3s.board}"
        self.assertEqual(expected, wins, msg)

        # X_X
        # OOX  o's turn
        # XO_
        t3s = TTTNode(-1, (1,0,1,-1,-1,1,1,-1,0), None)
        wins = mss.evaluate_strategies(t3s, False)
        expected = {'BB': (0,0,1), 'BR': (0,1,1), 'RB': (0,0,1), 'RR': (0,1,1)}
        msg = f"Unexpected strategy outcome for state: {t3s.board}"
        self.assertEqual(expected, wins, msg)

        # XOX
        # O_X  o's turn
        # XO_
        t3s = TTTNode(-1, (1,-1,1,-1,0,1,1,-1,0), None)
        wins = mss.evaluate_strategies(t3s, False)
        expected = {'BB': (0,0,1), 'BR': (0,1,1), 'RB': (0,0,1), 'RR': (0,1,1)}
        msg = f"Unexpected strategy outcome for state: {t3s.board}"
        self.assertEqual(expected, wins, msg)

        # X_X
        # OOX  x's turn
        # _O_
        t3s = TTTNode(1, (1,0,1,-1,-1,1,0,-1,0), None)
        wins = mss.evaluate_strategies(t3s, False)
        expected = {'BB': (0,1,0), 'BR': (0,1,0), 'RB': (0,2,1), 'RR': (0,3,1)}
        msg = f"Unexpected strategy outcome for state: {t3s.board}"
        self.assertEqual(expected, wins, msg)


        # XOX
        # O_X  x's turn
        # _O_
        t3s = TTTNode(1, (1,-1,1,-1,0,1,0,-1,0), None)
        wins = mss.evaluate_strategies(t3s, False)
        expected = {'BB': (0,1,0), 'BR': (0,2,0), 'RB': (0,2,1), 'RR': (0,4,1)}
        msg = f"Unexpected strategy outcome for state: {t3s.board}"
        self.assertEqual(expected, wins, msg)


        
                


