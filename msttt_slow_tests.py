import re
import unittest
from msttt import *
import subprocess
import timeout_decorator
import time

class MultiStrategySlowTestCase(unittest.TestCase):

    @timeout_decorator.timeout(seconds=10, exception_message="Timed out counting outcomes of full game...")
    def test_count_full(self):
        t3s = TTTNode(1, (0,0,0,0,0,0,0,0,0), None)
        mss = MultiStrategySearch()
        wins = mss.count_outcomes(t3s, False)
        msg = "Playing out a full game doesn't end with the expected number of ties."
        self.assertEqual(46080, wins[0], msg)
        msg = "Playing out a full game doesn't end with the expected number of x-wins."
        self.assertEqual(131184, wins[1], msg)
        msg = "Playing out a full game doesn't end with the expected number of o-wins."
        self.assertEqual(77904, wins[2], msg)




