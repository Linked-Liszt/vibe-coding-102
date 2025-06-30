# Vibe Coding 102: Applying Some Methodology to the Magic

Built for the ANL Vibe Coding Hackathon 06-30-2025. **NOTE: For those accessing this live: It is not expected that you keep up with the talk. Feel free to file this away and try it out in the afternoon.**

This repository contains a series of exercises designed to explore different aspects of using Large Language Models (LLMs) for coding tasks. The tutorial is broken down into three modules, each focusing on a specific skill or concept.

## Modules

*   **m1_the_loop**: A debugging exercise for a k-NN implementation, focusing on a tight feedback loop.
*   **m2_context**: Demonstrates how different contextual documents alter LLM-generated code for the same task.
*   **m3_reading_code**: An exercise in using an LLM to understand and document obfuscated code.

## Setup

To complete these exercises, you will need a Python environment that supports type hints (Python 3.10+). This can entirely be done with the python stdlib, but an env is recommended regardless. 

These tutorial are designed to be agentic tool agnostic.


### Using `venv`

1.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```

2.  **Activate the environment:**
    ```bash
    source .venv/bin/activate
    ```

### Using Anaconda/Conda

1.  **Create a conda environment:**
    ```bash
    conda create --name llm-tutorial python=3.12
    ```

2.  **Activate the environment:**
    ```bash
    conda activate llm-tutorial
    ```
