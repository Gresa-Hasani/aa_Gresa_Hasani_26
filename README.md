# aa_Gresa_Hasani_26

Weekly assignments for the Advanced Algorithms course. Each week has its own folder with the solution code and a README that explains the approach, the results and the time/space complexity.

**Author:** Gresa Hasani
**Language:** Python 3

## Weekly assignments

| Week | Topic | Summary |
|---|---|---|
| [Week 03](week_03/) | Recursion vs. Iteration | Recursive and iterative versions of the same algorithms (DFS, binary search, Fibonacci), plus three recursion exercises with measured output, call counts and complexity. Shows how memoization removes repeated subproblems. |
| [Week 04](week_04/) | Dynamic Questionnaire Analysis | Recursive analysis of a branching questionnaire modelled as a DAG: longest and shortest path, counting all paths, reachable questions with minimum depth, and question appearance probabilities. Uses cycle guards and memoization. |
| [Week 05](week_05/) | Counting Sorts | Comparison counting sort and distribution counting sort, with stable and unstable variants and counters for comparisons and passes. Distribution counting is then used as the stable pass of an LSD radix sort to sort dates and to sort words in Albanian dictionary order. No `sort()` is used. |

## Repository structure

```
aa_Gresa_Hasani_26/
├── week_03/          # Recursion vs. Iteration
├── week_04/          # Dynamic Questionnaire Analysis
├── week_05/          # Counting Sorts
├── .gitignore
└── README.md
```

## How to run

Each week is self-contained. Go into the week's folder and follow the instructions in its README. For example:

```
cd week_05
python counting.py
```

No external packages are needed; everything uses the Python standard library.