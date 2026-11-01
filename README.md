# Detyra 1 – Teknikat e Painformuara të Kërkimit

Lënda: Inteligjenca Artificiale · Fakulteti i Inxhinierisë Elektrike dhe Kompjuterike, Universiteti i Prishtinës

Gjuha: Python 3.8+ (pa varësi të jashtme).

## Përmbajtja e repo-s

```
.
├── README.md
├── .gitignore
├── social_golfers/   model.py  dfs.py    main.py
├── sudoku/           model.py  bfs.py    puzzles.py  main.py
├── latin_square/     model.py  iddfs.py  main.py
└── search_trees/     PDF-të e skanuara (pema me dorë)
```

Çdo problem ndahet në tri pjesë:

| Skedari | Roli |
|---|---|
| `model.py` | Modelimi i problemit: reprezentimi, objective function, landscape |
| `dfs.py` / `bfs.py` / `iddfs.py` | Algoritmi i kërkimit që kërkon detyra |
| `main.py` | Pika e hyrjes: lexon parametrat, thërret algoritmin, printon rezultatet |
| `puzzles.py` | (vetëm Sudoku) puzzle-t Easy, Medium, Hard |

## Si ekzekutohet

Nga brenda dosjes së problemit:

```bash
cd social_golfers && python main.py 8 4 10 60   # g p w sekonda_max
cd sudoku         && python main.py             # të tria nivelet; ose: python main.py Hard
cd latin_square   && python main.py 5           # n
```

---

## 1. Social Golfers (DFS me Backtracking)

**Problemi.** `n = g·p` lojtarë luajnë në `g` grupe me nga `p` lojtarë çdo javë. Dy lojtarë nuk mund të jenë në të njëjtin grup më shumë se një herë. Kërkohet numri sa më i madh i javëve (rasti i detyrës: 8 grupe × 4 lojtarë = 32).

**Reprezentimi.**
- Gjendja: `schedule[w][g][k]`, lojtari në pozicionin `k` të grupit `g` në javën `w`.
- Variabla: vendet (javë, grup, pozicion). Domain: `{0..n-1}`.
- Kufizimet: çdo javë është ndarje e të gjithë lojtarëve, dhe çdo çift takohet maksimumi një herë.

**Objective function (minimizim).**
`f = Σ_çifte max(0, takime(a,b) − 1)`. `f = 0` do të thotë orar i vlefshëm.

**Landscape.** Fqinji është swap i dy lojtarëve nga grupe të ndryshme brenda së njëjtës javë. Numri i fqinjëve është `w · (C(n,2) − g·C(p,2))`, pra 2240 për 5 javë dhe 4480 për 10. Funksioni `landscape()` llogarit `f` për secilin fqinj dhe raporton min, max, mesataren, histogramin, numrin e fqinjëve përmirësues dhe nëse gjendja është minimum lokal.

**Algoritmi.** DFS me backtracking, i ndërtuar javë → grup → lojtar, me bitmask:
- Prerje: një kandidat hidhet nëse ka takuar ndonjë anëtar të grupit që po ndërtohet.
- Thyerja e simetrisë: anëtari i parë i grupit është lojtari më i vogël i lirë, dhe anëtarët brenda grupit rriten. Kështu nuk provohen permutime të njëjta.
- Kufi kohe: kthen orarin më të gjatë të gjetur nëse skadon koha.

**Rezultate.**
- 3-3-4 gjendet menjëherë (37 nyje, `f=0`). Zgjidhja DFS del minimum i landscape-it.
- 8-4: brenda 20 s DFS arrin **5 javë të vlefshme** (`f=0`), por jo 10. Maksimumi i njohur për 8-4 është 10 javë, por arrihet me metoda konstruktive ose heuristike, jo me DFS të pastër, sepse hapësira është shumë e madhe.

---

## 2. Sudoku (BFS me Backtracking)

**Problemi.** Zgjidhja e një Sudoku 9×9 me tre nivele (Easy, Medium, Hard).

**Reprezentimi.**
- Gjendja: listë me 81 vlera (0 = bosh), indeksi `i = 9·rreshti + kolona`.
- Variabla: 81 qelizat. Domain: `{1..9}`.
- Kufizimet: 27 njësi (9 rreshta, 9 kolona, 9 kuti 3×3) pa përsëritje.

