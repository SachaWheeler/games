import multiprocessing as mp
from collections import defaultdict
from nltk.corpus import words
import os
import argparse
import copy
import random
import sys
import signal

from nltk.corpus import wordnet as wn
import nltk

# Make sure WordNet is downloaded
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

def define_word(word):
    synsets = wn.synsets(word)
    if not synsets:
        return f"No definition found for '{word}'."

    # Just get the first synset (most common meaning)
    definition = synsets[0].definition()
    return definition

def get_wordnet_defined_words():
    return set(wn.all_lemma_names())

def get_words(word_list):
    words = set(
        word.strip().lower()
        for word in word_list
        if len(word.strip()) == N and word.strip().isalpha()
    )
    words.update([
            word.strip().lower().rjust(N)
            for word in word_list
            if len(word.strip()) < N and word.strip().isalpha()
        ]
    )
    words.update([
            word.strip().lower().ljust(N)
            for word in word_list
            if len(word.strip()) < N and word.strip().isalpha()
        ]
    )
    return words

def build_prefix_dict(words, N):
    prefix_dict = defaultdict(list)
    for word in words:
        if len(word) != N:
            continue
        for i in range(1, N + 1):
            prefix_dict[word[:i]].append(word)
    return prefix_dict


def is_valid_prefix(square, row, N, prefix_dict):
    for col in range(N):
        col_prefix = "".join(square[i][col] for i in range(row + 1))

        if col_prefix not in prefix_dict:
            return False

        # Disallow exact row == column match (symmetry breaker)
        if row + 1 == N:
            col_word = "".join(square[i][col] for i in range(N))
            if col_word in square:
                return False

    return True


def build_square(start_word, word_list, prefix_dict, N):
    squares = []

    def backtrack(square, used_words):
        if len(square) == N:
            squares.append(square[:])

            results = "\n".join([" ".join(word) for word in square])
            with open(f"results/output-{N}.txt", "a") as output:
                output.write(f"\n{results}\n")
                output.write(f"{'-' * 2*N}\n")
                questions = []
                for word in square:
                    questions.append((word.strip(), define_word(word.strip())))
                cols = ["".join(row[i] for row in square) for i in range(N)]
                for word in cols:
                    questions.append((word.strip(), define_word(word.strip())))
                questions.sort(key=lambda x: x[0])
                for question in questions:
                    output.write(f"{question[0].strip().ljust(N)}: ({len(question[0])}) {question[1]}\n")
                output.write(f"{'-' * 2*N}\n")

            return

        for candidate in word_list:
            if candidate in used_words:
                continue
            square.append(candidate)
            used_words.add(candidate)

            if is_valid_prefix(square, len(square) - 1, N, prefix_dict):
                backtrack(square, used_words)

            square.pop()
            used_words.remove(candidate)

    backtrack([start_word], set([start_word]))
    return squares


def worker(args):
    start_word, word_list, prefix_dict, N = args
    random.shuffle(word_list)

    return build_square(start_word, word_list, prefix_dict, N)

def init_worker():
    # Ignore SIGINT in child processes; main will handle it
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def find_word_squares(word_list, N):
    word_list = [w.lower() for w in word_list if len(w) == N]
    prefix_dict = build_prefix_dict(word_list, N)

    args = [(word, word_list, prefix_dict, N) for word in word_list]

    try:
        with mp.Pool(initializer=init_worker) as pool:
            results = pool.map(worker, args)
    except KeyboardInterrupt:
        print("\n✋ Caught CTRL-C. Terminating workers...")
        pool.terminate()
        pool.join()
        sys.exit(1)

    all_squares = [square for sublist in results for square in sublist]
    return all_squares


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Word Square finder")

    parser.add_argument("--file", type=str, default="words.txt", help="Wordlist file")
    parser.add_argument("--num", type=int, default=5, help="Size of the square")

    args = parser.parse_args()
    N = args.num

    WORDFILE = args.file
    if os.path.isfile(WORDFILE):
        with open(WORDFILE, encoding="utf-8", errors="ignore") as file:
            word_list = set(
                    word.strip().lower()
                    for word in file
                    if len(word.strip()) in [N, N-1, N-2] and word.strip().isalpha()
                    )
    else:  # nltk
        defined_words = get_wordnet_defined_words()

        word_list = set(
            word.strip().lower()
            for word in defined_words
            if len(word.strip()) in [N, N-1, N-2, N-3] and word.strip().isalpha()
        )
        WORDFILE = "nltk"

    words = get_words(word_list)

    legend = f"{N} letters from {WORDFILE} ({len(words):,})"
    print(legend)
    with open(f"results/output-{N}.txt", "a") as output:
        output.write(f"\n{legend}\n")

    squares = find_word_squares(words, N)
    legend += f" ({len(squares):,} squares from {len(words):,} words)"

    """
    for square in squares:
        output.write("\n".join(square))
        output.write("\n---\n")
    """

    print(f"{len(squares):,} squares")
