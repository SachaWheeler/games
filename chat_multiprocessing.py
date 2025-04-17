import multiprocessing as mp
from collections import defaultdict


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
        prefix = "".join(square[i][col] for i in range(row + 1))
        if prefix not in prefix_dict:
            return False
    return True


def build_square(start_word, word_list, prefix_dict, N):
    squares = []

    def backtrack(square, used_words):
        if len(square) == N:
            squares.append(square[:])
            return

        prefix = "".join([row[len(square)] for row in square])
        for candidate in prefix_dict.get(prefix, []):
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
    N = 8  # or any size you want
    # with open('./words_alpha.txt') as f:
    with open("/usr/share/dict/words") as f:
        words = [line.strip() for line in f]

    squares = find_word_squares(words, N)

    for square in squares:
        print("\n".join(square))
        print("---")
