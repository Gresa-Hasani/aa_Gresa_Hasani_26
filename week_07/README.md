# Hashing: Chaining, Linear Probing and Double Hashing

Storing keys in a table of size `m` so that a key can be found by computing its cell instead of searching. A hash function `h(key, m)` maps every key to a cell. When two keys land in the same cell (a collision), **open hashing** keeps a list in every cell, while **closed hashing** puts the key in another free cell of the same table, found either by walking one cell at a time (linear probing) or by jumping with a step that depends on the key (double hashing).

The trace shows that removing a key by emptying its cell breaks later searches. The written functions fix this with a `DELETED` marker, add double hashing, count the comparisons of each method, and grow the table to keep the load factor at 0.5 or below.

The code is a Python version of the JavaScript functions from the lecture slides (Task 1: Trace and Task 2: Write).

## Files

| File | Description |
|---|---|
| `hashing.py` | `num`, `h`, `chained_table`, `probe_insert`, `probe_find`, `probe_remove` (Task 1), and `remove`, `double_hash_insert`, `double_hash_find`, `max_comparisons`, `next_prime`, `insert_grow` (Task 2), with a self-check that runs every check from the slides |

## How to run

```
python hashing.py
```

This builds the lecture's tables, runs the five trace calls and every check from Task 2, and prints each result next to the expected value. Output:

```
=== Task 1: Trace ===
T = ['PARTED', 'A', None, None, None, None, 'AND', 'MONEY', None, 'FOOL', 'HIS', 'ARE', 'SOON']
chainedTable(W, 13)[11] -> ['ARE', 'SOON']
probeFind(T, 'PARTED') -> 0
probeFind(T, 'KID') -> -1
probeRemove(T, 'ARE') -> 11
probeFind(T, 'SOON') -> -1
=== Task 2: remove ===
remove(T, 'ARE') -> 11 (expected 11)
probeFind(T, 'SOON') -> 12 (expected 12)
probeFind(T, 'ARE') -> -1 (expected -1)
remove(T, 'KID') -> -1 (expected -1)
=== Task 2: double hashing ===
D = [None, 56, None, 31, 75, 19, None, None, 30, 20, None]
doubleHashFind(D, 19) -> 5 (expected 5)
doubleHashFind(D, 42) -> -1 (expected -1)
=== Task 2: maxComparisons ===
maxComparisons(N, 11) -> {'chained': 3, 'linear': 6, 'double': 2} (expected 3, 6, 2)
maxComparisons(W, 13) -> {'chained': 2, 'linear': 2, 'double': 3} (expected 2, 2, 3)
=== Task 2: insertGrow ===
sizes: [5, 5, 11, 11, 11, 23, 23, 23] (expected 5 5 11 11 11 23 23 23)
G.length -> 23 (expected 23)
probeFind(G, 'ARE') -> 4 (expected 4)
```

Every real result matches the expected value from the slides.

## Data

The lecture's example:

```
W = ['A', 'FOOL', 'AND', 'HIS', 'MONEY', 'ARE', 'SOON', 'PARTED']   # words, m = 13
N = [30, 20, 56, 75, 31, 19]                                        # numbers, m = 11
```

`T` is a table of 13 cells, filled by inserting every word of `W` with `probe_insert`. An empty cell is `None` (the JavaScript `null`).

## Approach

### num and h

```
num(key) = key                               if key is a number
num(key) = sum of (letter position, A=1 … Z=26)   otherwise
h(key, m) = num(key) % m
```

The letter position is `ord(c) - 64`, the Python version of `c.charCodeAt(0) - 64`.

| Key | A | FOOL | AND | HIS | MONEY | ARE | SOON | PARTED |
|---|---|---|---|---|---|---|---|---|
| `num` | 1 | 48 | 19 | 36 | 72 | 24 | 63 | 64 |
| `h(key, 13)` | 1 | 9 | 6 | 10 | 7 | 11 | 11 | 12 |

### chained_table (open hashing)

```
table = m empty lists
for every key: append it to table[h(key, m)]
```

A new key goes to the end of its list, so colliding keys keep their insertion order.

### probe_insert, probe_find and probe_remove (closed hashing, linear probing)

```
i = h(key, m)
while table[i] is not None:
    find / remove: if table[i] == key, stop here
    i = (i + 1) % m                # after the last cell comes cell 0
insert: table[i] = key
```

