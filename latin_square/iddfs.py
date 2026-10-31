"""Iterative Deepening DFS me Backtracking për Latin Square."""

def iddfs_solve(n):
    """DLS (Depth-Limited Search) me kufi l = 1, 2, ..., n^2. Thellësia e qelizës = pozicioni i saj.
    Në kufi pos == l (pa qenë goal) kthehet cutoff; goal = n^2 qeliza të plotësuara.
    Thyerja e simetrisë: katror i reduktuar (rreshti dhe kolona e parë = 1..n); çdo katror latin
    normalizohet kështu me permutim rreshtash/kolonash/simbolesh, pra s'humbet asnjë klasë zgjidhjesh.
    Backtracking: nëse një qelizë s'ka vlerë të lirë (rresht/kolonë), kthehemi pas."""
    N, full = n * n, (1 << n) - 1
    grid, rows, cols, nodes = [0] * N, [0] * n, [0] * n, [0]

    def dls(pos, limit):
        nodes[0] += 1
        if pos == N: return True
        if pos == limit: return False          # cutoff
        r, c = divmod(pos, n)
        avail = full & ~rows[r] & ~cols[c]
        if r == 0: avail &= 1 << c            # normalizim: rreshti i parë = 1..n
        elif c == 0: avail &= 1 << r          # normalizim: kolona e parë = 1..n
        while avail:
            bit = avail & -avail; avail ^= bit
            grid[pos] = bit.bit_length()
            rows[r] |= bit; cols[c] |= bit
            if dls(pos + 1, limit): return True
            rows[r] ^= bit; cols[c] ^= bit; grid[pos] = 0
        return False

    for limit in range(1, N + 1):
        if dls(0, limit):
            return grid, {"depth_limit": limit, "nodes": nodes[0]}
    return None, {"nodes": nodes[0]}