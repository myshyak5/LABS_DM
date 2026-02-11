from itertools import permutations

word = "АБРАКАДАБРА"
n = 5

result = set(''.join(p) for p in permutations(word, n))

print(f"Различных слов: {len(result)}", end = "\n\n")
print(result)