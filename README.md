# aa_Gresa_Hasani_26

Weekly assignments for the **Advanced Algorithms** course. Each week has its own folder with the solution code and a README that explains the approach, the results and the time/space complexity.

**Author:** Gresa Hasani
**Language:** Python 3

## Weekly assignments

| Week | Topic | Summary |
|---|---|---|
| [Week 03](week_03/) | Recursion vs. Iteration | Recursive and iterative versions of the same algorithms (DFS, binary search, Fibonacci), plus three recursion exercises with measured output, call counts and complexity. Shows how memoization removes repeated subproblems. |
| [Week 04](week_04/) | Dynamic Questionnaire Analysis | Recursive analysis of a branching questionnaire modelled as a DAG: longest and shortest path, counting all paths, reachable questions with minimum depth, and question appearance probabilities. Uses cycle guards and memoization. |

## Repository structure

```
aa_Gresa_Hasani_26/
├── week_03/          # Recursion vs. Iteration
├── week_04/          # Dynamic Questionnaire Analysis
├── .gitignore
└── README.md
```

## How to run

Each week is self-contained. Go into the week's folder and follow the instructions in its README. For example:

```bash
cd week_04
python questionnaire.py
```

No external packages are needed; everything uses the Python standard library.
