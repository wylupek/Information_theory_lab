import bitarray as ba
from collections import Counter
import math
import json


def createOld(freq_dict: dict) -> dict:
    code_format = "0" + str(math.ceil(math.log2(len(freq_dict)))) + "b"
    return {item: format(i, code_format)
            for i, item in enumerate(freq_dict)}


def encodeOld(text, code) -> ba.bitarray:
    encoded_text = ba.bitarray()
    for letter in text:
        encoded_text.extend(ba.bitarray(code[letter]))
    return encoded_text


def decodeOld(encoded_text, code) -> str:
    code_inv = {v: k for k, v in code.items()}
    decoded_text = ""
    current_code = ""
    for bit in encoded_text:
        current_code += '1' if bit else '0'
        if current_code in code_inv:
            decoded_text += code_inv[current_code]
            current_code = ""
    return decoded_text


def saveOld(filename, code, encoded_text):
    with open(filename + ".bin", 'wb') as file:
        encoded_text.tofile(file)

    with open(filename + "_code.json", 'w') as file:
        json.dump(code, file)


def loadOld(filename):
    with open(filename + ".bin", 'rb') as file:
        encoded_text = ba.bitarray()
        encoded_text.fromfile(file)

    with open(filename + "_code.json", 'r') as file:
        code = json.load(file)

    return code, encoded_text


def load(file_path):
    bit_array = ba.bitarray()
    with open(file_path, 'rb') as file:
        bit_array.fromfile(file)
    return bit_array


def encode(bit_array: ba.bitarray):
    code = [0, 1]

    s = bit_array[0]
    for c in bit_array[1:]:
        if c in code:
            s = s + c

            continue



if __name__ == '__main__':
    # my_filename = "test.txt"
    # bit_array = load(my_filename)
    my_bit_array = ba.bitarray("101001000")
    encode(my_bit_array)

# 1 0 4 2 3 0 2
