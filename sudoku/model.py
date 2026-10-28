"""Sudoku: modelimi, objective function dhe landscape."""
import random

# Reprezentimi: lista me 81 numra (0 = qelizë e zbrazët), indeksi i = 9*rreshti + kolona.
# Variabla: 81 qelizat; Domain: {1..9} (qelizat e dhëna: domain me 1 vlerë).
# Kufizimet: 27 njësi (9 rreshta, 9 kolona, 9 kuti 3x3) pa përsëritje.

ROWS = [[9 * r + c for c in range(9)] for r in range(9)]
COLS = [[9 * r + c for r in range(9)] for c in range(9)]
BOXES = [[9 * (3 * br + r) + 3 * bc + c for r in range(3) for c in range(3)]
         for br in range(3) for bc in range(3)]
UNITS = ROWS + COLS + BOXES
PEERS = [sorted({j for u in UNITS if i in u for j in u} - {i}) for i in range(81)]

def parse(s):
    return [0 if ch in ".0" else int(ch) for ch in s]

def objective(b):
    """f = sum_{njësi} (9 - #shifra të ndryshme). f == 0 <=> Sudoku i zgjidhur (minimizim)."""
    return sum(9 - len({b[i] for i in u if b[i]}) for u in UNITS)

def candidates(b, i):
    used = {b[j] for j in PEERS[i]}
    return [v for v in range(1, 10) if v not in used]

def random_box_fill(b, rng=random):
    """Gjendje fillestare për landscape: çdo kuti plotësohet me shifrat që i mungojnë."""
    b = b[:]
    for box in BOXES:
        miss = [v for v in range(1, 10) if v not in {b[i] for i in box}]
        rng.shuffle(miss)
        for i in box:
            if b[i] == 0: b[i] = miss.pop()
    return b

def landscape(b, given):
    """Fqinjësia: swap i dy qelizave jo-të-dhëna brenda së njëjtës kuti (kutitë mbeten të sakta).
    Kthen statistikat e f mbi fqinjët."""
    base, vals = objective(b), []
    for box in BOXES:
        free = [i for i in box if given[i] == 0]
        for x in range(len(free)):
            for y in range(x + 1, len(free)):
                i, j = free[x], free[y]
                b[i], b[j] = b[j], b[i]
                vals.append(objective(b))
                b[i], b[j] = b[j], b[i]
    return {"f": base, "fqinje": len(vals), "min": min(vals), "max": max(vals),
            "mesatarja": round(sum(vals) / len(vals), 2),
            "permiresues": sum(v < base for v in vals),
            "minimum_lokal": all(v >= base for v in vals)}