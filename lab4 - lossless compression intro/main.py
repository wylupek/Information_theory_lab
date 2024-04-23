import bitarray as ba
from collections import Counter
import math
import json


def create(freq_dict: dict) -> dict:
    code_format = "0" + str(math.ceil(math.log2(len(freq_dict)))) + "b"
    return {item: format(i, code_format)
            for i, item in enumerate(freq_dict)}


def encode(text, code) -> ba.bitarray:
    encoded_text = ba.bitarray()
    for letter in text:
        encoded_text.extend(ba.bitarray(code[letter]))
    return encoded_text


def decode(encoded_text, code) -> str:
    code_inv = {v: k for k, v in code.items()}
    decoded_text = ""
    current_code = ""
    for bit in encoded_text:
        current_code += '1' if bit else '0'
        if current_code in code_inv:
            decoded_text += code_inv[current_code]
            current_code = ""
    return decoded_text


def save(filename, code, encoded_text):
    with open(filename + ".bin", 'wb') as file:
        encoded_text.tofile(file)

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
    my_filename = "norm_wiki_sample.txt"
    with open(my_filename, 'r') as my_file:
        data = my_file.read()
        data_len = len(data)
        freq = {item: count / len(data)
                for item, count in sorted(Counter(data).items(), key=lambda x: x[1], reverse=True)}

        my_code = create(freq)
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
        print("If texts are the same: ", my_decoded_text_loaded == data)
''' 
1.  Jest różnych 37 znaków (litery + cyfry + spacja).
    Najkrótsza możliwa długość kodu dla tego pliku to 6 (math.ceil(math.log2(len(freq_dict))))
2.  Stopień kompresji wynosi 10537 / (7903 + 1) = 1.33, lub inaczej 8 / 6 
3.  Można zastosować inne techniki kompresji np. kodowanie Huffmana
4.  Nieużyte kody są marnowane. Można zastosować inne podejscie np. kodowanie Huffmana
5.  Odkodowywanie kodów o zmiennej długości polega na odczytywaniu bitów z zakodowanego tekstu i dopasowywaniu 
    ich do odpowiadających im symboli. (kodowanie Huffmana)
6.  Granica zależy od ilości znaków w tekscie. Dla norm_wiki_sample.txt stopien kompresji wynosi 8/6. Gdyby tekst
    nie posiadał cyfr, to stopien kompresji wynosiłby 8/5.
'''
