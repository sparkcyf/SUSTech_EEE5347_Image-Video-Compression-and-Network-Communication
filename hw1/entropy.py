# Fan Qingyuan 12232509

import math

# read the text file by providing the path
def read_file(filename):
    with open(filename, 'r') as file:
        text = file.read()
    return text

# construct a dictionary with the characters as keys and the number of occurrences as values
def construct_dict(text):
    char_dict = {}
    # iterate through the text and add the characters to the dictionary
    for c in text:
        if c in char_dict:
            char_dict[c] += 1
        else:
            char_dict[c] = 1
    return char_dict

# calculate the entropy of the text from the dictionary
def calc_entropy(dict):
    # calculate the total number of characters
    total = 0
    for c in dict:
        total += dict[c]
    # calculate the entropy
    entropy = 0
    for c in dict:
        p = dict[c] / total
        entropy -= p * math.log(p, 2)
    return entropy

if __name__ == '__main__':
    filename = input("Enter the filename: ")
    text = read_file(filename)
    # text = read_file('input.txt')
    text_dict = construct_dict(text)
    print("The entropy is: " + str(calc_entropy(text_dict)))


