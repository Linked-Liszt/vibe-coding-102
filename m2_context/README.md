# Overview

This directory demonstrates how providing different contextual documents to a LLM dramatically change the generated code, even when the basic task remains the same.

Ask the LLM to implement the `CircularBuffer` class defined in `c_buffer.py`. A lightweight test suite, `test_buffer.py`, can be used to check the correctness of the files. 

## The Scenarios

Two different sets of requirements were provided to an LLM to guide the implementation:

1.  **The "Research" Context (`research_doc.md`)**:
    *   **Goal:** Rapid prototyping.
    *   **Style:** Emphasizes a "Functional Core, Imperative Shell" paradigm, using pure functions and immutable state.
    *   **Priorities:** Speed of implementation over polished, production-ready code.

2.  **The "Enterprise" Context (`enterprise_doc.md`)**:
    *   **Goal:** Production-ready library code.
    *   **Style:** Requires a strict Object-Oriented (OOP) approach.
    *   **Priorities:** Robustness, extensive error handling, detailed documentation, and logging.
