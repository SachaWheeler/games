import nltk
from nltk.corpus import stopwords
import random

def generate_grid(x):
    # Create a list of all the words in the dictionary
    word_list = []
    for i in range(x):
        for j in range(x):
            word = chr(ord('A') + i) + chr(ord('A') + j)
            if not word in stopwords.words():
                word_list.append(word)

    # Shuffle the list of words to ensure randomness
    random.shuffle(word_list)

    # Create a grid with the specified number of rows and columns
    grid = []
    for i in range(x):
        row = []
        for j in range(x):
            row.append(word_list[j])
        grid.append(row)

    return grid

grid = generate_grid(5)
print(grid)

