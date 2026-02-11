import math
from functools import lru_cache

#1
print(f"Все кратчайшие пути: {math.comb(33, 18)}")

#2
@lru_cache(maxsize=None)
def dp(remR, remU, last):
    if remR == 0 and remU == 0:
        return 1
    total = 0
    if remR > 0:
        total += dp(remR - 1, remU, 0)
    if remU > 0 and last != 1:
        total += dp(remR, remU - 1, 1)
    return total
print("Без двух вертикальных подряд:", dp(18, 15, 0))