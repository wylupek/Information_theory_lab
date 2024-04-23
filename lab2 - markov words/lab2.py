import random
import string
from collections import defaultdict

def ex1():
    with open("norm_wiki_sample.txt", 'r') as file:
        corpus = file.read()
        # Podziel tekst na słowa, usuń znaki interpunkcyjne i zmień wszystkie litery na małe
        words = corpus.split()
        words = [word.strip(".,!?") for word in words]
        words = [word.lower() for word in words]
        words_number = len(words)

        # Utwórz słownik z liczbą wystąpień każdego słowa
        word_count = {}
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1

        word_count = dict(sorted(word_count.items(), key=lambda x: x[1], reverse=False))
        for key, value in word_count.items():
            word_count[key] = value / words_number
        return word_count


def ex2():
    word_count = ex1()
    word_list = random.choices(list(word_count.keys()), weights=list(word_count.values()), k=300)
    for word in word_list:
        print(word, end=' ')


def ex3(n: int):
    with open("norm_wiki_sample.txt", 'r') as file:
        corpus = file.read()
        words = corpus.split()
        words = [word.lower() for word in words]
        words_number = len(words)

        word_dict = defaultdict(list)
        for i in range(words_number - n):
            first_words = words[i]
            for j in range(n - 1):
                first_words += ' ' + words[i + 1 + j]
            last_word = words[i + n]
            word_dict[first_words].append(last_word)

        word_prob_dict = defaultdict(dict)
        for key, value in word_dict.items():
            total = len(value)
            word_count = defaultdict(int)
            for word in value:
                word_count[word] += 1
            for word, count in word_count.items():
                word_prob_dict[key][word] = count / total

        # Przybliżenie pierwszego rzędu
        word_list = ['probability', 'of']
        for i in range(300):
            word_list += random.choices(list(word_prob_dict[' '.join(word_list[-n:])].keys()),
                                        weights=list(word_prob_dict[' '.join(word_list[-n:])].values()))
        print("Przybliżenie 1-rzędu")
        my_str = ' '.join(word_list)
        print("Wygenerowano: ", my_str)


if __name__ == "__main__":
    # ex1()
    # ex2()
    ex3(2)

