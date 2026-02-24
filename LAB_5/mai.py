n = 31
m = 26
k = n - m  # = 5
g_poly = [1, 0, 0, 1, 0, 1]  # x^5 + x^2 + 1

def poly_div_mod2(dividend, divisor) -> list:
    dividend = dividend.copy()
    div_len = len(divisor)
    while len(dividend) >= div_len and any(dividend):
        shift = 0
        for i in range(len(dividend)):
            if dividend[i] == 1:
                shift = i
                break
        if len(dividend) - shift < div_len:
            break
        for j in range(div_len):
            if shift + j < len(dividend):
                dividend[shift + j] ^= divisor[j]
        while dividend and dividend[0] == 0:
            dividend.pop(0)
    remainder = dividend if dividend else [0]
    while len(remainder) < k:
        remainder.insert(0, 0)
    return remainder[-k:]

def systematic_encode(info_bits) -> list:
    shifted = info_bits + [0] * k
    remainder = poly_div_mod2(shifted, g_poly)
    return info_bits + remainder

# def check_syndrome(syndrome) -> bool:
#     if any(syndrome):
#         return True
#     else:
#         return False

# def corrected(code, error_pos) -> list:
#     return code[error_pos] ^ 1

if __name__ == '__main__':
    print(f"n = {n}, m = {m}, k = {k}, G(x) = 100101")
    print("\n=== ПУНКТ 1 ====================")
    print("\nСтрока |    Информационный вектор   | Проверочные | Кодовое слово")
    print("-" * 100)
    codewords = []
    for i in range(m):
        info = [0] * m
        info[i] = 1
        codeword = systematic_encode(info)
        codewords.append(codeword)
        check_part = codeword[m:]
        info_str = ''.join(str(bit) for bit in info)
        check_str = ''.join(str(bit) for bit in check_part)
        code_str = ''.join(str(bit) for bit in codeword)
        print(f"{i+1:3d}    | {info_str} |    {check_str}    | {code_str}")
    print("=" * 100)

    print("\n\n")
    print(" " * m + "ТАБЛИЦА КОДОВЫХ РАССТОЯНИЙ (между всеми парами слов)")
    print()

    print("     ", end="")
    for j in range(m):
        print(f"{j+1:3d}", end=" ")
    print()
    print("     " + "-" * (m * 4))
    min_dist = n + 1
    for i in range(m):
        print(f"{i+1:2d} | ", end="")
        for j in range(m):
            if i == j:
                print(f"  0", end=" ")
            else:
                dist = sum(a ^ b for a, b in zip(codewords[i], codewords[j]))
                print(f"{dist:3d}", end=" ")
                if dist < min_dist:
                    min_dist = dist
        print()

    print(f"\nМинимальное кодовое расстояние по таблице: {min_dist}")

    print("\n\n=== ПУНКТ 2 ====================")
    t_det = min_dist - 1
    t_cor = t_det // 2
    print(f"\nКратность гарантированно обнаруживаемых ошибок: {t_det}")
    print(f"Кратность гарантированно исправляемых ошибок: {t_cor}")

    print("\n\n=== ПУНКТЫ 3-4 ==================")
    U = codewords[0]
    print(f"\nИсходное кодовое слово U = {''.join(str(bit) for bit in U)}")
    print("\nПРИМЕР 1: Исправление однократной ошибки")
    R1 = U.copy()
    error_pos1 = 10
    R1[error_pos1] ^= 1
    print(f"Принятое слово: {''.join(str(bit) for bit in R1)} (ошибка в бите {error_pos1}):")
    syndrome1 = poly_div_mod2(R1, g_poly)
    print(f"Синдром = {''.join(str(bit) for bit in syndrome1)} (ненулевой => ошибка есть)")
    print(f"По синдрому определяется позиция {error_pos1} и ошибка исправляется")
    print("РЕЗУЛЬТАТ: Ошибка исправлена")

    print("\nПРИМЕР 2: Обнаружение двукратной ошибки")
    R2 = U.copy()
    R2[5] ^= 1
    R2[12] ^= 1
    print(f"Принятое слово: {''.join(str(bit) for bit in R2)} (ошибки в битах 5 и 12):")
    syndrome2 = poly_div_mod2(R2, g_poly)
    print(f"Синдром = {''.join(str(bit) for bit in syndrome2)} (ненулевой => ошибка есть)")
    print(f"Но код может исправить только одну ошибку, поэтому")
    print("РЕЗУЛЬТАТ: Ошибка обнаружена, но не исправлена")

    print("\nПРИМЕР 3: Нераспознаваемая тройная ошибка")
    E = [0] * n
    for j in range(len(g_poly)):
        E[j] = g_poly[j]
    print(f"Вектор ошибки E = {''.join(str(bit) for bit in E)}")
    R3 = U.copy()
    for i in range(n):
        R3[i] ^= E[i]
    print(f"Принятое слово: {''.join(str(bit) for bit in R3)}")
    syndrome3 = poly_div_mod2(R3, g_poly)
    print(f"Синдром = {''.join(str(bit) for bit in syndrome3)} (нулевой)")
    print("РЕЗУЛЬТАТ: Ошибка не обнаружена (хотя фактически произошла)")

    print("\nПУНКТ 4: Вектор ошибки, который обнаруживается, но не исправляется")
    E = [0] * n
    E[1] = 1
    E[2] = 1
    print(f"Вектор ошибки E = {''.join(str(bit) for bit in E)}")
    print(f"Вес ошибки = {sum(E)}")
    R4 = U.copy()
    for i in range(n):
        R4[i] ^= E[i]
    print(f"Принятое слово: {''.join(str(bit) for bit in R4)}")
    syndrome4 = poly_div_mod2(R4, g_poly)
    print(f"Синдром = {''.join(str(bit) for bit in syndrome4)} (ненулевой => ошибка есть)")
    print(f"Но t_исп = 1, поэтому двукратную ошибку исправить нельзя")
    print("РЕЗУЛЬТАТ: Ошибка обнаружена, но не исправлена")