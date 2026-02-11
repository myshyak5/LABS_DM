def control_bits(n) -> list:
    result = []
    bit = 1
    while bit <= n:
        result.append(bit)
        bit *= 2
    return result

def str_to_bin(data) -> str:
    return ''.join(format(ord(i), '08b') for i in data)

def bin_to_str(binary) -> str:
    result = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        result += chr(int(byte, 2))
    return result

def ham_encode_38bit(data, cb, k) -> list:
    encoded = [0] * k
    data_ind = 0
    for i in range(1, k + 1):
        if i in cb:
            encoded[i - 1] = 0
        else:
            encoded[i - 1] = int(data[data_ind])
            data_ind += 1
    for pos in cb:
        idx = pos - 1
        count_ones = 0
        for bit_num in range(1, k + 1):
            if bit_num != pos and (bit_num & pos):
                if encoded[bit_num - 1] == 1:
                    count_ones += 1
        encoded[idx] = 0 if count_ones % 2 == 0 else 1
    return encoded

def ham_decode_38bit(encoded, cb, k) -> str:
    syndrome = 0
    wrong_pos = []
    for pos in cb:
        idx = pos - 1
        count_ones = 0
        for bit_num in range(1, k + 1):
            if bit_num != pos and (bit_num & pos):
                if encoded[bit_num - 1] == 1:
                    count_ones += 1
        computed = 0 if count_ones % 2 == 0 else 1
        if computed != encoded[idx]:
            syndrome += pos
            wrong_pos.append(pos)
    if syndrome:
        print(f"Wrong positions: {wrong_pos}")
        encoded[syndrome - 1] ^= 1
    decoded = []
    for i in range(1, k + 1):
        if i not in cb:
            decoded.append(str(encoded[i - 1]))
    return ''.join(decoded)

def introduce_error(encoded, error_pos) -> list:
    encoded[error_pos - 1] ^= 1
    return encoded

def main():
    len_block = 32
    word = "location"
    bin_word = str_to_bin(word)
    first_block = bin_word[:len_block]
    second_block = bin_word[len_block:]
    cb = control_bits(len_block)
    k = len_block + len(cb)
    print("Исходные данные:")
    print(f"{word}: {bin_word}")
    print(f"Блок 1: {first_block}")
    print(f"Блок 2: {second_block}")

    first_encoded = ham_encode_38bit(first_block, cb, k)
    second_encoded = ham_encode_38bit(second_block, cb, k)
    print(f"\nЗакодированный блок 1: {''.join(map(str, first_encoded))}")
    print(f"Закодированный блок 2: {''.join(map(str, second_encoded))}")
    
    first_with_error = introduce_error(first_encoded, 7)
    second_with_error = introduce_error(second_encoded, 17)
    print(f"\nОшибочный блок 1: {''.join(map(str, first_with_error))}")
    print(f"Ошибочный блок 2: {''.join(map(str, second_with_error))}")

    first_decoded = ham_decode_38bit(first_with_error, cb, k)
    second_decoded = ham_decode_38bit(second_with_error, cb, k)
    
    print(f"\nИсправленные данные:")
    print(f"Блок 1: {first_decoded}")
    print(f"Блок 2: {second_decoded}")
    
    recovered_bin = first_decoded + second_decoded
    recovered_str = bin_to_str(recovered_bin)
    print(f"Восстановленная строка: {recovered_str}")

if __name__ == '__main__':
    main()