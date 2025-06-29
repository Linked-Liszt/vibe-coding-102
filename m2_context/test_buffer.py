# test_circular_buffer.py

# NOTE: Run this file directly. python m2_context/test_circular_buffer.py 
# It's set up this way to be able to be run a little easier in context of the tutorial.

import unittest
from c_buffer import CircularBuffer


class TestCircularBuffer(unittest.TestCase):
    """A suite of tests for the CircularBuffer class using the unittest module."""

    def test_initialization(self):
        """Tests successful initialization and initial state."""
        buffer = CircularBuffer(5)
        self.assertTrue(buffer.is_empty())
        self.assertFalse(buffer.is_full())
        self.assertEqual(buffer.read(), [])

    def test_initialization_errors(self):
        """Tests that the constructor raises ValueError for invalid sizes."""
        with self.assertRaisesRegex(ValueError, "Buffer size must be a positive integer"):
            CircularBuffer(0)
        with self.assertRaisesRegex(ValueError, "Buffer size must be a positive integer"):
            CircularBuffer(-5)

    def test_add_and_read_items(self):
        """Tests adding items and reading them back in the correct order."""
        buffer = CircularBuffer(3)
        buffer.add(10)
        buffer.add(20)
        self.assertFalse(buffer.is_empty())
        self.assertFalse(buffer.is_full())
        self.assertEqual(buffer.read(), [10, 20])

    def test_buffer_becomes_full(self):
        """Tests that the buffer correctly identifies when it is full."""
        buffer = CircularBuffer(2)
        buffer.add('a')
        buffer.add('b')
        self.assertTrue(buffer.is_full())
        self.assertEqual(buffer.read(), ['a', 'b'])

    def test_overwrite_behavior(self):
        """Tests that adding to a full buffer overwrites the oldest element."""
        buffer = CircularBuffer(3)
        buffer.add(1)
        buffer.add(2)
        buffer.add(3)
        
        # Buffer is now full with [1, 2, 3]
        self.assertEqual(buffer.read(), [1, 2, 3])
        
        # This add should overwrite the oldest item (1)
        buffer.add(4)
        
        # The new state should be [2, 3, 4]
        self.assertTrue(buffer.is_full())
        self.assertEqual(buffer.read(), [2, 3, 4])

    def test_multiple_overwrites(self):
        """Tests that the buffer continues to overwrite correctly."""
        buffer = CircularBuffer(2)
        buffer.add(1)
        buffer.add(2)
        buffer.add(3)  # Overwrites 1 -> [2, 3]
        buffer.add(4)  # Overwrites 2 -> [3, 4]
        buffer.add(5)  # Overwrites 3 -> [4, 5]
        
        self.assertEqual(buffer.read(), [4, 5])
        self.assertTrue(buffer.is_full())

    def test_read_from_empty_buffer(self):
        """Tests that reading from a newly created buffer returns an empty list."""
        buffer = CircularBuffer(10)
        self.assertEqual(buffer.read(), [])

    def test_buffer_with_size_one(self):
        """Tests edge case of a buffer with size 1."""
        buffer = CircularBuffer(1)
        self.assertTrue(buffer.is_empty())
        
        buffer.add(100)
        self.assertTrue(buffer.is_full())
        self.assertEqual(buffer.read(), [100])
        
        buffer.add(200)
        self.assertTrue(buffer.is_full())
        self.assertEqual(buffer.read(), [200])

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

