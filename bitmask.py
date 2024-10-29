#!/usr/bin/env python
def word_to_bitmask(word):
    bitmask = 0
    for char in word:
        bitmask |= 1 << (ord(char) - ord('a'))
    return bitmask

def prepare_bitmask_set(word_list):
    return {word_to_bitmask(word) for word in word_list}

def is_word_in_list(random_word, bitmask_set):
    random_word_bitmask = word_to_bitmask(random_word)
    return random_word_bitmask in bitmask_set

def bitmask_to_word(bitmask):
    word = []
    for i in range(26):  # For each bit position from 0 to 25
        if bitmask & (1 << i):  # Check if the bit at position i is set
            word.append(chr(i + ord('a')))  # Convert bit position to letter
    return ''.join(word)


word_list = ["apple", "banana", "cherry", "date"]
bitmask_set = prepare_bitmask_set(word_list)

random_word = "apple"
print(is_word_in_list(random_word, bitmask_set))  # Output: True

random_word = "grape"
print(is_word_in_list(random_word, bitmask_set))  # Output: False

example_bitmask = word_to_bitmask("apple")
reconstructed_word = bitmask_to_word(example_bitmask)
print(reconstructed_word)  # Output might be "aelp" (characters sorted)


