"""
Task 1 - Trace: num, h, chained_table, probe_insert, probe_find, probe_remove
Task 2 - Write: remove, double_hash_insert/find, max_comparisons, insert_grow, next_prime
"""
DELETED = "DELETED"  # tombstone: not a key, but NOT empty either

# Task 1
def num(key):
    """A number is used as it is; a word = sum of letter positions (A=1 ... Z=26)."""
    if isinstance(key, int):
        return key
    s = 0
    for c in key:
        s += ord(c) - 64
    return s

def h(key, m):
    return num(key) % m

def chained_table(keys, m):
    """Open hashing: every cell holds a list, a new key goes to the end of its list."""
    table = [[] for _ in range(m)]
    for k in keys:
        table[h(k, m)].append(k)
    return table

def probe_insert(table, key):
    """Closed hashing, linear probing. Walks past anything that is not None."""
    m = len(table)
    i = h(key, m)
    while table[i] is not None:
        i = (i + 1) % m
    table[i] = key
    return i

def probe_find(table, key):
    """Stops at the first empty (None) cell. DELETED is not empty -> walk past it."""
    m = len(table)
    i = h(key, m)
    while table[i] is not None:
        if table[i] == key:
            return i
        i = (i + 1) % m
    return -1

def probe_remove(table, key):
    """Lecture version: empties the cell with None (this BREAKS later searches)."""
    m = len(table)
    i = h(key, m)
    while table[i] is not None:
        if table[i] == key:
            table[i] = None
            return i
        i = (i + 1) % m
    return -1

# Task 2
def remove(table, key):
    """Like probe_remove, but writes DELETED instead of None, so keys behind it stay reachable."""
    m = len(table)
    i = h(key, m)
    while table[i] is not None:
        if table[i] == key:
            table[i] = DELETED
            return i
        i = (i + 1) % m
    return -1

def _step(key, m):
    """Second hash: s = m - 2 - num(key) % (m - 2), always in 1..m-2 (never 0)."""
    return m - 2 - num(key) % (m - 2)

def double_hash_insert(table, key):
    m = len(table)
    i = h(key, m)
    s = _step(key, m)  # computed once per key
    while table[i] is not None:  # DELETED is not empty -> walk past it
        i = (i + s) % m
    table[i] = key
    return i

def double_hash_find(table, key):
    m = len(table)
    i = h(key, m)
    s = _step(key, m)
    while table[i] is not None:
        if table[i] == key:
            return i
        i = (i + s) % m
    return -1

def max_comparisons(keys, m):
    """Largest number of key comparisons in a successful search, per method."""
    chained = chained_table(keys, m)
    linear = [None] * m
    double = [None] * m
    for k in keys:
        probe_insert(linear, k)
        double_hash_insert(double, k)
    def path_length(table, key, step):
        i, count = h(key, m), 1
        while table[i] != key:
            i = (i + step) % m
            count += 1
        return count
    return {"chained": max(len(lst) for lst in chained),
            "linear": max(path_length(linear, k, 1) for k in keys),
            "double": max(path_length(double, k, _step(k, m)) for k in keys)}

def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True

def next_prime(n):
    """Smallest prime >= n."""
    while not is_prime(n):
        n += 1
    return n

def insert_grow(table, key):
    """Keeps load factor n/m <= 0.5. Returns the same table, or the new one if it grew."""
    m = len(table)
    n = sum(1 for x in table if x is not None and x != DELETED)
    if (n + 1) / m > 0.5:
        new_table = [None] * next_prime(2 * m)
        for x in table:  # from cell 0 to the end
            if x is not None and x != DELETED:
                probe_insert(new_table, x)
        table = new_table
    probe_insert(table, key)
    return table

# checks
W = ['A', 'FOOL', 'AND', 'HIS', 'MONEY', 'ARE', 'SOON', 'PARTED']
N = [30, 20, 56, 75, 31, 19]

def build_T():
    T = [None] * 13
    for w in W:
        probe_insert(T, w)
    return T

if __name__ == "__main__":
    print("=== Task 1: Trace ===")
    T = build_T()
    print("T =", T)
    print("chainedTable(W, 13)[11] ->", chained_table(W, 13)[11])
    print("probeFind(T, 'PARTED') ->", probe_find(T, 'PARTED'))
    print("probeFind(T, 'KID') ->", probe_find(T, 'KID'))
    print("probeRemove(T, 'ARE') ->", probe_remove(T, 'ARE'))
    print("probeFind(T, 'SOON') ->", probe_find(T, 'SOON'))
    print("=== Task 2: remove ===")
    T = build_T()
    print("remove(T, 'ARE') ->", remove(T, 'ARE'), "(expected 11)")
    print("probeFind(T, 'SOON') ->", probe_find(T, 'SOON'), "(expected 12)")
    print("probeFind(T, 'ARE') ->", probe_find(T, 'ARE'), "(expected -1)")
    print("remove(T, 'KID') ->", remove(T, 'KID'), "(expected -1)")
    print("=== Task 2: double hashing ===")
    D = [None] * 11
    for k in N:
        double_hash_insert(D, k)
    print("D =", D)
    print("doubleHashFind(D, 19) ->", double_hash_find(D, 19), "(expected 5)")
    print("doubleHashFind(D, 42) ->", double_hash_find(D, 42), "(expected -1)")
    print("=== Task 2: maxComparisons ===")
    print("maxComparisons(N, 11) ->", max_comparisons(N, 11), "(expected 3, 6, 2)")
    print("maxComparisons(W, 13) ->", max_comparisons(W, 13), "(expected 2, 2, 3)")
    print("=== Task 2: insertGrow ===")
    G = [None] * 5
    sizes = []
    for w in W:
        G = insert_grow(G, w)
        sizes.append(len(G))
    print("sizes:", sizes, "(expected 5 5 11 11 11 23 23 23)")
    print("G.length ->", len(G), "(expected 23)")
    print("probeFind(G, 'ARE') ->", probe_find(G, 'ARE'), "(expected 4)")