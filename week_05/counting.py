import unicodedata

# ---------- Counters ----------
comparisons = 0
passes = 0

def resetCounters():
    global comparisons, passes
    comparisons = 0
    passes = 0

def getCounters():
    return {"comparisons": comparisons, "passes": passes}

# ---------- Task 1 ----------
def c1(A, key):
    global comparisons
    n = len(A)
    count = [0] * n
    for i in range(n - 1):
        for j in range(i + 1, n):
            comparisons += 1
            if key(A[i]) < key(A[j]):
                count[j] += 1
            else:
                count[i] += 1
    S = [None] * n
    for i in range(n):
        S[count[i]] = A[i]
    return S

def c2(A, key, lo, hi):
    global passes
    passes += 1
    D = [0] * (hi - lo + 1)
    for x in A:
        D[key(x) - lo] += 1
    for j in range(1, len(D)):
        D[j] += D[j - 1]
    S = [None] * len(A)
    for i in range(len(A) - 1, -1, -1):
        j = key(A[i]) - lo
        S[D[j] - 1] = A[i]
        D[j] -= 1
    return S

def c3(A, key, lo, hi):
    global passes
    passes += 1
    D = [0] * (hi - lo + 1)
    for x in A:
        D[key(x) - lo] += 1
    for j in range(1, len(D)):
        D[j] += D[j - 1]
    S = [None] * len(A)
    for i in range(len(A)):
        j = key(A[i]) - lo
        S[D[j] - 1] = A[i]
        D[j] -= 1
    return S

# ---------- Task 2 ----------
def comparisonCountingSort(A, key):
    global comparisons
    n = len(A)
    count = [0] * n
    for i in range(n - 1):
        for j in range(i + 1, n):
            comparisons += 1
            if key(A[i]) <= key(A[j]):
                count[j] += 1
            else:
                count[i] += 1
    S = [None] * n
    for i in range(n):
        S[count[i]] = A[i]
    return S

def distributionCountingSort(A, key, lo, hi):
    global passes
    passes += 1
    D = [0] * (hi - lo + 1)
    for x in A:
        D[key(x) - lo] += 1
    for j in range(1, len(D)):
        D[j] += D[j - 1]
    S = [None] * len(A)
    for i in range(len(A) - 1, -1, -1):
        j = key(A[i]) - lo
        S[D[j] - 1] = A[i]
        D[j] -= 1
    return S

def _year(r):
    return int(r["date"][0:4])

def _month(r):
    return int(r["date"][5:7])

def _day(r):
    return int(r["date"][8:10])

def sortByDate(records):
    if len(records) == 0:
        lo_year, hi_year = 0, 0
    else:
        lo_year = hi_year = _year(records[0])
        for r in records:
            y = _year(r)
            if y < lo_year:
                lo_year = y
            if y > hi_year:
                hi_year = y
    S = distributionCountingSort(records, _day, 1, 31)
    S = distributionCountingSort(S, _month, 1, 12)
    S = distributionCountingSort(S, _year, lo_year, hi_year)
    return S

ALPHABET = ["a", "b", "c", "ç", "d", "dh", "e", "ë", "f", "g", "gj", "h",
            "i", "j", "k", "l", "ll", "m", "n", "nj", "o", "p", "q", "r",
            "rr", "s", "sh", "t", "th", "u", "v", "x", "xh", "y", "z", "zh"]
LETTER_NUM = {letter: i + 1 for i, letter in enumerate(ALPHABET)}
DIGRAPHS = {"dh", "gj", "ll", "nj", "rr", "sh", "th", "xh", "zh"}

def tokenize(word):
    word = unicodedata.normalize("NFC", word)
    out = []
    i = 0
    while i < len(word):
        two = word[i:i + 2]
        if two in DIGRAPHS:
            out.append(LETTER_NUM[two])
            i += 2
        else:
            ch = word[i]
            if ch not in LETTER_NUM:
                raise ValueError(f"'{ch}' is not in the Albanian alphabet")
            out.append(LETTER_NUM[ch])
            i += 1
    return out

def sortAlbanian(words):
    items = [(w, tokenize(w)) for w in words]
    max_len = 0
    for _, t in items:
        if len(t) > max_len:
            max_len = len(t)
    for p in range(max_len - 1, -1, -1):
        items = distributionCountingSort(items, lambda it: it[1][p] if p < len(it[1]) else 0, 0, 36)
    return [w for w, _ in items]

__all__ = [
    "c1", "c2", "c3", "comparisonCountingSort", "distributionCountingSort",
    "sortByDate", "tokenize", "sortAlbanian", "resetCounters", "getCounters",
]

if __name__ == "__main__":
    six = [
        {"name": "Arta", "grade": 9},
        {"name": "Blend", "grade": 6},
        {"name": "Dita", "grade": 9},
        {"name": "Edon", "grade": 9},
        {"name": "Fjolla", "grade": 6},
        {"name": "Gent", "grade": 5},
    ]
    g = lambda r: r["grade"]
    names = lambda S: " ".join(r["name"] for r in S)

    print("c1:", names(c1(six, g)))
    print("c2:", names(c2(six, g, 5, 10)))
    print("c3:", names(c3(six, g, 5, 10)))

    resetCounters()
    print("comparisonCountingSort:", names(comparisonCountingSort(six, g)))
    print("comparisons:", getCounters()["comparisons"])

    resetCounters()
    print("distributionCountingSort:", names(distributionCountingSort(six, g, 5, 10)))
    print("big lo:", distributionCountingSort([1003, 1001, 1002, 1001], lambda x: x, 1001, 1003))
    print("empty:", distributionCountingSort([], g, 5, 10))
    print("counters:", getCounters())

    recs = [
        {"id": 0, "date": "2024-10-13"}, {"id": 1, "date": "2024-01-20"}, {"id": 2, "date": "2026-05-15"},
        {"id": 3, "date": "2024-01-15"}, {"id": 4, "date": "2024-05-02"}, {"id": 5, "date": "2026-08-27"},
        {"id": 6, "date": "2025-02-19"}, {"id": 7, "date": "2026-11-22"}, {"id": 8, "date": "2024-09-10"},
        {"id": 9, "date": "2026-12-11"},
    ]
    resetCounters()
    print("sortByDate ids:", [r["id"] for r in sortByDate(recs)])
    print("passes:", getCounters()["passes"])

    print("tokenize('llamba'):", tokenize("llamba"))
    print("tokenize('shtëpi'):", tokenize("shtëpi"))

    words = ("shi çaj llamba zemër dhe gur nënë tokë xhami emër rrugë cep "
             "ëndërr drita thikë lule njeri gjak zhurmë rosa dera sot xixa dhelpër").split()
    resetCounters()
    print("sortAlbanian:", " ".join(sortAlbanian(words)))
    print("passes:", getCounters()["passes"])