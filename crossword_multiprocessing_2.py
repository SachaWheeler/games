from nltk.corpus import words
import os
import argparse
import nltk

from utils import (define_word, get_wordnet_defined_words, get_words,
                   build_prefix_dict, is_valid_prefix, output_square, build_square,
                   worker, init_worker, find_word_squares,
                   get_wordlist)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Word Square finder")

    parser.add_argument("--file", type=str, default="words.txt", help="Wordlist file")
    parser.add_argument("--num", type=int, default=5, help="Size of the square")
    parser.add_argument("--reuse", action="store_true", default=False, help="Unique words?")
    parser.add_argument("--square", action="store_true", default=False, help="Unique words?")

    args = parser.parse_args()

    WORDFILE = args.file
    N = args.num
    R = args.reuse
    SQUARE = args.square

    word_list, WORDFILE, n = get_wordlist(WORDFILE, N, SQUARE)
    words = get_words(word_list, N)

    legend = f"{n} - {N} letters from {WORDFILE} ({len(words):,} {SQUARE=} {R=})"
    print(legend)
    output_file = f"results/output-{N}.txt"
    print(f"writing to {output_file}")
    with open(output_file, "a") as output:
        output.write(f"\n{legend}\n")

    squares = find_word_squares(words, N, R)
    legend += f" ({len(squares):,} squares from {len(words):,} words)"

    print(f"{len(squares):,} squares")
