CSP Sudoku Solver
This project implements a Constraint Satisfaction Problem (CSP) solver specifically designed to tackle Sudoku puzzles of varying difficulties. The solver utilizes advanced AI search techniques to minimize the search space and find solutions efficiently.

Features
The solver is built using a combination of three core CSP techniques:

Backtracking Search: A depth-first search algorithm that builds a solution one variable at a time, undoing assignments that lead to failures.

AC-3 (Arc Consistency): A pre-processing algorithm that reduces the domains of variables by ensuring that every pair of constrained variables is consistent.

Forward Checking: A "look-ahead" technique used during the search to prune the domains of unassigned variables as soon as a neighbor is assigned a value.

MRV Heuristic (Minimum Remaining Values): A variable selection strategy that picks the cell with the fewest remaining legal choices to fail as early as possible (fail-fast).

File Structure
solver.py: The main Python script containing the SudokuSolver class and implementation logic.

easy.txt, medium.txt, hard.txt, veryhard.txt: Input files containing the Sudoku boards.

Input Format
The program reads Sudoku boards from text files where:

The file contains exactly 9 lines.

Each line contains exactly 9 digits (0–9).

The digit 0 represents an empty cell.

Example Input:

Plaintext
004030050
609400000
005100489
...
How to Run
Ensure you have Python 3 installed.

Place your board text files in the same directory as the script.

Run the script:

Bash
python solver.py
Performance Metrics Explained
The program outputs two primary metrics to evaluate the efficiency of the CSP approach:

Backtrack Calls: The total number of times the recursive backtracking function was invoked. A lower number indicates that the solver made fewer "guesses."

Backtrack Failures: The number of times the solver reached a dead-end and had to undo an assignment.

Understanding "1 Backtrack Call / 0 Failures"
On easier boards, you may notice only 1 Backtrack Call. This indicates that the AC-3 and Forward Checking algorithms were so effective that they mathematically narrowed down every empty cell to its only possible correct value before the search even began. The single call is simply the solver confirming the final valid state.

License
This project was developed for educational purposes as part of an Artificial Intelligence coursework assignment.
