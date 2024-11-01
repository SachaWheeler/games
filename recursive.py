#!/usr/bin/env python
import re
import time
from nltk.corpus import words
import argparse
import os
import random


def create_grid(wordlist, N):
    grid = [['' for _ in range(N)] for _ in range(N)]
    if fill_grid(grid, 0, N, wordlist):
        return grid
    else:
        return None

def fill_grid(grid, row, N, wordlist):
    # wl = list(wordlist)
    # random.shuffle(list(wl))
    # wordlist = set(wl)
    # Base case: all rows are filled
    if row == N:
        return True

    # Try each word in the wordlist for the current row
    for word in wordlist:
        # Place the word in the current row
        grid[row] = list(word)
        print([''.join(sublist) for sublist in grid], word,
                "               ", end='\r')


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
    # Construct a partial regex pattern for the current column
    pattern = ''.join(grid[row][col] if grid[row][col] else '.' for row in range(N))
    regex = re.compile(f"^{pattern}$")

    # Check if there's at least one word in wordlist that matches the column pattern
    # and is not already used in any row of the grid
    return any(regex.match(word) and word not in used_words for word in wordlist)

def used_words_in_grid(grid):
    # Gather a set of all words currently used in the rows of the grid
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
            out(output, "\nColumns:\n")
            for i in range(N):
                out(output, " ".join(row[i] for row in grid))
            out(output, "\n")
    else:
        print("No valid grid found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="enter an optional dictionary path and N.")
    parser.add_argument("file", nargs="?", type=str, help="Path to a dictionary file")
    parser.add_argument("number", nargs="?", type=int, help="Size of grid")
    args = parser.parse_args()

    if args.file and os.path.isfile(args.file):
        FILENAME=args.file
    else:
        FILENAME="words_alpha_2.txt"

    if args.number is not None and args.number > 1 and args.number < 10:
        N = args.number
    else:
        N = 4

    print(f"starting with {N=}, {FILENAME if FILENAME else 'nltk'}")

    try:
        with open(FILENAME, "r") as file:
            wordlist = set(word.strip().lower() for word in file \
                    if len(word.strip()) == N and \
                    word.strip().isalpha())
    except:
        wordlist = set(word.strip().lower() for word in words.words() \
                if len(word.strip()) == N and \
                word.strip().isalpha())

    # print(wordlist)
    start_time = time.time()

    grid = create_grid(wordlist, N)
    print()

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"done in {execution_time:.0f}s")

    display_grid(grid, execution_time)

