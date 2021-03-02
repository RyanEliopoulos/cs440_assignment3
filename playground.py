import re
import unittest
from msttt import *
import subprocess
# import timeout_decorator
import time


class MultiStrategyTestCase(unittest.TestCase):

    def test_count_outcomes_easy(self):
        mss = MultiStrategySearch()
        # t3s = TTTNode(1, (1, 0, 1, -1, -1, 1, 1, -1, -1), None)

        # wins = mss.count_outcomes(t3s, False)
        # msg = f"Unexpected outcome for state: {t3s.board}"
        # self.assertEqual((0, 1, 0), wins, msg)

        t3s = TTTNode(1, (1, -1, 1, -1, -1, 1, 1, -1, 0), None)
        wins = mss.count_outcomes(t3s, False)
        msg = f"Unexpected outcome for state: {t3s.board}"
        self.assertEqual((0, 0, 1), wins, msg)
        #
        # t3s = TTTNode(-1, (1, 0, 1, -1, -1, 1, 1, -1, 0), None)
        # wins = mss.count_outcomes(t3s, False)
        # msg = f"Unexpected outcome for state: {t3s.board}"
        # self.assertEqual((0, 1, 1), wins, msg)
        #
        # t3s = TTTNode(1, (1, 0, 1, -1, -1, 1, 0, -1, 0), None)
        # wins = mss.count_outcomes(t3s, False)
        # msg = f"Unexpected outcome for state: {t3s.board}"
        # self.assertEqual((0, 3, 1), wins, msg)
        #
        #





if __name__ == "__main__":
    unittest.main()