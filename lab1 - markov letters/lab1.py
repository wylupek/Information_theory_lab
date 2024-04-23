import random
import string
from collections import defaultdict

def ex1(is_print = True):
    word_counter = 0
    word_len = 0
    previous_space = False

    for i in range(1000000):
        random_number = random.randint(0, 26)
        if is_print:
            if random_number == 26:
                print(' ', end='')
            else:
                print(chr(97+random_number), end='')

        if random_number != 26 and previous_space == True:
            previous_space = False
            word_counter += 1
            word_len += 1
        elif random_number != 26 and previous_space == False:
            word_len += 1
        else:
            previous_space = True
    print("\n", word_len/word_counter)
        

def ex2():
    letters = string.ascii_lowercase + ' '
    alphabet_dict = {letter: 0 for letter in letters}
    with open("norm_wiki_sample.txt", 'r') as file:
        content = file.read()
        for letter in content:
            if letter in letters:
                alphabet_dict[letter] += 1

    letter_counter = 0
    for i in alphabet_dict:
        letter_counter += alphabet_dict[i]
    for i in alphabet_dict:
        alphabet_dict[i] = round(alphabet_dict[i] / letter_counter * 100, 2)
    print(alphabet_dict)
    print(sorted(alphabet_dict.items(), key=lambda x: x[1], reverse=True))

def ex3():
    letters = string.ascii_lowercase + ' '
    alphabet_dict = {letter: 0 for letter in letters}
    with open("norm_romeo.txt", 'r') as file:
        content = file.read()
        for letter in content:
            if letter in letters:
                alphabet_dict[letter] += 1

    letter_counter = 0
    for i in alphabet_dict:
        letter_counter += alphabet_dict[i]
    for i in alphabet_dict:
        alphabet_dict[i] = round(alphabet_dict[i] / letter_counter * 100, 2)

    char_list = random.choices(list(alphabet_dict.keys()), weights=alphabet_dict.values(), k=100000)
    my_str = "".join(char_list)

    word_counter = 0
    word_len = 0
    previous_space = False
    with open("norm_romeo.txt", 'r') as file:
        content = file.read()
        for letter in content:
            if letter != ' ' and previous_space == True:
                previous_space = False
                word_counter += 1
                word_len += 1
            elif letter != ' ' and previous_space == False:
                word_len += 1
            else:
                previous_space = True
    print("\nDla korpusu: ", word_len/word_counter)
    word_len = 0
    word_counter = 0

    for letter in my_str:
        if letter != ' ' and previous_space == True:
            previous_space = False
            word_counter += 1
            word_len += 1
        elif letter != ' ' and previous_space == False:
            word_len += 1
        else:
            previous_space = True
    print("\nDla wygenerowanego: ", word_len/word_counter)


def ex4():
    letters = string.ascii_lowercase + ' '
    alphabet_dict = {letter: 0 for letter in letters}
    with open("norm_romeo.txt", 'r') as file:
        corpus = file.read()
        for letter in corpus:
            if letter in letters:
                alphabet_dict[letter] += 1

    letter_counter = 0
    for i in alphabet_dict:
        letter_counter += alphabet_dict[i]
    for i in alphabet_dict:
        alphabet_dict[i] = round(alphabet_dict[i] / letter_counter * 100, 2)

    alphabet_dict = sorted(alphabet_dict.items(), key=lambda x: x[1], reverse=True)

    # Stwórz słownik przechowujący drugi najczęściej występujący znak i znaki po nim
    char_dict = defaultdict(list)

    # Przechodzimy przez korpus i zbieramy informacje
    for i in range(len(corpus) - 1):
        current_char = corpus[i]
        second_char = corpus[i + 1]
        char_dict[current_char].append(second_char)

    # Oblicz prawdopodobieństwo wystąpienia poszczególnych znaków po każdym z drugiego najczęściej występującego znaku
    probability_dict = defaultdict(dict)
    for key, value in char_dict.items():
        total = len(value)
        char_count = defaultdict(int)
        for char in value:
            char_count[char] += 1
        for char, count in char_count.items():
            probability_dict[key][char] = count / total

    print(f'{alphabet_dict[0]} - {probability_dict[alphabet_dict[0][0]]}\n'
          f'{alphabet_dict[1]} - {probability_dict[alphabet_dict[1][0]]}')


def ex5_1():
    letters = string.ascii_lowercase + ' '
    alphabet_dict = {letter: 0 for letter in letters}
    with open("norm_hamlet.txt", 'r') as file:
        corpus = file.read()
        for letter in corpus:
            if letter in letters:
                alphabet_dict[letter] += 1

    letter_counter = 0
    for i in alphabet_dict:
        letter_counter += alphabet_dict[i]
    for i in alphabet_dict:
        alphabet_dict[i] = round(alphabet_dict[i] / letter_counter * 100, 2)

    # alphabet_dict_sorted = sorted(alphabet_dict.items(), key=lambda x: x[1], reverse=True)

    # Stwórz słownik przechowujący drugi najczęściej występujący znak i znaki po nim
    char_dict = defaultdict(list)

    # Przechodzimy przez korpus i zbieramy informacje
    for i in range(len(corpus) - 1):
        current_char = corpus[i]
        second_char = corpus[i + 1]
        char_dict[current_char].append(second_char)

    # Oblicz prawdopodobieństwo wystąpienia poszczególnych znaków po każdym z drugiego najczęściej występującego znaku
    probability_dict = defaultdict(dict)
    for key, value in char_dict.items():
        total = len(value)
        char_count = defaultdict(int)
        for char in value:
            char_count[char] += 1
        for char, count in char_count.items():
            probability_dict[key][char] = count / total

    # Przybliżenie pierwszego rzędu
    char_list = random.choices(list(alphabet_dict.keys()), weights=alphabet_dict.values())
    for i in range(300):
        char_list += random.choices(list(probability_dict[char_list[-1]].keys()),
                                    weights=probability_dict[char_list[-1]].values())
    print("Przybliżenie 1-rzędu")
    my_str = ''.join(char_list)
    print("Wygenerowano: ", my_str)
    total_len = 0
    total_words = len(my_str.split())
    for i in my_str.split():
        total_len += len(i)
    print("Średnia długośc słowa: ", total_len/total_words, '\n')



