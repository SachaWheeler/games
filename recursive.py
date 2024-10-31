#!/usr/bin/env python
import re

def filter_words(wordlist, length):
    """Filter words of a specific length from the wordlist."""
    return [word for word in wordlist if len(word) == length]

def is_valid(word, column_regex, position):
    """Check if a word can fit in the current row given column regex patterns."""
    return all(column_regex[i].match(word[i]) for i in range(position))

def build_grid(wordlist, N, grid=[]):
    """
    Recursive function to build an N x N grid where each row and column forms
    a valid word from the wordlist.
    """
    # Base case: if grid is complete, return it
    if len(grid) == N:
        return grid

    # If grid is empty, start by picking any word for the first row
    if not grid:
        for word in wordlist:
            result = build_grid(wordlist, N, grid + [word])
            # print(result)
            if result:
                return result
        return None

    # Generate column regex patterns based on current grid state
    column_regex = [re.compile(''.join([grid[row][col] if row < len(grid) else '.'
                                        for row in range(N)])) for col in range(N)]
    print(grid, column_regex)

    # filter wordlist by ALL of the regex conditions
    filtered_wordlist = [
            word for word in wordlist
            if all(pattern.search(word) for pattern in column_regex)
    ]
    print(filtered_wordlist)
    exit

    # Try adding a word to the next row, respecting the column constraints
    for word in wordlist:
        if is_valid(word, column_regex, len(grid)):
            result = build_grid(wordlist, N, grid + [word])
            if result:
                return result

    return None  # No valid grid found


FILENAME="words_alpha_2.txt"
N = 5

with open(FILENAME, "r") as file:
    wordlist = {word.strip().lower() for word in file \
            if len(word.strip()) == N and \
            word.strip().isalpha()}

filtered_wordlist = filter_words(wordlist, N)
grid = build_grid(filtered_wordlist, N)

if grid:
    print("\nGenerated Grid:")
    for row in grid:
        print(row)
else:
    print("No valid grid found.")

