import sys, random
from model import objective, random_schedule, landscape
from dfs import dfs_solve

def show(s):
    for i, wk in enumerate(s, 1):
        print(f"Week {i:2d} | " + " | ".join(",".join(map(str, g)) for g in wk))

if __name__ == "__main__":
    g, p, w = (int(x) for x in sys.argv[1:4]) if len(sys.argv) >= 4 else (8, 4, 10)
    tl = float(sys.argv[4]) if len(sys.argv) > 4 else 60
    found, sol, st = dfs_solve(g, p, w, tl)
    print(f"g={g} p={p} w={w} | gjetur={found} | {st}")
    show(sol)
    print("f(zgjidhja) =", objective(sol))
    random.seed(1)
    r = random_schedule(g, p, max(len(sol), 1))
    print("Landscape (orari i rastesishem):", landscape(r))
    if sol:
        print("Landscape (zgjidhja DFS):", landscape([[x[:] for x in wk] for wk in sol]))