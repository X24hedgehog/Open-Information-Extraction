import spacy
nlp = spacy.load('en_core_web_sm')
V_list = ['AUX', 'VERB']
W_list = ['NOUN', 'PRON', 'DET', 'ADJ', 'ADV']
P_list = ['ADP', 'PART']


def find_predicate(i, cache):
    current_sentence = ""
    verb_found = False
    start = i
    while i < len(cache) and not verb_found:
        if cache[i].pos_ in V_list:
            start = i
            current_sentence += cache[i].text_with_ws
            verb_found = True
            if cache[i].pos_ == 'AUX' and cache[i+1].pos_ == 'VERB':
                current_sentence += cache[i+1].text_with_ws
                i += 1
        i += 1
    verb_part = current_sentence

    w_start = i
    while i < len(cache) and cache[i].pos_ in W_list:
        current_sentence += cache[i].text_with_ws
        i += 1

    if i < len(cache) and cache[i].pos_ in P_list:
        current_sentence += cache[i].text_with_ws
        i += 1
        return current_sentence, start, i

    return verb_part, start, w_start


def extract_predicate(doc):
    output = []
    cache = [t for t in doc]
    t = 0
    while t < len(cache):
        extracted_predicate, start, end = find_predicate(t, cache)
        t = end
        if extracted_predicate != '':
            output.append((extracted_predicate, start, end))

    return output


def extract_noun(doc):
    # print([(token.text_with_ws, token.pos_) for token in doc])
    return [(chunk.text, chunk.start, chunk.end) for chunk in doc.noun_chunks]


def extract_triples(doc):
    nouns = extract_noun(doc)
    predicates = extract_predicate(doc)
    triples = []
    last_object_index = -1
    for predicate in predicates:
        start, end = predicate[1], predicate[2]
        i = 0
        # print(f'start: {start}, end: {end}')
        while i < len(nouns) and nouns[i][2] <= start:
            i += 1
        if i == len(nouns) or nouns[i][2] > start:
            i -= 1

        j = len(nouns) - 1
        while j > -1 and nouns[j][1] >= end:
            j -= 1
        if j == -1 or nouns[j][1] < end:
            j += 1

        # if i == last_object_index and triples:
        #     triples.pop()

        if 0 <= i < len(nouns) and 0 <= j < len(nouns):
            triples.append((nouns[i][0], predicate[0], nouns[j][0]))
        last_object_index = j

    return triples


test_sentence = "Drs. Doxey, Eberini, Jungo, Kough, Palazzolo, Pereira Mouries and Rodriguez have no conflict of interests to declare ."
doc = nlp(test_sentence)
# print(f'Predicates: {extract_predicate(doc)}')
# print(f'Noun: {extract_noun(doc)}')
# print(extract_triples(doc))
