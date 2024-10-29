#!/usr/bin/env python
import random
import nltk
# from nltk.corpus import words
import itertools
import re
import time


# nltk.download('words')
LENGTH = 5
FILENAME="words_alpha_2.txt"

def get_word_list(filename=FILENAME):
    with open(filename, "r") as file:
        words = [word.strip().lower() for word in file \
                if len(word.strip()) in [LENGTH, LENGTH - 1] and \
                word.strip().isalpha()]

        print(len(words))

        first  = {word + " " for word in words if len(word) == LENGTH - 1}
        middle = {word for word in words if len(word) == LENGTH}
        last   = {" " + word for word in words if len(word) == LENGTH - 1}

    return first, middle, last

def regex_exists_in_list(word_list, start_char, end_char):
    pattern = f"^{start_char}.*{end_char}$"
    regex = re.compile(pattern)

    return any(regex.search(word) for word in word_list)

def create_word_grid(first_row, middle_row, last_row):
    all_words = set(list(first_row) + list(middle_row) + list(last_row))
    count = 0

    for first, last in itertools.product(first_row, last_row):
        if first.strip() != last.strip():
            no_match = False
            for i in range(1, LENGTH - 1):
                if not regex_exists_in_list(middle_row, first[i], last[i]):
                    no_match = True
                    break
            if no_match:
                print(f"skipping {first} {last}")
                continue

            # determine if the first and last rows have any matches at all
            for middle in itertools.permutations(middle_row, LENGTH - 2):
                grid = [first] +  list(middle) + [last]
                columns = ["".join(row[i] for row in grid)
                        for i in range(LENGTH)]

                """
                if count%100000==0:
                    print(f"{count}: {grid=}")
                count += 1
                """

                # no common elements and columns are legitimate words
                if not set(grid).intersection(columns) and \
                        all(col in all_words for col in columns):
                    return grid

    return None


def display_grid(grid, execution_time):
    if grid:
        with open('output.txt', 'a') as output:

            print(f"{LENGTH}x{LENGTH} Grid of words in {execution_time:.2f}s:")
            output.write(f"----------------\n"
            f"{LENGTH}x{LENGTH} Grid of words in {execution_time:.2f}s:\n")
            output.write(f"{FILENAME}\n")

            for row in grid:
                print(" ".join(row))
                output.write(" ".join(row))
                output.write("\n")
            print("\nColumns:")
            output.write("\nColumns:\n")
            for i in range(LENGTH):
                print(" ".join(row[i] for row in grid))
                output.write(" ".join(row[i] for row in grid))
                output.write("\n")
            output.write("\n")
    else:
        print("No valid grid found.")


if __name__ == "__main__":
    start_time = time.time()

    first, middle, last = get_word_list()
    grid = create_word_grid(first, middle, last)

    end_time = time.time()

    execution_time = end_time - start_time

    display_grid(grid, execution_time)

