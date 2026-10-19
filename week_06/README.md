# String Matching: Brute Force and Horspool

Finding a pattern `P` inside a text `T`. Brute force places the pattern at every position and compares it from left to right, moving one place to the right after any mismatch. Horspool's algorithm compares from right to left and uses a precomputed shift table to jump forward several positions at once. A second version, `horspool2`, changes only which text character decides the shift, and the trace shows that this change makes it miss a match.

The code is a Python version of the JavaScript functions from the lecture slides (Task 1: Trace).

## Files

| File | Description |
|---|---|
| `search.py` | `brute_force`, `shift_table`, `shift`, `horspool` and `horspool2`, with the real result of every call written as a comment |

## How to run

```
python search.py
```

This runs all four calls from the task on the lecture's example and prints the results. To see every alignment (step 5 of the task), uncomment the `print(i - m + 1)` line, which is the first line inside the `while` loop of `horspool` and `horspool2`.

## Data

The lecture's example:

```
T = 'JIM SAW ME IN A BARBERSHOP'    # n = 26
P = 'BARBER'                        # m = 6
```

`BARBER` starts at index 16.

## Approach

### brute_force

```
for i = 0 .. n - m:
    compare P[0..m-1] with T[i..i+m-1] from left to right
    if all m characters match: return i
return -1
```

The JavaScript `i <= n - m` becomes `range(n - m + 1)`, because `range` stops before its end value.

### shift_table and shift

```
for j = 0 .. m - 2:   table[P[j]] = m - 1 - j
shift(c) = table[c] if c is in the table, otherwise m
```

The table holds the shift for every character of the pattern **except the last one**. A later occurrence overwrites an earlier one, so each value is the distance from the character's last occurrence (in `P[0..m-2]`) to the end of the pattern. `B` appears at index 0 and 3, so `table['B'] = 6 − 1 − 3 = 2`. Any character that is not in the table shifts by `m`. The JavaScript `Map` becomes a Python `dict`.

### horspool

```
i = m - 1                        # text position under the pattern's last character
while i <= n - 1:
    compare P with T[i-m+1..i] from right to left (k = number of matched characters)
    if k == m: return i - m + 1
    i += shift(T[i])
return -1
```

The shift is decided by `T[i]`, the text character under the pattern's **last** position, whether the mismatch happened there or further left.

### horspool2

The same as `horspool` except one line:

```
i += shift(T[i - k])             # the text character where the mismatch happened
```

## Results for the dataset

| Call | Result |
|---|---|
| `shift_table(P)` | `{'B': 2, 'A': 4, 'R': 3, 'E': 1}`, any other character → 6 |
| `brute_force(T, P)` | 16 |
| `horspool(T, P)` | 16 |
| `horspool2(T, P)` | **-1** (misses the match at 16) |

### Every alignment of horspool

| Alignment `i − m + 1` | Window | Matched from the right (`k`) | Shift character `T[i]` | Shift |
|---|---|---|---|---|
| 0 | `JIM SA` | 0 | `A` | 4 |
| 4 | `SAW ME` | 0 | `E` | 1 |
| 5 | `AW ME ` | 0 | space | 6 |
| 11 | `IN A B` | 0 | `B` | 2 |
| 13 | ` A BAR` | 1 | `R` | 3 |
| 16 | `BARBER` | 6 | — | match |

### Every alignment of horspool2

| Alignment `i − m + 1` | Window | Matched from the right (`k`) | Shift character `T[i − k]` | Shift |
|---|---|---|---|---|
| 0 | `JIM SA` | 0 | `A` | 4 |
| 4 | `SAW ME` | 0 | `E` | 1 |
| 5 | `AW ME ` | 0 | space | 6 |
| 11 | `IN A B` | 0 | `B` | 2 |
| 13 | ` A BAR` | 1 | `A` | 4 |
| 17 | `ARBERS` | 0 | `S` | 6 |

After alignment 17, `i` becomes 28, which is past the end of the text, so `horspool2` returns `-1`.

### Why horspool2 misses the match

The two versions behave the same until alignment 13. There, the window is ` A BAR`: the last characters (`R`) match, then `E` and `A` mismatch at `T[17]`, so `k = 1`.

- `horspool` shifts by `T[18] = 'R'`, which is 3. That lands on alignment 16, where the match is.
- `horspool2` shifts by `T[17] = 'A'`, which is 4. That jumps to alignment 17 and skips the match.

The table values are distances measured from the pattern's **last** position. When the mismatch happens `k` places to the left, the character there is `k` places closer to the start of the pattern, so using its table value over-shifts. Looking up the mismatched character would only be safe with a shift of `table[c] − k` (or at least 1), which is the idea behind the bad-character rule of Boyer-Moore.

## Complexity

n = length of the text, m = length of the pattern, σ = size of the alphabet.

| Function | Worst case | Average (random text) | Extra space | Counter on this dataset |
|---|---|---|---|---|
| `brute_force` | Θ(n × m) | Θ(n) | Θ(1) | 17 alignments, 22 character comparisons |
| `shift_table` | Θ(m) | Θ(m) | Θ(min(m, σ)) | — |
| `horspool` | Θ(n × m) | Θ(n), often faster | Θ(min(m, σ)) | 6 alignments, 12 character comparisons |
| `horspool2` | — (not correct) | — | Θ(min(m, σ)) | 6 alignments, 7 character comparisons, wrong result |

The character comparisons count every `P[...] == T[...]` check, including the 6 that confirm the match. `horspool` needs about half the comparisons of brute force here, because 4 of its 5 shifts move the pattern more than one place. `horspool2` does even less work, but only because it skipped over the answer.

Both brute force and Horspool have a Θ(n × m) worst case (for example `T = 'aaaa…a'`, `P = 'baa…a'` for Horspool), but on ordinary text Horspool's shifts are often close to `m`, so it looks at only a fraction of the text.

## Assumptions

- Indices start at 0, as in the JavaScript code, and `-1` means "not found".
- The comparison is case-sensitive and the space counts as a normal character.
- `shift` returns `m` for any character that is not in `P[0..m-2]`, including characters that appear only as the pattern's last character.
- The Python code keeps the slide's names and loop conditions (`k <= m - 1`, `i <= n - 1`) so it can be compared with the slides line by line. Only `shiftTable` and `bruteForce` were renamed to `shift_table` and `brute_force`.