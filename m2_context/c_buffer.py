from typing import List, Any, TypeVar

class CircularBuffer:
    """
    A fixed-size buffer that overwrites the oldest data when full.

    This class provides a FIFO (First-In-First-Out) data structure with a
    fixed capacity. When the buffer is full, new items overwrite the oldest
    items in the buffer.
    """

    def __init__(self, size: int):
        """
        Initializes a CircularBuffer with a specified size.

        Args:
            size (int): The maximum capacity of the buffer. Must be a positive integer.

        Raises:
            ValueError: If the size is not a positive integer.
        """
        pass

    def is_full(self) -> bool:
        """
        Checks if the buffer is currently full.

        Returns:
            bool: True if the buffer is at maximum capacity, False otherwise.
        """
        pass

    def is_empty(self) -> bool:
        """
        Checks if the buffer is currently empty.

        Returns:
            bool: True if the buffer contains no items, False otherwise.
        """
        pass

    def add(self, item: any):
        """
        Adds an item to the buffer.

        If the buffer is full, this operation will overwrite the oldest item.

        Args:
            item (any): The item to be added to the buffer.
        """
        pass

    def read(self) -> list[any]:
        """
        Retrieves all items from the buffer in FIFO order.

        Returns:
            list[any]: A list of all items currently in the buffer, from oldest to newest.
                       Returns an empty list if the buffer is empty.
        """
        pass
