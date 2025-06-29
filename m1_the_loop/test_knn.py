import math
import unittest
from collections import Counter
import sys
import os

# NOTE: Run this file directly. python m1_the_loop/test_knn.py 
# It's set up this way to be able to be run a little easier in context of the tutorial.

# Make it possible to run the tests from the root of the project
if os.path.basename(os.getcwd()) == 'm1_the_loop':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from knn import calculate_distances, get_majority_vote, classify_point

class TestCalculateDistances(unittest.TestCase):
    def setUp(self):
        """Set up a consistent dataset for all tests."""
        self.training_data = [
            ((0, 0), 'A'),
            ((1, 1), 'A'),
            ((4, 4), 'B'),
            ((5, 5), 'B')
        ]
        self.new_point = (2, 2)

    def test_calculate_distances_buggy(self):
        """
        This test is designed to FAIL with the buggy code.
        It asserts the correct distance, but the function returns the squared one.
        """
        distances = calculate_distances(self.training_data, self.new_point)
        # This will FAIL because the function returns 8, not sqrt(8).
        self.assertAlmostEqual(distances[0][0], math.sqrt(8), msg="FAIL: Function should return sqrt(8).")


class TestGetMajorityVote(unittest.TestCase):
    def test_get_majority_vote_buggy_tie(self):
        """
        This test is designed to FAIL with the alphabetical tie-breaking bug.
        It creates a tie where the alphabetically first label ('A') is not the closest.
        """
        tie_neighbors = [
            (1.0, 'B'), (2.0, 'A'), 
            (3.0, 'B'), (4.0, 'A')
        ]
        result = get_majority_vote(tie_neighbors)
        # The buggy code will return 'A' (alphabetical). The correct code would return 'B' (closest).
        self.assertEqual(result, 'B', "FAIL: Buggy code chose 'A' alphabetically instead of 'B' (closest).")

    def test_get_majority_vote_three_way_tie(self):
        """
        This test is designed to FAIL with the alphabetical tie-breaking bug.
        It creates a three-way tie where the alphabetically first label ('A') is not the closest.
        """
        tie_neighbors = [(1.0, 'C'), (2.0, 'B'), (3.0, 'A')]
        result = get_majority_vote(tie_neighbors)
        # The buggy code will return 'A' (alphabetical). The correct code would return 'C' (closest).
        self.assertEqual(result, 'C', "FAIL: Buggy code chose 'A' alphabetically instead of 'C' (closest).")

class TestClassifyPoint(unittest.TestCase):
    def setUp(self):
        """Set up a consistent dataset for all tests."""
        self.new_point = (2, 2)

    def test_end_to_end_buggy(self):
        """
        This test is designed to FAIL with the alphabetical tie-breaking bug.
        It creates a tie where the alphabetically first label ('A') is not the closest.
        """
        training_data_tie = [
            ((3, 3), 'B'), # dist from (2,2) is sqrt(2)
            ((1, 1), 'A'), # dist from (2,2) is sqrt(2)
            ((10, 10), 'C')
        ]
        result = classify_point(training_data_tie, self.new_point, k=2)
        # The buggy code will return 'A' (alphabetical). The correct code would return 'B' (closest).
        self.assertEqual(result, 'B', "FAIL: Buggy code chose 'A' alphabetically instead of 'B' (closest).")

if __name__ == '__main__':
    # This will run all the tests defined in the TestKnnFunctions class.
    # The output will clearly show which tests pass and which fail.
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
