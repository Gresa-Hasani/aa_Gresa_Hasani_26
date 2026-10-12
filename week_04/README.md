# Dynamic Questionnaire Analysis

Recursive analysis of a questionnaire with conditional (branching) logic. Each question leads to a next question depending on the answer, so the questionnaire forms a directed graph. For the given dataset this graph is a **DAG**: some questions (q6, q8, q9) are reachable through several different paths.

All five problems are solved with **recursion**. Loops are used only for bookkeeping: building the question index, iterating over a question's answers, and sorting results.

## Files

| File | Description |
|---|---|
| `questionnaire.py` | Solutions to all five problems |
| `data.json` | The questionnaire dataset from the assignment |

## How to run

```bash
python questionnaire.py
```

This loads `data.json` and prints the result of every problem.

## Data model

- `radio` / `select` questions have a list of answers, each with its own `next_question_id`.
- `text` / `checkbox` questions have a single unconditional `next_question_id`.
- `next_question_id = null` ends the questionnaire.

Two helpers hide this difference from the recursive functions:

- `build_index` maps question id → question, for O(1) lookups.
- `get_branches` returns every question's outgoing branches as `(answer_id, next_question_id)` pairs. Text and checkbox questions have one branch with `answer_id = None`.

## Approach

### Problem 1 & 2: Longest and shortest path

```
best(None) = empty path
best(q)    = [q] + the longest / shortest of best(next) over all branches
```

Both use one shared recursive helper, `_best_path`, which compares children by path length. Only radio and select questions add an entry to `answer_path`.

- **Cycle guard:** `on_path` holds the questions on the current path, and a question is never re-entered. It is removed again when the call returns (backtracking).
- **Memoization:** the best result per question id is cached. A result is cached only if no branch was cut by the cycle guard, because such a result depends on the current path.

### Problem 3: Count all possible paths

```
paths(None) = 1
paths(q)    = sum of paths(next) over all branches
```

Every answer counts as its own branch, even when two answers lead to the same question. If a question already on the current path is reached again, the function returns `-1` (a cycle means infinitely many paths). Results are memoized per question id.

### Problem 4: Questions reachable from an answer

Recursion with depth tracking, starting at the answer's next question with depth 1. A question is recorded with its depth and recursed through only if it is new or reached at a **smaller** depth than before. Reaching it again at an equal or greater depth stops the recursion, which also guarantees termination if the data contains a cycle. Results are sorted by `min_depth`, then by `question_id`. Unknown question or answer ids return `[]`.

### Problem 5: Appearance probability

Probability is propagated forward from the start question:

- A question with `k` answers passes `p / k` along each answer.
- A text/checkbox question passes all of its probability to its next question.

Contributions are accumulated in maps keyed by question id, because several branches can lead to the same question. The expected position is the probability-weighted average position:

```
expected_position = sum(p × position) / sum(p)
```

Unreachable questions are reported with probability 0 and expected position 0. Values are rounded to 4 decimal places.

## Results for the dataset

| Problem | Result |
|---|---|
| Longest path | length 6: `q1 → q2 → q3 → q6 → q8 → q9` |
| Shortest path | length 4: `q1 → q5 → q6 → q8` |
| Number of paths | 22 |
| Reachable from `q2` / `a2_truck` | q4 (1), q6 (2), q7 (2), q8 (3), q9 (4) |

Problem 1 has several paths of maximum length; any of them is a correct answer.

| Question | Probability | Expected position |
|---|---|---|
| q1 | 1.0 | 1.0 |
| q8 | 1.0 | 4.5 |
| q6 | 0.875 | 3.4286 |
| q2 | 0.5 | 2.0 |
| q5 | 0.5 | 2.0 |
| q9 | 0.5 | 5.5 |
| q3 | 0.25 | 3.0 |
| q4 | 0.25 | 3.0 |
| q7 | 0.125 | 4.0 |

The probabilities sum to 5.0, the expected number of questions a user answers.

## Complexity

`n` = number of questions, `m` = average number of answers per question.

| Function | With memoization | Without memoization |
|---|---|---|
| Longest / shortest path | O(n × m) time, 19 recursive calls | grows with the number of paths, 62 calls |
| Count paths | O(n × m) time, 19 recursive calls | grows with the number of paths, 62 calls |
| Reachable questions | 8 calls for `q2` / `a2_truck` | — |
| Probabilities | — | one walk per path, 62 calls |

With memoization each branch (edge) is followed once: 1 call for the start question plus 1 per edge (18 edges in this dataset). Without it, shared sub-paths are re-explored for every path that reaches them (22 paths here), which can grow exponentially for larger questionnaires.

Extra space is O(n) for the memo and result maps, plus O(depth) for the recursion stack. The recursive call counts per function are recorded in `call_counter`.

## Assumptions

- A `next_question_id` that does not exist in the data is treated as the end of the questionnaire.
- A radio/select question with no answers is treated as a final question.
- Python's default recursion limit (about 1000 nested calls) is far above what this dataset needs.