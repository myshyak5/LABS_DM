def rle_compress(data):
    compressed = bytearray()
    i = 0
    n = len(data)
    while i < n:
        count = 1
        while i + count < n and count < 256 and data[i] == data[i + count]:
            count += 1
        if count > 1:
            compressed.append(count)
            compressed.append(ord(data[i]))
            i += count
        else:
            start = i
            non_repeat = 0
            while i < n and non_repeat < 256:
                if i + 2 < n and data[i] == data[i + 1]:
                    break
                non_repeat += 1
                i += 1
            compressed.append(0)
            compressed.append(non_repeat)
            for j in range(start, start + non_repeat):
                compressed.append(ord(data[j]))
    return compressed

def main():
    data = "aaaaaaaaaaaaadghtttttttttttyiklooooooop"
    print("Исходная строка:", data)
    print("Длина:", len(data), "байт")
    
    compressed = rle_compress(data)
    print("\nСжатые данные:", list(compressed))
    print("Длина:", len(compressed), "байт")
    
    print("\nФормат сжатия:")
    i = 0
    while i < len(compressed):
        count = compressed[i]
        if count == 0:
            length = compressed[i+1]
            print(f"[0, {length}] + данные: {list(compressed[i+2:i+2+length])}")
            i += 2 + length
        else:
            char = chr(compressed[i+1])
            print(f"[{count}, '{char}']")
            i += 2
    
    # Статистика
    rate = len(data) / len(compressed)
    ratio = len(compressed) / len(data)
    print(f"\nКоэффициент сжатия: {ratio}")
    print(f"Степень сжатия: {rate}")

if __name__ == "__main__":
    main()