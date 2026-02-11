import math

symbols = ['a', 'b', 'c', 'd', 'e', 'f']
probs = [0.10, 0.10, 0.05, 0.55, 0.10, 0.10]
string = "aecdfb"

range_table = {}
low = 0.0
for i, sym in enumerate(symbols):
    high = low + probs[i]
    range_table[sym] = (low, high)
    low = high

print("Таблица диапазонов:")
for sym in symbols:
    print(f"{sym}: [{range_table[sym][0]:.2f}, {range_table[sym][1]:.2f})")
print()

low, high = 0.0, 1.0
for i, sym in enumerate(string):
    sym_low, sym_high = range_table[sym]
    range_width = high - low
    new_low = low + range_width * sym_low
    new_high = low + range_width * sym_high
    low, high = new_low, new_high
    print(f"Символ '{sym}': интервал [{low:.8f}, {high:.8f})")

print(f"\nИтоговый интервал: [{low:.8f}, {high:.8f})")

code = low
print(f"Выбранный код: {code:.8f}")

interval_length = high - low
min_bits = math.ceil(-math.log2(interval_length))

binary_code = ""
temp_code = code
for _ in range(min_bits):
    temp_code *= 2
    bit = int(temp_code)
    binary_code += str(bit)
    temp_code -= bit

print(f"Двоичный код: {binary_code}")

# 5. Степень сжатия
original_bits = len(string) * math.ceil(math.log2(len(symbols)))
encoded_bits = min_bits
print(f"\nИсходный размер: {original_bits}")
print(f"Сжатый размер: {encoded_bits}")
print(f"\nСтепень сжатия: {original_bits/encoded_bits}")
print(f"Коэффициент сжатия: {encoded_bits/original_bits}")