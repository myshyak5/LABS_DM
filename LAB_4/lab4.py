import math
from heapq import heappush, heappop, heapify


def clean_text(text):
    text = text.lower()
    text = text.replace(' ', '')
    for i in text:
        if i in '1234567890-_,.:;!?()’“”…':
            text = text.replace(i,'')
    return text

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

def build_huffman_codes(node, code="", codes={}):
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
        print(f"Всего символов в тексте: {len(text)}")
    text = clean_text(text)
    print(f"Количество буквенных символов в тексте: {len(text)}")
    letter_list, bigram_list, total_letters, total_bigrams = analyze_text_statistics(text)
    couple_l_n = sorted(letter_list.items(), key=lambda x:x[1])
    print("\nСписок букв с их частотами (по возрастанию частоты): ")
    print(couple_l_n)
    with open('statistic_letter.txt', 'w', encoding='utf-8') as f:
        for letter in letter_list:
            f.write(f'{letter}: {letter_list[letter]}\n')
    with open('statistic_bigrams.txt', 'w', encoding='utf-8') as f:
        for letter in bigram_list:
            f.write(f'{letter}: {bigram_list[letter]}\n')
    
    # 2. Коды Хаффмана
    tree = build_huffman_tree(letter_list)
    huffman_codes = build_huffman_codes(tree)
    
    print("\nКоды Хаффмана:")
    for char, code in sorted(huffman_codes.items(), key=lambda x: len(x[1])):
        print(f"    {char}: {code}")
    encoded_huffman = ''.join(huffman_codes[char] for char in text)
    huffman_bits = len(encoded_huffman)
    
    # Равномерный 5-битовый код
    uniform_bits = len(text) * 5
    
    # Шеннон
    probs = [count/total_letters for count in letter_list.values()]
    entropy = -sum(p * math.log2(p) for p in probs)
    shannon_bits = entropy * total_letters
    
    print(f"\nСравнение:")
    print(f"    Равномерный код: {uniform_bits} бит")
    print(f"    Код Хаффмана: {huffman_bits} бит")
    print(f"    По Шеннону: {shannon_bits} бит")
    print(f"    Хаффман / Равномерный: {huffman_bits/uniform_bits}")
    
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
    print(f"    LZW / Хаффман: {lzw_bits/huffman_bits}")