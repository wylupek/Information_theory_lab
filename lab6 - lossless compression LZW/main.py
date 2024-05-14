import bitarray as ba
from collections import Counter
import math
import json


def create(data: list) -> dict:
    freq_dict = {item: count / len(data)
                 for item, count in sorted(Counter(data).items(), key=lambda x: x[1], reverse=True)}
    code_format = "0" + str(math.ceil(math.log2(len(freq_dict)))) + "b"
    return {item: format(i, code_format)
            for i, item in enumerate(freq_dict)}


def save(filename: str, list_of_codes: list, codes: dict) -> None:
    with open(filename + ".bin", 'wb') as file:
        encoded_text = ba.bitarray()
        for code in list_of_codes:
            encoded_text.extend(ba.bitarray(codes[code]))
        encoded_text.tofile(file)

    codes["len"] = len(encoded_text)
    with open(filename + "_code.json", 'w') as file:
        json.dump(codes, file)


def load(filename):
    with open(filename + ".bin", 'rb') as file:
        encoded_text = ba.bitarray()
        encoded_text.fromfile(file)

    with open(filename + "_code.json", 'r') as file:
        code = json.load(file)

    return code, encoded_text


def load_file(file_path) -> ba.bitarray:
    bit_array = ba.bitarray()
    with open(file_path, 'rb') as file:
        bit_array.fromfile(file)
    return bit_array


def encode(bit_array: ba.bitarray, code_size: float) -> list:
    output = []
    lzw_code = {'0': 0, '1': 1}
    next_code = 2
    s = str(bit_array[0])
    for c in bit_array.to01()[1:]:
        x = s + c
        if x in lzw_code:
            s = x
        else:
            output.append(str(lzw_code[s]))
            if next_code < code_size:
                lzw_code[x] = next_code
                next_code += 1
            s = c
    output.append(str(lzw_code[s]))
    return output


def decode(bit_array: ba.bitarray, code, code_size: float):
    code_inv = {v: int(k) for k, v in list(code.items())[:-1]}
    decoded_codes = []
    current_code = ""
    try:
        for i in range(code["len"]):
            current_code += '1' if bit_array[i] else '0'
            if current_code in code_inv:
                decoded_codes.append(code_inv[current_code])
                current_code = ""
    except KeyError:
        for bit in bit_array:
            current_code += '1' if bit else '0'
            if current_code in code_inv:
                decoded_codes.append(code_inv[current_code])
                current_code = ""

    output = []
    lzw_code = {0: '0', 1: '1'}
    next_code = 2
    c = ''
    old = decoded_codes[0]
    output.append(lzw_code[old])

    for new in decoded_codes[1:]:
        if new in lzw_code:
            word = lzw_code[new]
        else:
            word = lzw_code[old] + c
        output.append(word)
        c = word[0]
        if next_code < code_size:
            lzw_code[next_code] = lzw_code[old] + c
            next_code += 1
        old = new
    return output


if __name__ == '__main__':
    my_code_size = 2**12
    my_filename = "../data/lena.bmp"

    # Load -> Encode -> Save
    my_bit_array = load_file(my_filename)
    encoded_data = encode(my_bit_array, my_code_size)
    my_code = create(encoded_data)
    save(my_filename, encoded_data, my_code)
    print("Loaded file len:", len(my_bit_array))

    # Load -> Decode -> Compare
    my_code_loaded, my_encoded_text_loaded = load(my_filename)
    decoded_data = ''.join(decode(my_encoded_text_loaded, my_code_loaded, my_code_size))
    print("Decoded data len:", len(decoded_data))
    print("If files are the same:", decoded_data == my_bit_array.to01())


'''
filename                    original    'inf'           2**12       2**18
norm_wiki_sample.txt        10537       6233+67074      8974+95     6560+8059
wiki_sample.txt             11630       7391+77434      10441+95    7606+8047
lena.bmp                    11255       10522+104620    12186+95    11373+8030

'''


# my_bit_array = ba.bitarray("101001000")
# 1 0 2 3 0 6
# 1 0 4 2 3 0 2
