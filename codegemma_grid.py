import nltk
from nltk.corpus import words
from nltk.corpus import stopwords

# Set the size of the grid
x = int(input("Enter the size of the grid: "))

# Load the list of valid English words
word_list = words.words()

# Remove stopwords
stop_words = set(stopwords.words('english'))
word_list = [word for word in word_list if word not in stop_words]

# Filter words to be the same length as the grid size
grid_words = [word for word in word_list if len(word) == x]

# Generate a list of possible first words for each row
row_words = [word for word in grid_words if word[0] in [letter for letter in grid_words[0]]]

# Generate a list of possible first words for each column
col_words = [word for word in grid_words if word[0] in [letter for letter in grid_words[0]]]

# Find valid grid solutions
solutions = []

def find_solutions(row, col, used_words):
    if row == x:
        solutions.append(used_words[:])
        return

    for word in row_words:
        if word not in used_words:
            if any(word[0] in word for word in col_words):
                used_words.append(word)
                find_solutions(row + 1, col, used_words)
                used_words.pop()


for word in col_words:
    find_solutions(1, 0, [word])

# Print the solutions
for solution in solutions:
    for word in solution:
        print(word, end=" ")
    print()