A search stops at the first empty cell. `probe_remove` is the same as `probe_find`, but when it finds the key it sets the cell back to `None`.

### remove

`probe_remove` with one change: the cell gets `DELETED` instead of `None`. `DELETED` is not a key, so a search never matches it, but it is not empty either, so a search walks past it and still finds the keys that were inserted behind the removed one. The table keeps its length and only the cells on the key's path are read.

### double_hash_insert and double_hash_find

```
i = h(key, m)
s = m - 2 - num(key) % (m - 2)       # second hash, computed once per key
while table[i] is not None:          # DELETED is not empty: walk past it
    find: if table[i] == key, return i
    i = (i + s) % m
insert: table[i] = key, return i
find:   return -1
```

`num(key) % (m - 2)` is between 0 and `m - 3`, so the step `s` is always between 1 and `m - 2` and never 0. Because `m` is prime, every step `s < m` shares no factor with `m`, so the walk visits every cell before it repeats.

### max_comparisons

```
build the chained, linear and double tables of size m from keys
chained = length of the longest list
linear / double = for every key, count the cells from h(key, m) up to and including its own cell; keep the largest
```

Every count is the number of key comparisons a successful search for that key makes. `keys` is only read, never changed.

### next_prime and insert_grow

```
next_prime(n): try n, n + 1, … until a number has no divisor d with 2 ≤ d ≤ √n

insert_grow(table, key):
    n = number of real keys (None and DELETED are not keys)
    if (n + 1) / m > 0.5:
        new table of size next_prime(2 * m)
        insert the old keys into it with probe_insert, from cell 0 to the end
    probe_insert(table, key) and return the table
```

The function returns the same table if it did not grow and the new one if it did. Only real keys are copied, so a new table has no `DELETED` cells.

## Results for the dataset

### Task 1: Trace

The table after inserting `W`:

| Cell | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `T` | PARTED | A | – | – | – | – | AND | MONEY | – | FOOL | HIS | ARE | SOON |

`SOON` hashes to 11, which `ARE` already holds, so it moves to 12. `PARTED` hashes to 12, which is now taken, so it wraps around to 0.

| Call | Predicted = Real | Why |
|---|---|---|
| `chainedTable(W, 13)[11]` | `['ARE', 'SOON']` | both hash to 11, in insertion order |
| `probeFind(T, 'PARTED')` | 0 | 12 (SOON) → 0 |
| `probeFind(T, 'KID')` | -1 | `num('KID')` = 24, so 11 → 12 → 0 → 1 → cell 2 is empty |
| `probeRemove(T, 'ARE')` | 11 | cell 11 becomes `None` |
| `probeFind(T, 'SOON')` | **-1** | the search starts at 11, which is now empty, and stops before reaching `SOON` in cell 12 |

The last call is the point of the task: `SOON` is still in the table, but emptying cell 11 cut the path to it.

### Task 2: Write

| Call | Result |
|---|---|
| `remove(T, 'ARE')` (table built again) | 11 |
| `probeFind(T, 'SOON')` | 12 |
| `probeFind(T, 'ARE')` | -1 |
| `remove(T, 'KID')` | -1 |
| `D` after `doubleHashInsert` of `N` (m = 11) | `[None, 56, None, 31, 75, 19, None, None, 30, 20, None]` |
| `doubleHashFind(D, 19)` | 5 |
| `doubleHashFind(D, 42)` | -1 |
| `maxComparisons(N, 11)` | `{chained: 3, linear: 6, double: 2}` |
| `maxComparisons(W, 13)` | `{chained: 2, linear: 2, double: 3}` |
| `insertGrow` sizes, one per word of `W` | 5 5 11 11 11 23 23 23 |
| `G.length` | 23 |
| `probeFind(G, 'ARE')` | 4 |

All results match the checks on the slides.

### Comparisons per key

For `N` with m = 11, the three tables are:

| Method | Table |
|---|---|
| chained | cell 1: [56], cell 8: [30, 19], cell 9: [20, 75, 31] |
| linear | `[31, 56, 19, None, None, None, None, None, 30, 20, 75]` |
| double | `[None, 56, None, 31, 75, 19, None, None, 30, 20, None]` |

