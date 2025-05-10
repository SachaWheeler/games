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

def get_wordlist(WORDFILE, N, SQUARE):
    n = N - int(N/3) if not SQUARE else N
    if os.path.isfile(WORDFILE):
        with open(WORDFILE, encoding="utf-8", errors="ignore") as file:
            word_list = set(
                word.strip().lower()
                for word in file
                if n <= len(word.strip()) <= N  # and word.strip().isalpha()
            )
    else:  # nltk
        defined_words = get_wordnet_defined_words()
        word_list = set(
            word.strip().lower()
            for word in defined_words
            if n <= len(word.strip()) <= N  # and word.strip().isalpha()
        )
        WORDFILE = "nltk"
    return(word_list, WORDFILE, n)

def get_words(word_list, N):
    words = set(
        word.strip().lower()
        for word in word_list
        if len(word.strip()) == N  # and word.strip().isalpha()
    )
    words.update([
            word.strip().lower().rjust(N)
            for word in word_list
            if len(word.strip()) < N  # and word.strip().isalpha()
        ]
    )
    words.update([
            word.strip().lower().ljust(N)
            for word in word_list
            if len(word.strip()) < N  # and word.strip().isalpha()
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


def is_valid_prefix(square, row, N, R, prefix_dict):
    for col in range(N):
        col_prefix = "".join(square[i][col] for i in range(row + 1))

        if col_prefix not in prefix_dict:
            return False

        # Disallow exact row == column match (symmetry breaker) unless resusing (R)
        if not R and row + 1 == N:
            col_word = "".join(square[i][col] for i in range(N))
            if col_word in square:
                return False

    return True

def output_square(square):
    N = len(square)
    results = "\n".join([" ".join(word) for word in square])
    with open(f"results/output-{N}.txt", "a") as output:
        output.write(f"\n{results}\n")
        output.write(f"{'-' * 2*N}\n")
        questions = []
        for word in square:
            if word.strip() not in questions:
                questions.append((word.strip(), define_word(word.strip())))
        cols = ["".join(row[i] for row in square) for i in range(N)]
        for word in cols:
            if word.strip() not in questions:
                questions.append((word.strip(), define_word(word.strip())))
        questions = list(set(questions))
        questions.sort(key=lambda x: x[0])
        for question in questions:
            output.write(f"{question[0].strip().ljust(N)}: ({len(question[0])}) {question[1]}\n")
        output.write(f"{'-' * 2*N}\n")

def build_square(start_word, word_list, prefix_dict, N, R):
    squares = []

    def backtrack(square, used_words):
        if len(square) == N:
            squares.append(square[:])

            output_square(square)
            return

        for candidate in word_list:
            if candidate in used_words:
                continue
            square.append(candidate)
            used_words.add(candidate)

            if is_valid_prefix(square, len(square) - 1, N, R, prefix_dict):
                backtrack(square, used_words)

            square.pop()
            used_words.remove(candidate)

    backtrack([start_word], set([start_word]))
    return squares


def worker(args):
    start_word, word_list, prefix_dict, N, R = args
    random.shuffle(word_list)

    return build_square(start_word, word_list, prefix_dict, N, R)

def init_worker():
    # Ignore SIGINT in child processes; main will handle it
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def find_word_squares(word_list, N, R):
    word_list = [w.lower() for w in word_list if len(w) == N]
    prefix_dict = build_prefix_dict(word_list, N)

    args = [(word, word_list, prefix_dict, N, R) for word in word_list]

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

