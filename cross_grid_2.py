import nltk
from nltk.corpus import words, stopwords
from collections import defaultdict
import sys

# Uncomment if needed
# nltk.download('words')
# nltk.download('stopwords')

"""
def load_words(word_length):
    word_list = [w.lower() for w in words.words() if len(w) == word_length and w.isalpha()]
    stops = set(stopwords.words('english'))
    filtered = [w for w in word_list if w not in stops]
    return list(set(filtered))  # remove duplicates
"""
def load_words(word_length, filename='nouns.txt'):
    """Load words of a given length from a custom word list file."""
    with open(filename, 'r') as f:
        words = [line.strip().lower() for line in f if len(line.strip()) == word_length and line.strip().isalpha()]
    return list(set(words))


def build_prefix_map(word_list):
    """Build a map of all prefixes to words starting with those prefixes."""
    prefix_map = defaultdict(list)
    for word in word_list:
        for i in range(1, len(word)):
            prefix = word[:i]
            prefix_map[prefix].append(word)
    return prefix_map

def is_valid_prefix(square, new_word, prefix_map):
    """Check that all columns formed with new_word are valid prefixes."""
    n = len(square) + 1  # the next row number
    for col in range(len(new_word)):
        prefix = ''.join(row[col] for row in square) + new_word[col]
        if prefix not in prefix_map:
            return False
    return True

def is_valid_square(square, word_set):
    """Check if all columns are valid words."""
    size = len(square)
    for col in range(size):
        column_word = ''.join(row[col] for row in square)
        if column_word not in word_set:
            return False
    return True

def build_squares(size, word_list, prefix_map, word_set, square=[], results=[]):
    if len(square) == size:
        if is_valid_square(square, word_set):
            results.append(square[:])
        return

    for word in word_list:
        if word in square:
            continue
        if len(square) == 0 or is_valid_prefix(square, word, prefix_map):
            square.append(word)
            build_squares(size, word_list, prefix_map, word_set, square, results)
            square.pop()

def main(size):
    word_list = load_words(size)
    word_set = set(word_list)
    prefix_map = build_prefix_map(word_list)

    results = []
    build_squares(size, word_list, prefix_map, word_set, [], results)

    print(f"\nFound {len(results)} valid {size}x{size} word squares:\n")
    for square in results:
        for row in square:
            print(row)
        print('-' * (2 * size))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python word_square.py <size>")
        sys.exit(1)
    size = int(sys.argv[1])
    main(size)

