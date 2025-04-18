#!/usr/bin/env python
import re
import time
from nltk.corpus import words
import argparse
import os
import random
# from functools import cache


def create_grid(wordlist, N):
    grid = [['' for _ in range(N)] for _ in range(N)]
    if fill_grid(grid, 0, N, wordlist):
        return grid
    else:
        return None

# @cache
def fill_grid(grid, row, N, wordlist):
    # Base case: all rows are filled
    if row == N:
        return True

    # Try each word in the wordlist for the current row
    for word in wordlist:
        # only consider words which match the index col if REUSE_WORDS
        if REUSE_WORDS and \
                [word[i] for i in range(row)] != [grid[j][row] for j in range(row)]:
            continue
        if word in used_words_in_grid(grid):  # Don't repeat rows
            continue

        # Place the word in the current row
        grid[row] = list(word)

        # debugging
        print([''.join(sublist) for sublist in grid], word, "               ", end='\r')

        # Check if this row is valid by examining each column regex
        if all(has_valid_column_match(grid,
            col, N, wordlist, used_words_in_grid(grid)) for col in range(N)):
            # Recursively try to fill the next row
            if fill_grid(grid, row + 1, N, wordlist):
                return True

        # Undo the row placement (backtracking)
        grid[row] = [''] * N

    # No valid words found for this configuration
    return False

def has_valid_column_match(grid, col, N, wordlist, used_words):
    # Construct a regex pattern for the current column
    pattern = ''.join(grid[row][col] if grid[row][col] else '.' for row in range(N))
    regex = re.compile(f"^{pattern}$")

    # Check if there's at least one word in wordlist that matches the column pattern
    # and is not already used in any row of the grid
    return any(regex.match(word) and word not in used_words for word in wordlist)

# @cache
def used_words_in_grid(grid):
    # Gather a set of all words currently used in the rows of the grid
    if REUSE_WORDS:
        return {}
    else:
        return {''.join(row) for row in grid if all(row)}


def out(output, message):
    print(message)
    output.write(message + "\n")

def display_grid(grid, execution_time):
    if grid:
        with open('output.txt', 'a') as output:
            out(output, f"----------------\n"
            f"{N}x{N} Grid of words in {execution_time:.2f}s:\n"
            f"{FILENAME if FILENAME else 'nltk'}\n")

            for row in grid:
                out(output, " ".join(row))
            if not REUSE_WORDS:
                out(output, "\nColumns:\n")
                for i in range(N):
                    out(output, " ".join(row[i] for row in grid))
            out(output, "\n")
    else:
        print("No valid grid found.")

def get_wordlist(FILENAME, N):
    try:
        with open(FILENAME, "r") as file:
            wordlist = set(word.strip().lower() for word in file \
                    if len(word.strip()) == N and \
                    word.strip().isalpha())
    except:
        wordlist = set(word.strip().lower() for word in words.words() \
                if len(word.strip()) == N and \
                word.strip().isalpha())
    return wordlist

def log_results(N, wl_length, filename, execution_time):
    with open("results.csv", "a") as results:
        results.write(f"{N}, {wl_length},"
                f"\'{filename if filename else 'nltk'}\',"
                f"{'reuse' if REUSE_WORDS else 'unigue'},"
                f"{execution_time:.2f}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="enter an optional dictionary path and N.")
    parser.add_argument("file", nargs="?", type=str, help="Path to a dictionary file")
    parser.add_argument("number", nargs="?", type=int, help="Size of grid")
    parser.add_argument("reuse", nargs="?", type=str, help="Reuse words")
    args = parser.parse_args()

    if args.file and os.path.isfile(args.file):
        FILENAME=args.file
    else:
        FILENAME = None

    if args.number is not None and args.number > 1:  # and args.number < 10:
        N = args.number
    else:
        N = 7

    if args.reuse is not None:
        REUSE_WORDS = True  # if True, words are reused in cols
    else:
        REUSE_WORDS = not True

    wordlist = list(get_wordlist(FILENAME, N))
    random.shuffle(wordlist)
    # print(wordlist)

    print(f"starting with {N=},"
            f"{FILENAME if FILENAME else 'nltk'}"
            f"({len(wordlist):,} words) {'' if REUSE_WORDS else 'not '}reusing")

    start_time = time.time()
    grid = create_grid(wordlist, N)
    end_time = time.time()
    execution_time = end_time - start_time
    if grid:
        log_results(N, len(wordlist), FILENAME, execution_time)
    else:
        log_results(N, len(wordlist), FILENAME, None)

    display_grid(grid, execution_time)

