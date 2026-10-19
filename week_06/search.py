T = 'JIM SAW ME IN A BARBERSHOP'
P = 'BARBER'


def brute_force(T, P):
    n, m = len(T), len(P)
    for i in range(n - m + 1):
        j = 0
        while j < m and P[j] == T[i + j]:
            j += 1
        if j == m:
            return i
    return -1


def shift_table(P):
    m = len(P)
    table = {}
    for j in range(m - 1):
        table[P[j]] = m - 1 - j
    return table


def shift(table, c, m):
    return table[c] if c in table else m


def horspool(T, P):
    n, m = len(T), len(P)
    table = shift_table(P)
    i = m - 1
    while i <= n - 1:
        k = 0
        while k <= m - 1 and P[m - 1 - k] == T[i - k]:
            k += 1
        if k == m:
            return i - m + 1
        i += shift(table, T[i], m)
    return -1


def horspool2(T, P):
    n, m = len(T), len(P)
    table = shift_table(P)
    i = m - 1
    while i <= n - 1:
        k = 0
        while k <= m - 1 and P[m - 1 - k] == T[i - k]:
            k += 1
        if k == m:
            return i - m + 1
        i += shift(table, T[i - k], m)
    return -1


if __name__ == '__main__':
    print('shift_table(P) =', shift_table(P))
    # Result: {'B': 2, 'A': 4, 'R': 3, 'E': 1}
    # B=2 (last B before the end, index 3), A=4, R=3, E=1; any other char -> m = 6

    print('brute_force(T, P) =', brute_force(T, P))
    # Result: 16

    print('horspool(T, P) =', horspool(T, P))
    # Result: 16

    print('horspool2(T, P) =', horspool2(T, P))
    # Result: -1
