"""Social Golfers: modelimi, objective function dhe landscape."""
import itertools, random
from collections import Counter

# Reprezentimi: schedule[w][g] = lista e p lojtarëve (0..n-1) në grupin g të javës w.
# Variabla: pozicioni (w, g, k); Domain: {0..n-1}, n = g*p.
# Kufizimet: çdo javë është ndarje e n lojtarëve; çifti (a,b) takohet max 1 herë.

def objective(schedule):
    """f = sum_{çifte} max(0, takime-1). f == 0  <=>  zgjidhje e vlefshme (minimizim)."""
    c = Counter()
    for week in schedule:
        for grp in week:
            for pair in itertools.combinations(sorted(grp), 2):
                c[pair] += 1
    return sum(v - 1 for v in c.values() if v > 1)

def random_schedule(g, p, w, rng=random):
    sched = []
    for _ in range(w):
        perm = list(range(g * p)); rng.shuffle(perm)
        sched.append([perm[i * p:(i + 1) * p] for i in range(g)])
    return sched

def landscape(schedule):
    """Fqinjësia: swap i dy lojtarëve nga grupe të ndryshme brenda së njëjtës javë.
    Madhësia = w * (C(n,2) - g*C(p,2)). Kthen statistikat e f mbi fqinjët."""
    base, vals = objective(schedule), []
    for week in schedule:
        for gi, gj in itertools.combinations(range(len(week)), 2):
            for a in range(len(week[gi])):
                for b in range(len(week[gj])):
                    week[gi][a], week[gj][b] = week[gj][b], week[gi][a]
                    vals.append(objective(schedule))
                    week[gi][a], week[gj][b] = week[gj][b], week[gi][a]
    return {"f": base, "fqinje": len(vals), "min": min(vals), "max": max(vals),
            "mesatarja": round(sum(vals) / len(vals), 2),
            "permiresues": sum(v < base for v in vals),
            "te_barabarte": sum(v == base for v in vals),
            "me_te_keq": sum(v > base for v in vals),
            "minimum_lokal": all(v >= base for v in vals),
            "histogram": dict(sorted(Counter(vals).items()))}