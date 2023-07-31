import spacy
import re

# Load the English language model
nlp = spacy.load('en_core_web_sm')

# Read the text file and extract the predicates
predicates = []
with open('extract_predicate.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            cleaned_line = re.sub(r'^/\d+\s*', '', line)
            predicates.extend(cleaned_line.split('.'))


# Function to check if a predicate contains at least one verb and doesn't contain numbers or slashes
def is_valid_predicate(predicate):
    predicate = predicate.strip()
    valid = False
    doc = nlp(predicate)
    tokens = []
    found_noun = False
    for token in doc:
        if token.pos_ == 'VERB' or token.pos_ == 'AUX':
            valid = True
        if valid:
            tokens.append(token.text)
            if token.pos_ == 'NOUN':
                found_noun = True

    if found_noun:
        index_of_noun = tokens.index(predicate.split()[-1])  # Find the last noun's index
        tokens = tokens[:index_of_noun + 1]

    if valid:
        cleaned_predicate = ' '.join(tokens)
        return cleaned_predicate


# Filter the predicates to include only those with verbs and without numbers or slashes
filtered_predicates = list(set([is_valid_predicate(predicate) for predicate in predicates if is_valid_predicate(predicate)]))

# Write the filtered predicates to a new file
with open('filtered_predicates.txt', 'w') as file:
    for predicate in filtered_predicates:
        file.write(predicate + '\n')
