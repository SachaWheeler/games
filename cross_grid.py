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

NO_MATCHES = set()
MATCHES = set()
def regex_exists(word_list, start_char, end_char):
    pair = f"{start_char}{end_char}"
    spaces = LENGTH - (len(start_char) + len(end_char))
    if pair in NO_MATCHES:
        return False
    elif pair in MATCHES:
        return True

    # pattern = f"^{start_char}.*{end_char}$"
    pattern = f"^{start_char}" + "".join(["." for _ in range(spaces)]) + f"{end_char}$"
    regex = re.compile(pattern)

    matches = any(regex.search(word) for word in word_list)
    if not matches:
        print("-", pair)
        NO_MATCHES.add(pair)
    else:
        MATCHES.add(pair)
        print("+", pair)
    print(f"{pair=}, {pattern=}, {matches=} {spaces=}")

    return matches

def create_word_grid(first_row, middle_row, last_row):
    all_words = set(list(first_row) + list(middle_row) + list(last_row))

    for first, last in itertools.product(first_row, last_row):
        if first.strip() != last.strip():
            no_match = False
            for i in range(1, LENGTH - 1):
                if not regex_exists(middle_row, first[i], last[i]):
                    no_match = True
                    break

            if no_match: # no column words match the first and last rows
                continue

            """
            for middle in itertools.permutations(middle_row, LENGTH - 2):
                # print(" ", middle)
                grid = [first] +  list(middle) + [last]
                columns = ["".join(row[i] for row in grid)
                        for i in range(LENGTH)]

                # no common elements and columns are legitimate words
                if not set(grid).intersection(columns) and \
                        all(col in all_words for col in columns):
                    return grid
            """
            grid = [first] + ["".join(["-" for _ in range(LENGTH)])
                    for x in range(LENGTH -2)] + [last]
            cols = []
            print(grid)
            for row in range(1, LENGTH - 1):
                print(row)
                for middle_word in middle_row:
                    no_match = False
                    if middle_word not in grid and middle_word not in cols:
                        grid[row] = middle_word
                        cols = ["".join(r[i] for r in grid) for i in range(LENGTH)]

                        for col in cols:
                            print(f"testing {col[:row+1]=} {col[-1]=}")
                            if not regex_exists(all_words, col[:row+1], col[-1]):
                                # skip word
                                no_match = True
                                break
                        if no_match: # skip to next word
                            continue
                        break  # skip to next row

                print(row, cols)
            return grid


    return None

def out(output, message):
    print(message)
    output.write(message + "\n")

def display_grid(grid, execution_time):
    if grid:
        with open('output.txt', 'a') as output:

            out(output, f"----------------\n"
            f"{LENGTH}x{LENGTH} Grid of words in {execution_time:.2f}s:\n"
            f"{FILENAME}\n")

            for row in grid:
                out(output, " ".join(row))
            out(output, "\nColumns:\n")
            for i in range(LENGTH):
                out(output, " ".join(row[i] for row in grid))
            out(output, "\n")
    else:
        print("No valid grid found.")


if __name__ == "__main__":
    start_time = time.time()

    first, middle, last = get_word_list()
    grid = create_word_grid(first, middle, last)

    end_time = time.time()

    execution_time = end_time - start_time

    display_grid(grid, execution_time)

