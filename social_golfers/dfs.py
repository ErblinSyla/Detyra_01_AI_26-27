"""DFS me Backtracking për Social Golfers (me bitmask)."""
import sys, time
sys.setrecursionlimit(20000)

class _Timeout(Exception): pass

def dfs_solve(g, p, w, time_limit=60.0):
    """Ndërton javë pas jave, grup pas grupi, lojtar pas lojtari.
    Prerje (pruning): kandidati s'duhet të ketë takuar asnjë anëtar të grupit.
    Thyerja e simetrisë: anëtari i parë i grupit = lojtari më i vogël i lirë;
    anëtarët brenda grupit rriten (pa permutime të përsëritura)."""
    n, full = g * p, (1 << (g * p)) - 1
    met = [0] * n                      # met[a] = bitmask i lojtarëve që a i ka takuar
    schedule, best, stats = [], [[]], {"nodes": 0}
    deadline = time.time() + time_limit

    def next_group(groups, used):
        if len(groups) < g:
            return place(groups, [], used)
        schedule.append([m[:] for m in groups])
        if len(schedule) > len(best[0]):
            best[0] = [wk[:] for wk in schedule]
        if len(schedule) == w or place([], [], 0):
            return True
        schedule.pop()
        return False

    def place(groups, members, used):
        stats["nodes"] += 1
        if stats["nodes"] & 0x3FFF == 0 and time.time() > deadline:
            raise _Timeout
        if not members:
            x = ~used & full
            f = (x & -x).bit_length() - 1
            members = [f]; used |= 1 << f
        if len(members) == p:
            for a in members:
                for b in members:
                    if a != b: met[a] |= 1 << b
            groups.append(members[:])
            ok = next_group(groups, used)
            groups.pop()
            if not ok:
                for a in members:
                    for b in members:
                        if a != b: met[a] &= ~(1 << b)
            return ok
        forb = used
        for m in members: forb |= met[m]
        for c in range(members[-1] + 1, n):
            if forb >> c & 1: continue
            members.append(c)
            if place(groups, members, used | 1 << c): return True
            members.pop()
        return False

    t, found = time.time(), False
    try:
        found = place([], [], 0)
    except _Timeout:
        pass
    sol = schedule if found else best[0]
    return found, sol, {"nodes": stats["nodes"], "weeks": len(sol), "time": round(time.time() - t, 2)}