| Key | 30 | 20 | 56 | 75 | 31 | 19 |
|---|---|---|---|---|---|---|
| `h(key, 11)` | 8 | 9 | 1 | 9 | 9 | 8 |
| step `s` | 6 | 7 | 7 | 6 | 5 | 8 |
| linear comparisons | 1 | 1 | 1 | 2 | 3 | **6** |
| double comparisons | 1 | 1 | 1 | 2 | 2 | 2 |

Cells 8, 9 and 10 fill up next to each other, so `31` and `19` have to walk through the whole cluster: `19` starts at 8 and checks 8, 9, 10, 0, 1 before it reaches 2. This is **primary clustering**. With double hashing every key jumps with its own step, so the cluster does not form and no key needs more than 2 comparisons.

For `W` with m = 13 it is the other way round: linear needs at most 2, double needs 3. `SOON` hashes to 11 (taken by `ARE`) with step 3, so it checks 11 → 1 (`A`) → 4. Double hashing avoids clustering on average, but on a single small table its jumps can still land on occupied cells.

### insert_grow

| Word | n before | (n + 1) / m | Table size after |
|---|---|---|---|
| A | 0 | 1/5 | 5 |
| FOOL | 1 | 2/5 | 5 |
| AND | 2 | 3/5 > 0.5 | 11 (= next prime ≥ 10) |
| HIS | 3 | 4/11 | 11 |
| MONEY | 4 | 5/11 | 11 |
| ARE | 5 | 6/11 > 0.5 | 23 (= next prime ≥ 22) |
| SOON | 6 | 7/23 | 23 |
| PARTED | 7 | 8/23 | 23 |

In the final table of 23 cells, `A`, `FOOL` and `MONEY` sit in cells 1, 2 and 3. `ARE` hashes to 1 (24 % 23), so it walks 1 → 2 → 3 and lands in cell 4.

## Complexity

n = number of keys, m = table size, α = n / m (load factor).

| Function | Average | Worst case | Extra space |
|---|---|---|---|
| `num`, `h` | Θ(length of the key) | Θ(length of the key) | Θ(1) |
| `chained_table` | Θ(n + m) | Θ(n + m) | Θ(n + m) |
| `probe_insert`, `probe_find`, `probe_remove`, `remove` | Θ(1) when α ≤ 0.5 | Θ(m) | Θ(1) |
| `double_hash_insert`, `double_hash_find` | Θ(1) when α ≤ 0.5 | Θ(m) | Θ(1) |
| `max_comparisons` | Θ(n + m) | Θ(n × m) | Θ(m) |
| `next_prime(n)` | Θ(√n) per number tried | — | Θ(1) |
| `insert_grow` | Θ(1) amortized | Θ(m) when it grows | Θ(m) for the new table |

With linear probing, a successful search needs about ½ (1 + 1 / (1 − α)) comparisons on average, which is 1.5 at α = 0.5 but grows quickly as the table fills, because of clustering. Double hashing needs about (1 / α) ln(1 / (1 − α)), which is about 1.39 at α = 0.5. A chained search needs about 1 + α / 2. These formulas assume keys spread uniformly over the table.

`insert_grow` copies the whole table when it grows, but the size at least doubles each time, so the copies add up to Θ(n) over n inserts, and each insert costs Θ(1) amortized.

## Assumptions

- Words are uppercase letters A to Z. A lowercase letter or a space gives a wrong letter position (for example `ord(' ') - 64` is −32).
- The JavaScript `typeof key === 'number'` becomes `isinstance(key, int)`. In Python `bool` is a subclass of `int`, so `True` would be used as 1.
- The JavaScript `%` can return a negative number for a negative key, while Python's `%` always returns a value in `0..m-1`.
- Every probing loop assumes the table has at least one `None` cell. On a table with no `None` cell left (full of keys, `DELETED` cells, or both), `probe_insert` and an unsuccessful `probe_find` loop forever, exactly like the JavaScript versions. `insert_grow` prevents this by keeping α ≤ 0.5.
- Double hashing needs a prime `m ≥ 3`. With `m = 2` the step divides by zero, and with a non-prime `m` the walk can miss free cells.
- `probe_insert` does not check for duplicates and does not reuse `DELETED` cells, as on the slides.
- `DELETED` is the string `"DELETED"`, so it must not be used as a key.
- `max_comparisons` needs at least one key, distinct keys, and fewer keys than `m`, as stated on the slide.