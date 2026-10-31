"""Latin Square: modelimi, objective function dhe landscape."""
import random

# Reprezentimi: lista me n*n numra, indeksi pos = n*r + c (plotësim rresht-pas-rreshti).
# Variabla: n^2 qelizat; Domain: {1..n}.
# Kufizimet: çdo vlerë 1..n shfaqet saktësisht një herë në çdo rresht dhe kolonë.

def objective(g, n):
    """f = sum_{rreshta, kolona} (n - #vlera të ndryshme). f == 0 <=> katror latin (minimizim)."""
    rows = sum(n - len(set(g[n * r:n * r + n])) for r in range(n))
    cols = sum(n - len(set(g[c::n])) for c in range(n))
    return rows + cols

def landscape(g, n):
    """Fqinjësia: ndrysho vlerën e një qelize në çfarëdo vlere tjetër. Madhësia = n^2 (n-1)."""
    base, vals = objective(g, n), []
    for i in range(n * n):
        old = g[i]
        for v in range(1, n + 1):
            if v != old:
                g[i] = v; vals.append(objective(g, n))
        g[i] = old
    return {"f": base, "fqinje": len(vals), "min": min(vals), "max": max(vals),
            "mesatarja": round(sum(vals) / len(vals), 2),
            "permiresues": sum(v < base for v in vals),
            "minimum_lokal": all(v >= base for v in vals)}

def random_square(n, rng=random):
    return [rng.randint(1, n) for _ in range(n * n)]