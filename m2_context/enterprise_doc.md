**Project:** Core Utilities Library (`common.utils`)
**Component:** `CircularBuffer`
**Ticket:** CORE-112: Implement Production-Ready Circular Buffer

**General Coding Standards:**
- **Paradigm:** Adhere to a strict Object-Oriented Programming (OOP) model.
- **Robustness:** Code must be defensive. Explicitly check for invalid inputs and edge cases. All external inputs must be validated.
- **Error Handling:** Raise specific exceptions (`ValueError`, `TypeError`) with clear error messages. Do not rely on silent failures or broad `try...except` blocks.
- **Logging:** Integrate logging points. Use the standard `logging` module to log key events at the INFO level (e.g., buffer creation, overwrite events) and potential issues at the WARNING level.
- **Documentation:**
    - Provide exhaustive Google-style docstrings for the class and all public methods.
    - Include type hints for all method signatures and arguments as per PEP 484.
    - Add inline comments to explain complex logic, especially pointer arithmetic.

**Implementation Mandates:**
- **State Management:** All state must be managed via instance variables (`self`).
- **Internal Structure:** Use a pre-allocated Python `list` for the internal data store to ensure predictable memory allocation.
- **API:** Implement the standard `CircularBuffer` API contract (`__init__`, `add`, `read`, `is_full`, `is_empty`).