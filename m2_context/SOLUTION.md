# Research Buffer: 

Prompt: @/m2_context/buffer.py @/m2_context/research_doc.md Implement a circular buffer following the guidelines. Use the test_buffer file to verify your results. 

(Yeah... I 1-shot these and didn't look too closely. I was running a little low on time. Though it's fairly low-risk if these implementations have edge cases ;) )


```python
# circular_buffer.py

def _add_item(state: tuple, item: any) -> tuple:
    """A pure function to add an item to the buffer state."""
    items, head, count, size = state
    
    # Calculate the position for the new item
    write_pos = (head + count) % size
    
    # Create the new tuple of items
    new_items = items[:write_pos] + (item,) + items[write_pos + 1:]
    
    # If the buffer is full, the head pointer moves forward
    new_head = (head + 1) % size if count == size else head
    
    # The count increases but does not exceed the size
    new_count = min(count + 1, size)
    
    return (new_items, new_head, new_count, size)

def _read_items(state: tuple) -> list[any]:
    """A pure function to read all items from the buffer state."""
    items, head, count, size = state
    
    # Read items in FIFO order, handling wrap-around
    return [items[(head + i) % size] for i in range(count)]

class CircularBuffer:
    """A fixed-size buffer that overwrites the oldest data when full."""

    def __init__(self, size: int):
        """Initializes a CircularBuffer with a specified size."""
        if not isinstance(size, int) or size <= 0:
            raise ValueError("Buffer size must be a positive integer")
        
        # State is an immutable tuple: (items, head_pointer, current_count, max_size)
        self.state = (tuple([None] * size), 0, 0, size)

    def is_full(self) -> bool:
        """Checks if the buffer is currently full."""
        _items, _head, count, max_size = self.state
        return count == max_size

    def is_empty(self) -> bool:
        """Checks if the buffer is currently empty."""
        _items, _head, count, _max_size = self.state
        return count == 0

    def add(self, item: any):
        """Adds an item to the buffer, overwriting the oldest if full."""
        self.state = _add_item(self.state, item)

    def read(self) -> list[any]:
        """Retrieves all items from the buffer in FIFO order."""
        return _read_items(self.state)
```

# Enterprise Buffer

Prompt: @/m2_context/buffer.py @/m2_context/enterprise_doc.md  @/m2_context/test_buffer.py  Implement a circular buffer following the guidelines. Use the test_buffer to check the result. 

```python
import logging
from typing import List, Any, TypeVar

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

T = TypeVar('T')

class CircularBuffer:
    """
    A circular buffer implementation that overwrites the oldest data when full.

    This class provides a fixed-size buffer that operates in a circular manner,
    making it suitable for storing streams of data where only the most recent
    items are important.
    """

    def __init__(self, size: int):
        """
        Initializes the CircularBuffer.

        Args:
            size: The maximum number of items the buffer can hold. Must be a positive integer.

        Raises:
            ValueError: If the size is not a positive integer.
        """
        if not isinstance(size, int) or size <= 0:
            raise ValueError("Buffer size must be a positive integer")
        
        self._size = size
        self._buffer: List[Any] = [None] * size
        self._head = 0  # Points to the next available slot for writing
        self._tail = 0  # Points to the start of the data for reading
        self._is_full = False
        logging.info(f"CircularBuffer initialized with size {size}")

    def add(self, item: Any) -> None:
        """
        Adds an item to the buffer.

        If the buffer is full, the oldest item is overwritten.

        Args:
            item: The item to add to the buffer.
        """
        if self._is_full:
            logging.info(f"Buffer is full. Overwriting oldest item at index {self._tail}")
        
        self._buffer[self._head] = item
        self._head = (self._head + 1) % self._size

        if self._is_full:
            self._tail = (self._tail + 1) % self._size
        elif self._head == self._tail:
            self._is_full = True

    def read(self) -> List[Any]:
        """
        Reads all items from the buffer in order from oldest to newest.

        Returns:
            A list of items currently in the buffer.
        """
        if self.is_empty():
            return []
        
        if self._is_full:
            # The buffer is full, data is from tail to end, then start to head
            return self._buffer[self._tail:] + self._buffer[:self._head]

        # Buffer is not full, data is from tail to head
        if self._tail < self._head:
            return self._buffer[self._tail:self._head]
        else:
            # This case should not be reached in a non-full buffer
            # unless it's empty, which is handled above.
            return []

    def is_full(self) -> bool:
        """
        Checks if the buffer is full.

        Returns:
            True if the buffer is full, False otherwise.
        """
        return self._is_full

    def is_empty(self) -> bool:
        """
        Checks if the buffer is empty.

        Returns:
            True if the buffer is empty, False otherwise.
        """
        return not self._is_full and self._head == self._tail
```