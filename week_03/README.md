# Week 03 – Recursion vs. Iteration

This week compares recursive and iterative versions of the same algorithms, and analyzes the output, number of calls, and time/space complexity of three recursive functions.

## Files

| File | Contents |
|---|---|
| `recursive_functions` | Pairs of recursive and iterative implementations, grouped by how recursion affects efficiency |
| `tasks` | Python translations of three JavaScript recursion exercises (`m1`, `m2`/`mm`, `m3`), with measured results |

Both files are split into cells with `#%%` (code) and `#%% md` (notes), so they can be run cell by cell in PyCharm, VS Code, or Jupyter (via Jupytext).

---

## `recursive_functions` – Recursive vs. Iterative

The same problem is solved both ways to show three possible outcomes.

### 1. Same efficiency – Depth-First Search on a tree

- `dfs_rec(node, out)` – recursive pre-order traversal
- `dfs_iter(root)` – iterative traversal with an explicit stack

| | Time | Space |
|---|---|---|
| Recursive | O(n) | O(h) – call stack |
| Iterative | O(n) | O(h) – explicit stack |

`h` is the height of the tree. The iterative version does not remove the stack; it only manages it manually. The only practical difference is that the recursive version can hit Python's recursion limit (default 1000) on very deep trees.

### 2. Degrades in space – Binary Search

- `bsearch_iter(a, x)` – iterative
- `bsearch_rec(a, x, lo, hi)` – recursive

| | Time | Space |
|---|---|---|
| Iterative | O(log n) | O(1) |
| Recursive | O(log n) | O(log n) – one stack frame per step |

Python does not perform tail-call optimization, so the recursive version keeps every frame on the stack.

### 3. Degrades in time – Fibonacci

- `fib_iter(n)` – iterative
- `fib_rec(n)` – naive recursive

| | Time | Space |
|---|---|---|
| Iterative | O(n) | O(1) |
| Naive recursive | O(φⁿ) ≈ O(1.618ⁿ), exponential | O(n) |

The slowdown comes from recomputing the same subproblems many times, not from recursion itself. Adding memoization (`@functools.lru_cache`) brings the recursive version back to O(n) time.

---

## `tasks` – Recursion Exercises

All results below were measured by instrumenting the functions with a call counter.

### Task 1 – `m1(a)`: divide and conquer on an array

Splits the array in half and returns `m1(left) + m1(right) + 1`. Arrays of length 0 or 1 return their length.

| Input | Output | Calls |
|---|---|---|
| **array of 8** (test input) | **15** | **15** |
| array of 20 | 39 | 39 |

- Output = calls = **2n − 1** (every call adds exactly 1)
- **Time:** O(n log n) – only O(n) calls, but every slice copies part of the list
- **Space:** O(n) – stack depth is O(log n), but the slices along one path add up to about 2n

### Task 2 – `m2(n)` / `mm(n)`: mutual recursion

The two functions call each other. They produce the Hofstadter Female (`m2`) and Male (`mm`) sequences.

| n | Output | `m2` calls | `mm` calls | Total calls |
|---|---|---|---|---|
| 3 | 2 | 8 | 7 | 15 |
| 8 | 5 | 50 | 49 | 99 |
| 20 | 13 | 814 | 813 | 1,627 |

- `mm` is always called exactly one time less than `m2`
- **Time:** grows faster than any polynomial (measured: when n doubles, the multiplication factor of calls itself roughly doubles). The exact complexity class was not derived.
- **Space:** O(n) recursion depth
- With memoization, each value is computed once and time drops to O(n)

### Task 3 – `m3(n)`: two identical recursive calls

Returns `m3(n - 1) + m3(n - 1)`, with `m3(n) = 1` for `n <= 1`.

| n | Output | Calls |
|---|---|---|
| 20 | 524,288 (2¹⁹) | 1,048,575 (2²⁰ − 1) |

- Output = **2ⁿ⁻¹**, calls = **2ⁿ − 1** (a full binary tree of calls)
- **Time:** O(2ⁿ)
- **Space:** O(n) – only n frames on the stack at once
- Replacing the two calls with `2 * m3(n - 1)` gives the same result in only n calls

---

## Summary

| Function | Test input | Output | Calls | Time | Space |
|---|---|---|---|---|---|
| `m1` | array of 8 | 15 | 15 | O(n log n) | O(n) |
| `m2` / `mm` | n = 20 | 13 | 1,627 | superpolynomial (measured) | O(n) |
| `m3` | n = 20 | 524,288 | 1,048,575 | O(2ⁿ) | O(n) |

## Running

Python 3, no external libraries. Run the cells in order, or run the whole file:

```bash
python tasks.py
```