import sys, time, random
from model import parse, objective, random_box_fill, landscape
from bfs import bfs_solve
from puzzles import PUZZLES

def show(b):
    for r in range(9):
        if r % 3 == 0 and r: print("------+-------+------")
        row = b[9 * r:9 * r + 9]
        print(" | ".join(" ".join(map(str, row[k:k + 3])) for k in (0, 3, 6)))

if __name__ == "__main__":
    levels = sys.argv[1:] or list(PUZZLES)
    for lvl in levels:
        b = parse(PUZZLES[lvl]); t = time.time()
        sol, st = bfs_solve(b)
        print(f"\n== {lvl} | f(fillim)={objective(b)} | f(zgjidhje)={objective(sol)} | "
              f"{st} | {time.time() - t:.2f}s")
        show(sol)
        random.seed(7)
        print("Landscape:", landscape(random_box_fill(b), b))