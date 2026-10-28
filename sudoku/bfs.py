"""BFS me Backtracking (prerje e degëve të pavlefshme) për Sudoku."""
from collections import deque
from model import candidates

def bfs_solve(board):
    """Radha (queue) mban gjendje të pjesshme. Zgjerojmë qelizën me më pak kandidatë (MRV).
    Nëse një qelizë s'ka kandidatë -> gjendja hidhet (dead-end, 'backtracking' në BFS).
    Çdo hap e mbush saktësisht 1 qelizë, pra BFS e eksploron nivel pas niveli."""
    q, expanded, max_q = deque([tuple(board)]), 0, 1
    while q:
        b = q.popleft()
        best = None
        for i in range(81):
            if b[i] == 0:
                c = candidates(b, i)
                if best is None or len(c) < len(best[1]):
                    best = (i, c)
                    if len(c) <= 1: break
        if best is None:
            return list(b), {"expanded": expanded, "max_queue": max_q}
        expanded += 1
        i, c = best
        for v in c:
            nb = list(b); nb[i] = v
            q.append(tuple(nb))
        max_q = max(max_q, len(q))
    return None, {"expanded": expanded, "max_queue": max_q}