def ex5_2():
    letters = string.ascii_lowercase + ' '
    alphabet_dict = {letter: 0 for letter in letters}
    with open("norm_hamlet.txt", 'r') as file:
        corpus = file.read()
        for letter in corpus:
            if letter in letters:
                alphabet_dict[letter] += 1

    letter_counter = 0
    for i in alphabet_dict:
        letter_counter += alphabet_dict[i]
    for i in alphabet_dict:
        alphabet_dict[i] = round(alphabet_dict[i] / letter_counter * 100, 2)

    # alphabet_dict_sorted = sorted(alphabet_dict.items(), key=lambda x: x[1], reverse=True)

    # Stwórz słownik przechowujący drugi najczęściej występujący znak i znaki po nim
    char_dict = defaultdict(list)

    # Przechodzimy przez korpus i zbieramy informacje
    for i in range(len(corpus) - 3):
        current_char = corpus[i]
        second_char = corpus[i + 1]
        third = corpus[i + 2]
        fourth = corpus[i + 3]
        char_dict[current_char + second_char + third].append(fourth)

    # Oblicz prawdopodobieństwo wystąpienia poszczególnych znaków po każdym z drugiego najczęściej występującego znaku
    probability_dict = defaultdict(dict)
    for key, value in char_dict.items():
        total = len(value)
        char_count = defaultdict(int)
        for char in value:
            char_count[char] += 1
        for char, count in char_count.items():
            probability_dict[key][char] = count / total

    # Przybliżenie trzeciego rzędu
    char_list = ['t', 'h', 'e']
    for i in range(300):
        char_list += random.choices(list(probability_dict[''.join(char_list[-3:])].keys()),
                                    weights=probability_dict[''.join(char_list[-3:])].values())
    print("Przybliżenie 3-rzędu")
    my_str = ''.join(char_list)
    print("Wygenerowano: ", my_str)
    total_len = 0
    total_words = len(my_str.split())
    for i in my_str.split():
        total_len += len(i)
    print("Średnia długośc słowa: ", total_len / total_words, '\n')


def ex5_3():
    letters = string.ascii_lowercase + ' '
    alphabet_dict = {letter: 0 for letter in letters}
    with open("norm_hamlet.txt", 'r') as file:
        corpus = file.read()
        for letter in corpus:
            if letter in letters:
                alphabet_dict[letter] += 1

    letter_counter = 0
    for i in alphabet_dict:
        letter_counter += alphabet_dict[i]
    for i in alphabet_dict:
        alphabet_dict[i] = round(alphabet_dict[i] / letter_counter * 100, 2)

    # alphabet_dict_sorted = sorted(alphabet_dict.items(), key=lambda x: x[1], reverse=True)

    # Stwórz słownik przechowujący drugi najczęściej występujący znak i znaki po nim
    char_dict = defaultdict(list)

    # Przechodzimy przez korpus i zbieramy informacje
    for i in range(len(corpus) - 5):
        current_char = corpus[i]
        second_char = corpus[i + 1]
        third_char = corpus[i + 2]
        fourth_char = corpus[i + 3]
        fifth_char = corpus[i + 4]
        sixth_char = corpus[i + 5]
        char_dict[current_char + second_char + third_char + fourth_char + fifth_char].append(sixth_char)

    # Oblicz prawdopodobieństwo wystąpienia poszczególnych znaków po każdym z drugiego najczęściej występującego znaku
    probability_dict = defaultdict(dict)
    for key, value in char_dict.items():
        total = len(value)
        char_count = defaultdict(int)
        for char in value:
            char_count[char] += 1
        for char, count in char_count.items():
            probability_dict[key][char] = count / total


    # Przybliżenie piątego rzędu
    char_list = ['p', 'r', 'o', 'b', 'a', 'b', 'i', 'l', 'i', 't', 'y']
    for i in range(300):
        char_list += random.choices(list(probability_dict[''.join(char_list[-5:])].keys()),
                                    weights=probability_dict[''.join(char_list[-5:])].values())

    print("Przybliżenie 5-rzędu")
    my_str = ''.join(char_list)
    print("Wygenerowano: ", my_str)
    total_len = 0
    total_words = len(my_str.split())
    for i in my_str.split():
        total_len += len(i)
    print("Średnia długośc słowa: ", total_len / total_words)


if __name__ == "__main__":
    ex5_1()
    ex5_2()
    ex5_3()

        
        






