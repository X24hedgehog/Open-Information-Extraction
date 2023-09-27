import spacy
import json
nlp = spacy.load("en_core_web_sm")


def add_oie_result():
    def is_valid_predicate(predicate):
        predicate = predicate.strip()
        valid = False
        doc = nlp(predicate)
        tokens = []
        for token in doc:
            if token.pos_ == 'VERB' or token.pos_ == 'AUX':
                valid = True
            if valid:
                tokens.append(token.text)
                if token.pos_ == 'NOUN':
                    tokens.pop(-1)
                    break

        if valid:
            cleaned_predicate = ' '.join(tokens)
            return cleaned_predicate

    with open('openie_with_entities/v3/oie_output_3.txt', 'r', encoding="utf8") as file:
        lines = file.readlines()

    # Initialize a list to store the extracted data
    link = ''
    cache_triples_dict = {}
    cache_triples = []
    cache = dict()
    original_sentence = ''
    original = True
    count = 0

    # print(lines)
    # Iterate through each chunk
    for line in lines:
        if count % 2000 == 0:
            print(count)
        count += 1
        if line.startswith('I use '):
            cache[link] = cache_triples_dict
            cache_triples_dict = dict()
            link = line[6:-1]
        else:
            sentence = line.strip()
            if sentence and not sentence[0].isnumeric() and original:
                if cache_triples:
                    cache_triples_dict[original_sentence] = cache_triples
                original_sentence = sentence
                cache_triples = []
            elif sentence and len(sentence) >= 8 and sentence[4] == ":":
                l = line.split('; ')
                if len(l) == 3:
                    subject, predicate, object = l[0][7:].strip(
                    ), l[1].strip(), l[2].strip()
                    filtered_predicate = is_valid_predicate(predicate)
                    subject_doc, object_doc = nlp(subject), nlp(object)
                    subject_ent, object_ent = subject_doc.ents, object_doc.ents
                    # print(f'Subject: {subject}, Predicate: {predicate}, Object: {object}, Subject entity: {subject_ent}, Object entity: {object_ent}')
                    if subject_ent and object_ent and filtered_predicate:
                        for ent in subject_doc.ents:
                            sub_entity = ent.text
                            break
                        for ent in object_doc.ents:
                            obj_entity = ent.text
                            break
                        new_triple = (
                            sub_entity, filtered_predicate, obj_entity)
                        # print(f'Triple: {new_triple}')
                        if new_triple not in cache_triples:
                            cache_triples.append(new_triple)

    print('oie dict extracted!!!!!!!!!!!!!!!!!')
    print('oie dict extracted!!!!!!!!!!!!!!!!!')
    print('oie dict extracted!!!!!!!!!!!!!!!!!')
    print('oie dict extracted!!!!!!!!!!!!!!!!!')
    print('oie dict extracted!!!!!!!!!!!!!!!!!')
    print('oie dict extracted!!!!!!!!!!!!!!!!!')
    return cache


oie_dict = add_oie_result()
# filtered_predicates_updated = []

# # Load the JSON file
# with open('triples_with_link_2.json', 'r') as json_file:
#     data = json.load(json_file)

# keys = set(oie_dict.keys())
# for entry in data:
#     entry_id = entry["id"]
#     if entry_id in keys:
#         for triple in oie_dict[entry_id]:
#             triple_list = [triple[0], triple[1], triple[2]]
#             if triple_list not in entry['extraction']:
#                 entry['extraction'].append(triple_list)
#         for tri in entry['extraction']:
#             filtered_predicates_updated.append(tri[1])

# with open('triples_with_link_v3.json', 'w') as updated_json_file:
#     json.dump(data, updated_json_file, indent=4)

# # with open('filtered_predicates_updated.txt', 'w') as file:
# #     for predicate in filtered_predicates_updated:
# #         file.write(predicate + '\n')
