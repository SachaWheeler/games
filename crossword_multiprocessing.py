import multiprocessing as mp
from collections import defaultdict
from nltk.corpus import words
import os
import argparse
import copy
import random


def get_words(word_list):
    words = set(
        word.strip().lower()
        for word in word_list
        if len(word.strip()) == N and word.strip().isalpha()
    )
    words.update([
            word.strip().lower().rjust(N)
            for word in word_list
            if len(word.strip()) == N-1 and word.strip().isalpha()
        ]
    )
    words.update([
            word.strip().lower().ljust(N)
            for word in word_list
            if len(word.strip()) == N-1 and word.strip().isalpha()
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


def find_word_squares(word_list, N):
    word_list = [w.lower() for w in word_list if len(w) == N]
    prefix_dict = build_prefix_dict(word_list, N)

    args = [(word, word_list, prefix_dict, N) for word in word_list]

    with mp.Pool() as pool:
        results = pool.map(worker, args)

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
                    if len(word.strip()) in [N, N-1] and word.strip().isalpha()
                    )
    else:  # nltk
        word_list = set(
            word.strip().lower()
            for word in words.words()
            if len(word.strip()) in [N, N-1] and word.strip().isalpha()
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
