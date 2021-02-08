from collections import defaultdict
from random import choices, choice

from nltk.util import trigrams


def generate_sentence(beginning=None):
    endings = ('!', '.', '?')
    output = []
    if not beginning:
        #  generate first two words
        word = choice(list(dictionary.keys()))
        #  re-roll word if it ends with full stops
        while any(ending in word for ending in endings) \
                or not word[0].isupper():
            word = choice(list(dictionary.keys()))
    else:
        word = beginning
    output.append(word)
    sent_end = word
    last_word = word.split()[1]

    for _ in range(3):
        #  generate next word based on the current one
        tails = choices(list(dictionary[sent_end].keys()), list(dictionary[sent_end].values()))

        for tail in tails:
            if not tail.endswith(endings):
                output.append(tail)
                sent_end = f"{last_word} {tail}"
                last_word = tail
                break

        if last_word not in tails:
            return generate_sentence()

    for _ in range(30):
        tail = choices(list(dictionary[sent_end].keys()), list(dictionary[sent_end].values()))[0]
        sent_end = f"{last_word} {tail}"
        last_word = tail
        output.append(tail)

        if tail.endswith(endings):
            break

    return ' '.join(output)


filename = input() or 'corpus.txt'

with open(filename, 'r', encoding='utf-8') as source:
    text = source.read().split()

trigrams = [((x[0], x[1]), x[2]) for x in trigrams(text)]
dictionary = defaultdict(lambda: defaultdict(int))

for head, tail in trigrams:
    dictionary[' '.join(head)][tail] += 1

for _ in range(10):
    sentence = generate_sentence()
    print(sentence)
