import math
from heapq import heappush, heappop, heapify


def analyze_text_statistics(text):
    letter_stats = {}
    for letter in text:
        if letter in letter_stats:
            letter_stats[letter] += 1
        else:
            letter_stats[letter] = 1
    
    total_letters = len(text)
    sorted_letters = dict(sorted(letter_stats.items()))

    bigram_stats = {}
    for i in range(len(text) - 1):
        bigram = text[i] + text[i+1]
        if bigram in bigram_stats:
            bigram_stats[bigram] += 1
        else:
            bigram_stats[bigram] = 1
    
    total_bigrams = len(text) - 1
    sorted_bigrams = dict(sorted(bigram_stats.items()))
    return sorted_letters, sorted_bigrams, total_letters, total_bigrams

# Класс для дерева Хаффмана
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    heap = [Node(char, freq) for char, freq in frequencies.items()]
    heapify(heap)
    
    while len(heap) > 1:
        left = heappop(heap)
        right = heappop(heap)
        parent = Node(None, left.freq + right.freq)
        parent.left = left
        parent.right = right
        heappush(heap, parent)
    
    return heap[0]

def build_huffman_codes(node, code="", codes=None):
    if codes is None:
        codes = {}
    if node is None:
        return codes
    if node.char is not None:
        codes[node.char] = code
        return codes
    build_huffman_codes(node.left, code + "0", codes)
    build_huffman_codes(node.right, code + "1", codes)
    return codes

# LZW алгоритм
class LZW:
    def __init__(self):
        self.dictionary = {}
        self.next_code = 0
    
    def compress(self, text):
        unique_chars = sorted(set(text))
        for char in unique_chars:
            self.dictionary[char] = self.next_code
            self.next_code += 1
        
        compressed = []
        current_string = ""
        
        for char in text:
            new_string = current_string + char
            if new_string in self.dictionary:
                current_string = new_string
            else:
                if current_string:
                    compressed.append(self.dictionary[current_string])
                self.dictionary[new_string] = self.next_code
                self.next_code += 1
                current_string = char
        
        if current_string:
            compressed.append(self.dictionary[current_string])
        
        return compressed


if __name__ == "__main__":
    with open('text.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    text = text.lower()
    # Оставляем только нужные символы
    
    print(f"Всего символов в тексте: {len(text)}")
    
    # 1. Статистический анализ
    letter_list, bigram_list, total_letters, total_bigrams = analyze_text_statistics(text)
    
    # Сохраняем статистику
    with open('statistic_letter.txt', 'w', encoding='utf-8') as f:
        for letter in letter_list:
            f.write(f'{letter}: {letter_list[letter]}\n')
    
    with open('statistic_bigrams.txt', 'w', encoding='utf-8') as f:
        for bigram in bigram_list:
            f.write(f'{bigram}: {bigram_list[bigram]}\n')
    
    # 2. Коды Хаффмана для букв
    tree_letters = build_huffman_tree(letter_list)
    huffman_codes_letters = build_huffman_codes(tree_letters)
    
    # Кодирование текста кодами для букв
    encoded_huffman_letters = ''.join(huffman_codes_letters[char] for char in text)
    huffman_letters_bits = len(encoded_huffman_letters)
    
    # Коды Хаффмана для пар букв
    tree_bigrams = build_huffman_tree(bigram_list)
    huffman_codes_bigrams = build_huffman_codes(tree_bigrams)
    
    with open('huffman_codes_letters.txt', 'w', encoding='utf-8') as f:
        for char, code in sorted(huffman_codes_letters.items(), key=lambda x: len(x[1])):
            f.write(f'{repr(char)}: {code}\n')
    with open('huffman_codes_bigrams.txt', 'w', encoding='utf-8') as f:
        for bigram, code in sorted(huffman_codes_bigrams.items(), key=lambda x: len(x[1])):
            f.write(f'{repr(bigram)}: {code}\n')

    encoded_huffman_bigrams = ''
    for i in range(len(text) - 1):
        if i+1 < len(text):
            bigram = text[i] + text[i+1]
            encoded_huffman_bigrams += huffman_codes_bigrams[bigram]
    huffman_bigrams_bits = len(encoded_huffman_bigrams)
    
    # Равномерный 5-битовый код
    uniform_bits = len(text) * 5
    
    # Шеннон для букв
    probs_letters = [count/total_letters for count in letter_list.values()]
    entropy_letters = -sum(p * math.log2(p) for p in probs_letters)
    shannon_letters_bits = entropy_letters * total_letters
    
    # Шеннон для пар
    probs_bigrams = [count/total_bigrams for count in bigram_list.values()]
    entropy_bigrams = -sum(p * math.log2(p) for p in probs_bigrams)
    shannon_bigrams_bits = entropy_bigrams * total_bigrams
    
    print(f"Равномерный код: {uniform_bits} бит")
    print(f"Код Хаффмана (буквы): {huffman_letters_bits} бит")
    print(f"Код Хаффмана (пары букв): {huffman_bigrams_bits} бит")
    print(f"По Шеннону (буквы): {shannon_letters_bits} бит")
    print(f"По Шеннону (пары): {shannon_bigrams_bits} бит")
    
    print(f"\nСравнение с равномерным кодом:")
    print(f"    Хаффман (буквы) / Равномерный: {huffman_letters_bits/uniform_bits}")
    print(f"    Хаффман (пары) / Равномерный: {huffman_bigrams_bits/uniform_bits}")
    
    print(f"\nСравнение с Шенноном:")
    print(f"    Хаффман (буквы) / Шеннон (буквы): {huffman_letters_bits/shannon_letters_bits}")
    print(f"    Хаффман (пары) / Шеннон (пары): {huffman_bigrams_bits/shannon_bigrams_bits}")
    
    # 3. LZW кодирование
    lzw = LZW()
    compressed = lzw.compress(text)
    bits_per_code = math.ceil(math.log2(lzw.next_code))
    lzw_bits = len(compressed) * bits_per_code
    
    print(f"\nLZW:")
    print(f"    Размер словаря: {lzw.next_code}")
    print(f"    Бит на код: {bits_per_code}")
    print(f"    LZW: {lzw_bits} бит")
    print(f"    LZW / Равномерный: {lzw_bits/uniform_bits}")
    print(f"    LZW / Хаффман (буквы): {lzw_bits/huffman_letters_bits}")
    print(f"    LZW / Хаффман (пары): {lzw_bits/huffman_bigrams_bits}")
