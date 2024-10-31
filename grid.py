#!/usr/bin/env python

import random

def filter_wordlist(wordlist, grid, row_index):
    """
    Filters the wordlist to keep words that match the current grid columns.
    """
    grid_size = len(grid[0]) if grid else len(wordlist[0])
    filtered_words = []

    for word in wordlist:
        valid_word = True
        for col in range(grid_size):
            if row_index > 0 and len(grid) >= row_index:
                for prev_row in range(row_index):
                    if col < len(grid[prev_row]) and word[col] != grid[prev_row][col]:
                        valid_word = False
                        break
            if not valid_word or word in grid:
                break
        if valid_word:
            filtered_words.append(word)

    return filtered_words

def fill_grid(wordlist, grid, N):
    """
    Recursively fills the grid row by row.
    """
    # Base case: if the grid is full, return it
    if len(grid) == N:
        return grid

    # Filter wordlist to match current grid columns
    filtered_wordlist = filter_wordlist(wordlist, grid, len(grid))

    if not filtered_wordlist:
        return None

    # Choose a random word from the filtered list
    next_word = random.choice(filtered_wordlist)
    grid.append(next_word)

    # Recursive call to fill the next row
    return fill_grid(wordlist, grid, N)

def create_grid(wordlist, N):
    """
    Initializes an empty grid and starts the filling process.
    """
    # Ensure all words in the wordlist have length N
    filtered_wordlist = [word for word in wordlist if len(word) == N]

    if not filtered_wordlist:
        print("No words of the required length found in the wordlist.")
        return None

    # Start filling the grid
    grid = []
    filled_grid = fill_grid(filtered_wordlist, grid, N)

    if filled_grid:
        return filled_grid
    else:
        print("Could not create a valid grid with the given wordlist.")
        return None

# Sample usage
# wordlist = ["cat", "dog", "bat", "hat", "fat", "rat", "mat", "sat", "pat", "bar", "tar"]

FILENAME="words_alpha_2.txt"
N = 5

with open(FILENAME, "r") as file:
    wordlist = [word.strip().lower() for word in file \
            if len(word.strip()) == N and \
            word.strip().isalpha()]



grid = create_grid(wordlist, N)
if grid:
    for row in grid:
        print(row)

