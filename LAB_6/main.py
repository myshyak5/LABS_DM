import itertools

G1 = [
    (0, 1), (0, 4), (0, 7), (0, 8), (0, 9),
    (1, 2), (1, 5), (1, 6), (1, 7), (1, 9),
    (2, 3), (2, 5), (2, 8),
    (3, 4), (3, 6),
    (4, 5), (4, 9),
    (5, 6), (5, 7),
    (6, 7), (6, 9),
    (7, 8), (7, 9),
    (8, 9)
]

G2 = [
    (0, 2), (0, 5), (0, 9),
    (1, 3), (1, 7), (1, 8), (1, 9),
    (2, 4), (2, 6), (2, 7), (2, 8),
    (3, 5), (3, 6), (3, 7), (3, 8),
    (4, 5), (4, 6), (4, 8), (4, 9),
    (5, 7),
    (6, 7), (6, 8), (6, 9),
    (7, 8)
]

n = 10
m = len(G1)

A1 = [[0] * n for _ in range(n)]
for u, v in G1:
    A1[u][v] = 1
    A1[v][u] = 1

A2 = [[0] * n for _ in range(n)]
for u, v in G2:
    A2[u][v] = 1
    A2[v][u] = 1

I1 = [[0] * m for _ in range(n)]
for edge_index, (u, v) in enumerate(G1):
    I1[u][edge_index] = 1
    I1[v][edge_index] = 1

found = False
count = 0
for perm in itertools.permutations(range(n)):
    count += 1
    ok = True
    for i in range(n):
        for j in range(n):
            if A1[i][j] != A2[perm[i]][perm[j]]:
                ok = False
                break
        if not ok:
            break
    if ok:
        print("Графы изоморфны!")
        print("Изоморфизм:")
        print("\nG1 | G2")
        print("-" * 7)
        for i in range(n):
            print(f"{i}  | {perm[i]}")
        found = True
        break

if not found:
    print("Графы НЕ изоморфны.")
    print(f"Проверено {count} биекций.")

print("\nМатрица смежности для G1:\n")
print(*A1, sep = "\n")
print("\nМатрица инцидентности для G1:\n")
print(*I1, sep = "\n")