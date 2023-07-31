import spacy

# Load the English language model
nlp = spacy.load('en_core_web_sm')

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


test_sentence = "L.Messi, C.Ronaldo, Neymar.J are the best. They have fantastic skills. D.Maradona and V.Basten . really like them."
doc = nlp(test_sentence)
for token in doc:
    print(f'{token} : {token.pos_}')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
