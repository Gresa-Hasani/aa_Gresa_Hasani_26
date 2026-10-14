# Counting Sorts

Sorting without comparing keys. Comparison counting sort finds each element's final position by comparing it with every other element. Distribution counting sort instead counts how often each key value occurs and uses those counts to place every element directly, so no two keys are ever compared. Distribution counting is then used as the stable pass of an LSD radix sort, to sort dates and to sort words in Albanian dictionary order.

No `sort()` or `localeCompare` is used anywhere. Two global counters record the work: `comparisons` (+1 every time two keys are compared) and `passes` (+1 for every counting pass: count → running sums → place).

## Files

| File | Description |
|---|---|
| `counting.py` | All functions, with a self-check that runs every check from the assignment |

## How to run

```
python counting.py
```

This runs every function on the assignment's data and prints the results.

## Data

- `six`: six students with grades 9 6 9 9 6 5 (Arta, Blend, Dita, Edon, Fjolla, Gent). The key is the grade.
- `recs`: ten records with ids 0..9 and a date string `'YYYY-MM-DD'`.
- `words`: 24 Albanian words, sorted using the 36-letter alphabet `a b c ç d dh e ë f g gj h i j k l ll m n nj o p q r rr s sh t th u v x xh y z zh`.

## Approach

### Task 1: c1, c2, c3

```
c1:     count[i] = number of elements that must come before A[i];  S[count[i]] = A[i]
c2, c3: D[k] = how many keys are ≤ k  (count, then running sums);  S[D[k] - 1] = x, then D[k] -= 1
```

All three sort correctly by key. They differ only in how they handle equal keys:

- `c1` compares every pair `i < j`. On a tie, `key(A[i]) < key(A[j])` is false, so the earlier element `i` gets the +1 and ends up after the later one. Not stable.
- `c2` places elements walking from right to left. The last element with a given key takes the last free slot of its block, so equal keys keep their input order. Stable.
- `c3` walks from left to right but still fills each block from its last slot, so the first element with a given key lands last. Not stable.

`c1` and `c3` give the same order: every group of equal grades comes out reversed.

### comparisonCountingSort

`c1` with `<=` instead of `<`. On a tie the later element `j` gets the +1, so earlier elements stay in front and the sort is stable. Every pair `i < j` is compared exactly once with no early exit, so it always makes exactly n(n − 1) / 2 comparisons.

### distributionCountingSort

`c2` with `passes += 1` once per call. Keys are only used as indices into `D`, never compared with each other. `key − lo` shifts every key into `0..hi − lo`, so `D` has `hi − lo + 1` cells whatever `lo` is (3 cells for keys 1001..1003). An empty list runs every loop zero times, returns `[]`, and still counts one pass.

### sortByDate

```
S = distributionCountingSort(records, day,   1, 31)
S = distributionCountingSort(S,       month, 1, 12)
S = distributionCountingSort(S,       year,  min_year, max_year)
```

Day, month and year are taken from the string by slicing (`[8:10]`, `[5:7]`, `[0:4]`), so no two date strings are compared. The smallest and largest year are found first with one loop over the year numbers.

The passes go from the least significant part to the most significant. Each pass sorts the whole list by one key only, so the last pass (year) decides the main order. Earlier passes only break ties, and that works only because every pass is stable. In the opposite order (year → month → day) the result would be sorted by day of the month.

### tokenize

Reads the word from left to right. If the next two characters are one of `dh gj ll nj rr sh th xh zh`, they count as one letter and both are consumed; otherwise one character is taken. Each letter is looked up in a dictionary built from the alphabet (`a = 1 … zh = 36`).

### sortAlbanian

```
for p = longest − 1 down to 0:
    S = distributionCountingSort(S, letter at position p, or 0 if the word is shorter, 0, 36)
```

Every word is tokenized once, and the longest word sets the number of passes. A word with no letter at position `p` gets 0, which is smaller than every letter, so a word comes before any longer word that starts with it: `dhe` = [6, 7, 0, …] comes before `dhelpër` = [6, 7, 16, …].

Code-point order (what `sort()` would use) is wrong for Albanian: it puts `ç` and `ë` after `z` and splits digraphs into two letters. It would put `dhe` before `drita` (`h` < `r`), but in Albanian `d` < `dh`, so `drita` comes first.

## Results for the dataset

| Call | Result |
|---|---|
| `c1(six, g)` | Gent Fjolla Blend Edon Dita Arta |
| `c2(six, g, 5, 10)` | Gent Blend Fjolla Arta Dita Edon |
| `c3(six, g, 5, 10)` | Gent Fjolla Blend Edon Dita Arta |
| `comparisonCountingSort(six, g)` | Gent Blend Fjolla Arta Dita Edon, 15 comparisons |
| `distributionCountingSort(six, g, 5, 10)` | Gent Blend Fjolla Arta Dita Edon |
| `distributionCountingSort([1003, 1001, 1002, 1001], x → x, 1001, 1003)` | [1001, 1001, 1002, 1003] |
| `distributionCountingSort([], g, 5, 10)` | [] |
| `sortByDate(recs)` ids | 3 1 4 8 0 6 2 5 7 9, 3 passes |
| `tokenize('llamba')` | [17, 1, 18, 2, 1] |
| `tokenize('shtëpi')` | [27, 28, 8, 22, 13] |
| `sortAlbanian(words)` | 6 passes (longest word: `dhelpër`, 6 letters) |

`sortAlbanian(words)` in full:

```
cep çaj dera drita dhe dhelpër emër ëndërr gur gjak lule llamba nënë njeri
rosa rrugë sot shi tokë thikë xixa xhami zemër zhurmë
```

The three distribution calls (six, 1001..1003, empty) together give `{'comparisons': 0, 'passes': 3}`.

## Complexity

n = number of elements, k = hi − lo + 1 (size of the key range), L = number of letters in the longest word.

| Function | Time | Extra space | Stable | Counter |
|---|---|---|---|---|
| `c1` | Θ(n²) | Θ(n) | No | n(n − 1) / 2 comparisons |
| `c2` | Θ(n + k) | Θ(n + k) | Yes | 1 pass |
| `c3` | Θ(n + k) | Θ(n + k) | No | 1 pass |
| `comparisonCountingSort` | Θ(n²) | Θ(n) | Yes | n(n − 1) / 2 comparisons (15 for n = 6) |
| `distributionCountingSort` | Θ(n + k) | Θ(n + k) | Yes | 1 pass, 0 comparisons |
| `sortByDate` | Θ(n + 31 + 12 + years) | Θ(n + 31) | Yes | 3 passes |
| `tokenize` | Θ(word length) | Θ(word length) | — | — |
| `sortAlbanian` | Θ(L × (n + 37)) | Θ(n + 37) | Yes | L passes (6 here) |

Distribution counting is linear only when k is not much larger than n. With grades (k = 6), months (k = 12) or letters (k = 37) the range is small, so it beats any comparison sort, which needs Ω(n log n) comparisons in the worst case.

## Assumptions

- Every key returned by `key` is a whole number in `lo..hi`. A key outside that range raises an `IndexError` or lands in the wrong cell.
- Dates are always in the format `'YYYY-MM-DD'` with zero-padded month and day.
- Words are lowercase. `tokenize` normalizes to NFC, so an `ë` written as `e` + a combining diaeresis still matches, and it raises a `ValueError` for any character outside the Albanian alphabet.
- Finding the smallest and largest year compares year numbers, not date strings, and is not counted in `comparisons`.
- `passes` counts one pass per call of `c2`, `c3` or `distributionCountingSort`, including a call on an empty list.