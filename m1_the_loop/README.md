# k-NN Debugging Exercise

This exercise walks through debugging a simple implementation of the k-Nearest Neighbors (k-NN) algorithm. The goal is to practice a tight feedback loop with an LLM, focusing on fixing one issue at a time.

## The Problem: k-Nearest Neighbors (k-NN)

k-NN is a simple, supervised machine learning algorithm that can be used for classification or regression. For a given data point, it finds the 'k' closest points in the training data and assigns a label based on the labels of its neighbors. In this classification exercise, the label is determined by a majority vote among the neighbors. 

_Technically,_ it's not a very robust solution and can't handle distance ties well, but treat is as the toy problem it is. The unit tests are also very targeted so there may be workarounds that still pass the tests, but I think it's best to keep the code small and easy for people to pick up quickly rather than being non-deterministic or robust. 

## The Exercise: The Tight Loop

The core of this exercise is to practice the "tight loop" of development with an AI assistant:

1.  **Prompt the LLM**: Isolate a single function and ask the LLM to fix the bug within it.
2.  **Read the Output**: Review the code changes (diffs) suggested by the model.
3.  **Re-prompt or Refactor**: If the suggestion isn't quite right, either refine your prompt or make manual adjustments to the code.
4.  **Verify with Unit Tests**: Run the tests to confirm that the bug is fixed and no new issues have been introduced.
5.  **Stage or Commit**: Save your changes.
6.  **Repeat**: Move to the next function and repeat the process.

This iterative process encourages deliberate, focused problem-solving and ensures each change is verified before moving on.

## Setup

The `knn.py` file contains a basic k-NN implementation with three functions:

1.  `calculate_distances()`: Contains a bug related to how it calculates the distance.
2.  `get_majority_vote()`: Contains a bug in its tie-breaking logic.
3.  `classify_point()`: Depends on the other two functions to work correctly.

The `test_knn.py` file contains a suite of unit tests designed to fail until the bugs in `knn.py` are fixed.

## How to Run the Tests

You can verify your implementation at any time by running the unit tests from the root directory of the project. The tests will show which parts of the implementation are working correctly and which are still buggy.

```bash
python m1_the_loop/test_knn.py
