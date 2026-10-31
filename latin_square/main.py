import sys, random
from model import objective, landscape, random_square
from iddfs import iddfs_solve

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    g, st = iddfs_solve(n)
    print(f"n={n} | {st} | f(zgjidhja)={objective(g, n)}")
    for r in range(n): print(*g[n * r:n * r + n])
    random.seed(3)
    print("Landscape (katror i rastesishem):", landscape(random_square(n), n))