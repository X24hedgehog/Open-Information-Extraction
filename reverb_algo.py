import spacy
nlp = spacy.load('en_core_web_sm')
V_list = ['AUX', 'VERB']
W_list = ['NOUN', 'PRON', 'DET', 'ADJ', 'ADV']
P_list = ['INTJ', 'PART']


def find_predicate(i):
    


def reverb(sentence):
    doc = nlp(sentence)
    current_sentence = ""
    cache = []
    for t in doc:
        cache.append(t)
    i = 0
    verb_found = False
    while i < len(cache) and not verb_found:
        token = cache[i]
        if token.pos_ in V_list:
            current_sentence += token.text_with_ws
            verb_found = True
        i += 1

    while i < len(cache) and cache[i].pos_ in W_list:
        current_sentence += cache[i].text_with_ws
        i += 1

    if i < len(cache) and cache[i].pos_ in P_list:
        current_sentence += cache[i].text_with_ws

    return current_sentence


test_sentence = 'The authors are solely responsible for the content and writing of the paper .'
print(reverb(test_sentence))


def extract_predicate(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    extracted_predicates = []
    for line in lines:
        if line != '':
            predicate = reverb(line)
            extracted_predicates.append(predicate)

    extracted_predicates = list(set(extracted_predicates))

    with open(output_file, 'w') as file:
        for string in extracted_predicates:
            file.write(string + '\n')

    print(f"Extracted {len(extracted_predicates)} predicates and saved them to {output_file}")


# # Usage example
# input_file_path = 'openie_with_entities/oie_output_1.txt.conj'
# output_file_path = 'reverb_predicates.txt'
# extract_predicate(input_file_path, output_file_path)
