#!/usr/bin/env python
import random
import nltk
# from nltk.corpus import words
import itertools

# nltk.download('words')
WORD_LENGTH = 3
FILENAME="words_alpha_3.txt"

def get_word_list(filename=FILENAME):
    with open(filename, "r") as file:
        words = [word.strip().lower() for word in file \
                if len(word.strip()) in [WORD_LENGTH, WORD_LENGTH - 1] and \
                word.strip().isalpha()]

        print(len(words))

        first  = {word + " " for word in words if len(word) == WORD_LENGTH - 1}
        middle = {word for word in words if len(word) == WORD_LENGTH}
        last   = {" " + word for word in words if len(word) == WORD_LENGTH - 1}

    return first, middle, last

# Step 2: Create a WORD_LENGTHxWORD_LENGTH word grid
def create_word_grid(first_row, middle_row, last_row):
    all_words = set(list(first_row) + list(middle_row) + list(last_row))
    count = 0

    for first, last in itertools.product(first_row, last_row):
        if first.strip() != last.strip(): # no dupes
            for middle in itertools.permutations(middle_row, WORD_LENGTH - 2):
                grid = [first] +  list(middle) + [last]
                columns = ["".join(row[i] for row in grid) for i in range(WORD_LENGTH)]

                if count%100000==0:
                    print(f"{count}: {grid=}")
                count += 1
                # print(f"{columns=}")
                # no common elements and columns are legitimate words
                if not set(grid).intersection(columns) and \
                        all(col in all_words for col in columns):
                    return grid

    return None


def display_grid(grid):
    if grid:
        print(f"{WORD_LENGTH}x{WORD_LENGTH} Grid of words:")
        for row in grid:
            print(" ".join(row))
        print("\nColumns:")
        for i in range(WORD_LENGTH):
            print(" ".join(row[i] for row in grid))
    else:
        print("No valid grid found.")


if __name__ == "__main__":
    first, middle, last = get_word_list()
    grid = create_word_grid(first, middle, last)
    display_grid(grid)

