import nltk
from nltk.corpus import words, stopwords
from collections import defaultdict
import sys

# Uncomment if needed
# nltk.download('words')
# nltk.download('stopwords')

def get_valid_words(length):
    word_list = [w.lower() for w in words.words() if len(w) == length and w.isalpha()]
    stop_words = set(stopwords.words('english'))
    return [w for w in word_list if w not in stop_words]

def build_prefix_map(word_list):
    """Map from prefix to list of words starting with that prefix"""
    prefix_map = defaultdict(list)
    for word in word_list:
        for i in range(1, len(word) + 1):
            prefix = word[:i]
            prefix_map[prefix].append(word)
    return prefix_map

def is_valid_prefix(prefix_map, square, word, level):
    """Check if adding 'word' to the current square keeps all columns valid"""
    for col in range(len(word)):
        prefix = ''.join(row[col] for row in square) + word[col]
        if prefix not in prefix_map:
            return False
    return True

def backtrack(x, word_list, prefix_map, square, used, results):
    if len(square) == x:
        # Final check: make sure each column is a full valid word
        for col in range(x):
            col_word = ''.join(row[col] for row in square)
            if col_word not in word_list:
                return
        results.append(square[:])
        return

    for word in word_list:
        if word in used:
            continue
        if not square or is_valid_prefix(prefix_map, square, word, len(square)):
            square.append(word)
            used.add(word)
            backtrack(x, word_list, prefix_map, square, used, results)
            used.remove(word)
            square.pop()

def find_word_squares(x):
    word_list = get_valid_words(x)
    word_set = set(word_list)
    prefix_map = build_prefix_map(word_list)

    results = []
    backtrack(x, word_set, prefix_map, [], set(), results)
    return results

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python word_square.py <x>")
        sys.exit(1)

    x = int(sys.argv[1])
    print(f"Building {x}x{x} word squares...")
    squares = find_word_squares(x)

    print(f"\nFound {len(squares)} word square(s):\n")
    for square in squares:
        for row in square:
            print(row)
        print("-" * (x * 2))

