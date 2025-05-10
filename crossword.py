import copy
from collections import defaultdict
import nltk
import os

# Ensure NLTK words are available
try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

from nltk.corpus import words as nltk_words

# --------------------------
# Load and index word list
# --------------------------
def load_word_list(file_path=None):
    if file_path and os.path.isfile(file_path):
        with open(file_path, encoding="utf-8", errors="ignore") as f:
            raw_words = [line.strip().lower() for line in f if line.strip().isalpha()]
    else:
        raw_words = [w.lower() for w in nltk_words.words() if w.isalpha()]

    word_dict = defaultdict(list)
    for w in raw_words:
        word_dict[len(w)].append(w)
    return word_dict

# --------------------------
# Identify word slots
# --------------------------
def find_word_slots(grid):
    rows, cols = len(grid), len(grid[0])
    slots = []

    # Horizontal (across)
    for r in range(rows):
        c = 0
        while c < cols:
            if grid[r][c] == " ":
                start = c
                while c < cols and grid[r][c] == " ":
                    c += 1
                if c - start > 1:
                    slots.append({"dir": "across", "row": r, "col": start, "length": c - start})
            else:
                c += 1

    # Vertical (down)
    for c in range(cols):
        r = 0
        while r < rows:
            if grid[r][c] == " ":
                start = r
                while r < rows and grid[r][c] == " ":
                    r += 1
                if r - start > 1:
                    slots.append({"dir": "down", "row": start, "col": c, "length": r - start})
            else:
                r += 1

    return slots

# --------------------------
# Grid manipulation helpers
# --------------------------
def can_place(word, slot, grid):
    r, c = slot['row'], slot['col']
    for i in range(len(word)):
        if slot['dir'] == 'across':
            cell = grid[r][c + i]
            if cell != " " and cell != word[i]:
                return False
        else:
            cell = grid[r + i][c]
            if cell != " " and cell != word[i]:
                return False
    return True

def place_word(word, slot, grid):
    r, c = slot['row'], slot['col']
    for i in range(len(word)):
        if slot['dir'] == 'across':
            grid[r][c + i] = word[i]
        else:
            grid[r + i][c] = word[i]

def remove_word(word, slot, grid, original_grid):
    r, c = slot['row'], slot['col']
    for i in range(len(word)):
        if slot['dir'] == 'across':
            grid[r][c + i] = original_grid[r][c + i]
        else:
            grid[r + i][c] = original_grid[r + i][c]

# --------------------------
# Recursive solver
# --------------------------
def solve_all(grid, word_dict, slots, index=0, used_words=None, original_grid=None, solutions=None):
    if used_words is None:
        used_words = set()
    if solutions is None:
        solutions = []

    if index == len(slots):
        solutions.append(copy.deepcopy(grid))
        return

    slot = slots[index]
    candidates = word_dict.get(slot['length'], [])

    for word in candidates:
        if word in used_words:
            continue
        if can_place(word, slot, grid):
            snapshot = copy.deepcopy(grid)
            place_word(word, slot, grid)
            used_words.add(word)

            solve_all(grid, word_dict, slots, index + 1, used_words, snapshot, solutions)

            remove_word(word, slot, grid, snapshot)
            used_words.remove(word)

# --------------------------
# Output helpers
# --------------------------
def print_grid(grid):
    return "\n".join("".join(row) for row in grid)

def write_solutions_to_file(solutions, filename="solutions.txt"):
    with open(filename, "w") as f:
        for i, grid in enumerate(solutions, 1):
            f.write(f"Solution #{i}\n")
            f.write(print_grid(grid))
            f.write("\n" + "-" * 20 + "\n")
    print(f"✅ {len(solutions)} solution(s) written to {filename}")

# --------------------------
# Entry point
# --------------------------
import argparse

def main():
    parser = argparse.ArgumentParser(description="Crossword grid solver")
    parser.add_argument("--file", "-f", type=str, help="Path to word list file")
    parser.add_argument("--output", "-o", type=str, default="solutions.txt", help="Output file for solutions")
    args = parser.parse_args()

    grid = [
        [" ", " ", " ", " "],
        [" ", " ", " ", " "],
        [" ", " ", " ", " "],
    ]

    word_dict = load_word_list(args.file)
    slots = find_word_slots(grid)
    original = copy.deepcopy(grid)
    solutions = []
    solve_all(grid, word_dict, slots, original_grid=original, solutions=solutions)

    if solutions:
        write_solutions_to_file(solutions, filename=args.output)
    else:
        print("❌ No solutions found.")


if __name__ == "__main__":
    main()

