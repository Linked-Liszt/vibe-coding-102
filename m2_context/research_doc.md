**Project:** Signal Processing R&D
**Component:** `CircularBuffer` (for algorithm prototyping)
**Task:** Quick implementation of a circular buffer for data stream simulation.

**Development Philosophy:**
- **Paradigm:** "Functional Core, Imperative Shell." The core logic should be in pure, stateless functions for easy testing and reasoning. Wrap them in a class to satisfy the project's basic API needs.
- **Speed Over Polish:** Prioritize getting a working implementation quickly. Minimize boilerplate.
- **Error Handling:** Rely on Python's duck typing. Avoid explicit type checks. Assume inputs are correct for the prototype's purpose.
- **Documentation:** Minimal documentation is required. A one-line docstring for the class and public methods is sufficient. No inline comments are needed unless the logic is exceptionally non-obvious.
- **No Dependencies:** Use only Python's built-in types and modules.

**Implementation Mandates:**
- **Core Logic:** Implement the buffer's operations (`add`, `read`) as private, pure functions that accept the current state as an argument and return the new state.
- **State Representation:** Use immutable tuples to represent the buffer's state (`(items, pointers, etc.)`) to reinforce the functional approach.
- **API Wrapper:** The public `CircularBuffer` class should simply manage the state and delegate all logic to the internal pure functions.
- **API:** The class must expose the standard `CircularBuffer` API contract (`__init__`, `add`, `read`, `is_full`, `is_empty`) to allow it to be swapped with other buffer implementations for testing.