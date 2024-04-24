import bitarray as ba
from collections import Counter
import json
import heapq
import math


class Node:
    def __init__(self, f, char=None):
        self.freq = f
        self.char = char
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def calculate_entropy(text: str, order: int) -> float:
    substrings = [text[i:i + order] for i in range(len(text) - order + 1)]
    f = Counter(substrings)
    return -sum((count / len(substrings)) * math.log2(count / len(substrings)) for _, count in f.items())


def build_huffman_tree(freq_dict):
    pq = [Node(f, char) for char, f in freq_dict.items()]
    heapq.heapify(pq)
    while len(pq) > 1:
        left = heapq.heappop(pq)
        right = heapq.heappop(pq)
        merged = Node(left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(pq, merged)
    return pq[0]


def generate_huffman_codes(root, code="", codes=None):
    if codes is None:
        codes = {}
    if root is not None:
        if root.char is not None:
            codes[root.char] = code
        generate_huffman_codes(root.left, code + "0", codes)
        generate_huffman_codes(root.right, code + "1", codes)
    return codes


def create(freq_dict):
    huffman_tree = build_huffman_tree(freq_dict)
    huffman_codes = generate_huffman_codes(huffman_tree)
    return huffman_codes


def encode(text, code) -> ba.bitarray:
    encoded_text = ba.bitarray()
    for letter in text:
        encoded_text.extend(ba.bitarray(code[letter]))
    return encoded_text


def decode(encoded_text, code) -> str:
    code_inv = {v: k for k, v in code.items()}
    decoded_text = ""
    current_code = ""
    try:
        for i in range(code["len"]):
            current_code += '1' if encoded_text[i] else '0'
            if current_code in code_inv:
                decoded_text += code_inv[current_code]
                current_code = ""
    except KeyError:
        for bit in encoded_text:
            current_code += '1' if bit else '0'
            if current_code in code_inv:
                decoded_text += code_inv[current_code]
                current_code = ""
    return decoded_text


def save(filename, code, encoded_text):
    with open(filename + ".bin", 'wb') as file:
        encoded_text.tofile(file)

    code["len"] = len(encoded_text)
    with open(filename + "_code.json", 'w') as file:
        json.dump(code, file)


def load(filename):
    with open(filename + ".bin", 'rb') as file:
        encoded_text = ba.bitarray()
        encoded_text.fromfile(file)

    with open(filename + "_code.json", 'r') as file:
        code = json.load(file)

    return code, encoded_text


if __name__ == '__main__':
    my_filename = "../data/norm_wiki_sample.txt"
    with open(my_filename, 'r') as my_file:
        data = my_file.read()
        data_len = len(data)
        freq = {item: count / len(data)
                for item, count in sorted(Counter(data).items(), key=lambda x: x[1], reverse=True)}

        my_code = create(freq)
        average_len = sum(len(my_code[char]) * freq[char] for char in my_code)

        my_encoded_text = encode(data, my_code)
        my_decoded_text = decode(my_encoded_text, my_code)
        print("Code: ", my_code)
        print("Original text length:", data_len)
        print("Encoded text length:", len(my_encoded_text))

        save(my_filename, my_code, my_encoded_text)
        my_code_loaded, my_encoded_text_loaded = load(my_filename)
        my_decoded_text_loaded = decode(my_encoded_text_loaded, my_code_loaded)
        print("\nLoaded Code:", my_code_loaded)
        print("Loaded encoded text length:", len(my_encoded_text_loaded))
        print("Loaded decoded text length:", len(my_decoded_text_loaded))

        print("\nIf texts are the same: ", my_decoded_text_loaded == data)
        print("Average code len: ", average_len)
        print("Coding efficiency (H/L): ", calculate_entropy(data, 1) / average_len)

'''
1. Średnia długość kodu:  4.3090155002237935
2. Efektywność kodowania: 0.9933582848516693
'''