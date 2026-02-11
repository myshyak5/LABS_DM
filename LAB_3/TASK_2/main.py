def ham_distance(a, b) -> int:
    return bin(int(a, 2)^int(b, 2)).count("1")

def min_ham_distance(data: list) -> int:
    min_dist = float('inf')
    for i in range(len(data) - 1):
        for j in range(i + 1, len(data)):
            min_dist = min(min_dist, ham_distance(data[i], data[j]))
    return min_dist

def print_distance_table(codes_dict, title):
    print(f"\n{title}\n")

    chars = list(codes_dict.keys())
    codes = list(codes_dict.values())

    print(" " * 10 + "—" * 33)
    print(" " * 10, end="|")
    for char in chars:
        print(f"{char:^3}", end="|")
    print("\n" + " " * 10 + "—" * 33)
    for i in range(len(chars)):
        print(f"{chars[i]}: {codes[i]:^7}", end="|")
        for j in range(len(chars)):
            distance = ham_distance(codes[i], codes[j])
            print(f"{distance:^3}", end="|")
        print()

def main():
    # Часть 1: Коды с расстоянием >= 2 (4 бита)
    print("1. Коды с расстоянием >= 2 (4 бита, обнаружение ошибок):")
    codes_d2 = {
        'ч': '0000',
        'ш': '0011',
        'щ': '0101',
        'ь': '0110',
        'ъ': '1001',
        'э': '1010',
        'ю': '1100',
        'я': '1111'
    }
    
    print_distance_table(codes_d2, "ТАБЛИЦА РАССТОЯНИЙ ХЕММИНГА (4-битные коды):")
    print(f"\nМинимальное расстояние: {min_ham_distance(list(codes_d2.values()))}")

    error_code_d2 = '0001'
    if error_code_d2 not in codes_d2.values():
        print(f"\nКод {error_code_d2} не найден!")
    
    # Часть 2: Коды с расстоянием >= 3 (6 бит)
    print("\n2. Коды с расстоянием >= 3 (6 бит, исправление ошибок):")
    codes_d3 =  {
    'ч': '000000',
    'ш': '001110', 
    'щ': '010101',  
    'ь': '011011',  
    'ъ': '100011',  
    'э': '101101',  
    'ю': '110110',  
    'я': '111000' 
}
    print_distance_table(codes_d3, "ТАБЛИЦА РАССТОЯНИЙ ХЕММИНГА (6-битные коды):")
    print(f"\nМинимальное расстояние: {min_ham_distance(list(codes_d3.values()))}")

    error_code_d3 = "000001"
    
    if error_code_d3 not in codes_d3.values():
        print(f"\nКод {error_code_d3} не найден!")
    
    # Ищем ближайший код
    print(f"\nПоиск ближайшего корректного кода для {error_code_d3}:")
    print("-" * 60)
    
    nearest_char = None
    min_dist_err = float('inf')
    distances = {}
    
    for char, code in codes_d3.items():
        dist = ham_distance(error_code_d3, code)
        distances[char] = dist
        print(f"Расстояние до '{char}' ({code}): {dist}")
        if dist < min_dist_err:
            min_dist_err = dist
            nearest_char = char
    
    print("-" * 60)
    print(f"\nБлижайший код: {codes_d3[nearest_char]} (символ '{nearest_char}')")

if __name__ == "__main__":
    main()