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
| [Week 06](week_06/) | String Matching: Brute Force and Horspool | Brute-force matching and Horspool's algorithm with its shift table, traced alignment by alignment on the lecture's example. A modified version, `horspool2`, shifts by the mismatched character instead of the last one and misses the match, which shows why Horspool's shift must use the text character under the pattern's last position. |
| [Week 07](week_07/) | Hashing: Chaining, Linear Probing and Double Hashing | Open hashing with chained lists and closed hashing with linear probing, traced on the lecture's example. Shows that removing a key by emptying its cell breaks later searches, and fixes it with a `DELETED` marker. Adds double hashing, compares the maximum number of key comparisons of the three methods (primary clustering), and grows the table to the next prime to keep the load factor at 0.5 or below. |

## Repository structure

```
aa_Gresa_Hasani_26/
├── week_03/          # Recursion vs. Iteration
│   ├── recursive_function.ipynb
│   ├── tasks.ipynb
│   └── README.md
├── week_04/          # Dynamic Questionnaire Analysis
│   ├── questionnaire.py
│   ├── data.json
│   └── README.md
├── week_05/          # Counting Sorts
│   ├── counting.py
│   └── README.md
├── week_06/          # String Matching: Brute Force and Horspool
│   ├── search.py
│   └── README.md
├── week_07/          # Hashing: Chaining, Linear Probing and Double Hashing
│   ├── hashing.py
│   └── README.md
├── .gitignore
└── README.md
```

## How to run

Each week is self-contained. Go into the week's folder and follow the instructions in its README. For example:

```
cd week_07
python hashing.py
```

Week 03 is a set of Jupyter notebooks and is opened in Jupyter, VS Code or PyCharm instead. No external packages are needed; everything uses the Python standard library.