**Objective function (minimizim).**
`f = Σ_27 njësitë (9 − numri i shifrave të ndryshme)`. Për një tabelë të pjesshme llogarit edhe shifrat që mungojnë. `f = 0` do të thotë i zgjidhur.

**Landscape.** Gjendja fillestare ka çdo kuti të plotë me shifrat që i mungojnë (në rend të rastit). Fqinji është swap i dy qelizave jo-të-dhëna brenda së njëjtës kuti, kështu që kutitë mbeten të sakta. Fqinjë: 112 (Easy), 128 (Medium), 176 (Hard).

**Algoritmi.** BFS me radhë (`deque`) që mban gjendje të pjesshme:
- Zgjerohet qeliza me më pak kandidatë (MRV). Çdo hap plotëson saktësisht një qelizë, pra BFS shkon nivel pas niveli.
- Nëse një qelizë nuk ka kandidatë, gjendja hidhet. Ky është "backtracking" në BFS: dega e pavlefshme pritet, pa kthim rekursiv.
- Goal: nuk ka qeliza bosh.

**Rezultate.**

| Niveli | Zgjerime | Radha maksimale | Kohë |
|---|---|---|---|
| Easy | 49 | 1 | ~0 s |
| Medium | 51 | 1 | ~0 s |
| Hard | 24,880 | 1003 | ~0.5 s |

Në Easy dhe Medium çdo hap ka një kandidat të vetëm, ndaj BFS nuk degëzohet.

---

## 3. Latin Square (IDDFS me Backtracking)

**Problemi.** Për një `n` të dhënë, të krijohet një matricë `n×n` me numrat 1..n, ku secili shfaqet saktësisht një herë në çdo rresht dhe kolonë.

**Reprezentimi.**
- Gjendja: listë me `n²` vlera, indeksi `pos = n·r + c`, plotësim rresht pas rreshti.
- Variabla: `n²` qelizat. Domain: `{1..n}`.
- Kufizimet: pa përsëritje në rreshta dhe kolona.

**Objective function (minimizim).**
`f = Σ_rreshta,kolona (n − vlera të ndryshme)`. `f = 0` do të thotë katror latin.

**Landscape.** Fqinji është ndryshimi i një qelize në çdo vlerë tjetër, pra `n²(n−1)` fqinjë (100 për n=5, 180 për n=6).

**Algoritmi.** IDDFS = DLS (Depth-Limited Search) me kufi `l = 1, 2, …, n²`:
- Thellësia e një qelize është pozicioni i saj. Në kufi (`pos == l`) pa qenë goal kthehet cutoff. Goal është kur `n²` qelizat janë plotësuar.
- Backtracking: nëse një qelizë nuk ka vlerë të lirë për rreshtin dhe kolonën, kthehemi pas.
- Thyerja e simetrisë: katror i reduktuar (rreshti dhe kolona e parë janë 1..n). Çdo katror latin normalizohet kështu, pa humbur klasa zgjidhjesh.

**Rezultate.**
- n=5: 6,760 nyje (pa normalizim ishin 13.5M).
- n=6: 1,506,140 nyje.
- Për n ≥ 7 bëhet i ngadaltë: IDDFS riprovon nyjet për çdo kufi `l < n²`, ku asnjë goal nuk mund të gjendet, dhe hapësira rritet eksponencialisht.

---

## 4. Search Trees (me dorë)

PDF-të ndodhen te `search_trees/`. Gjendjet dhe operatorët:

| Problemi | Gjendja | Operatorët |
|---|---|---|
| 8-Puzzle | Grid 3×3 | Lëvizja e vendit bosh: Up, Down, Left, Right |
| Missionaries and Cannibals | `(M_majtas, C_majtas, varka)` | Kalimi i 1M, 2M, 1C, 2C ose 1M1C |
| Rotating Workforce Scheduling | Tabelë `x[e][d]` ∈ {D, N, O} | Vendosja e një shifti në qelizën tjetër bosh |

Degët e prera (✂) janë gjendje të pavlefshme ose të përsëritura.