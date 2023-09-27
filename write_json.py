import spacy
import json
from reverb_algo import extract_triples
import requests
from bs4 import BeautifulSoup
from extract_predicate_and_oie_result import oie_dict

nlp = spacy.load("en_core_web_sm")


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
        # Find the last noun's index
        index_of_noun = tokens.index(predicate.split()[-1])
        tokens = tokens[:index_of_noun + 1]

    if valid:
        cleaned_predicate = ' '.join(tokens)
        return cleaned_predicate


def extract_authors_and_title(pubmed_link):
    try:
        response = requests.get(pubmed_link)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        author_div = soup.find('div', class_='inline-authors')
        title_element = soup.find('h1', class_='heading-title')

        if author_div:
            authors = [author.get_text(strip=True)
                       for author in author_div.find_all('a')]
            # Remove elements that are numbers
            authors = [author for author in authors if not author.isdigit()]
        else:
            authors = None

        if title_element:
            article_title = title_element.get_text(strip=True)
        else:
            article_title = None

        return authors, article_title

    except Exception as e:
        print(f"Error: {e}")
        return None, None


def get_author_and_article_from_json():
    with open('Result/triples_with_link_final_version.json', 'r') as json_file:
        data = json.load(json_file)
    article_author_dict = dict()
    for entry in data:
        author = entry["author list"]
        article = entry["article"]
        link = entry["id"]
        article_author_dict[link] = [author, article]
    return article_author_dict


def generate_author_replacements(authors, triple):
    phrases_to_replace = ["The author", "The authors",
                          "the author", "the authors", "The Author", "The Authors", "We"]
    new_triples = []
    subject, predicate, object_ = triple
    for r in phrases_to_replace:
        if r in subject:
            for author in authors:
                new_subject = subject.replace(r, author, 1)
                new_triple = (new_subject, predicate, object_)
                new_triples.append(new_triple)
            return new_triples
    return [triple]


def contains_named_entity(noun_phrase):
    doc = nlp(noun_phrase)

    if doc.ents:
        return True
    return False


with open('openie_with_entities/v3/oie_output_v3.txt.conj', 'r', encoding="utf8") as file:
    lines = file.readlines()


# Initialize a list to store the extracted data
data_list = []
link = ''
triples_dict_dict = dict()
author_list = []
article = ''
original_sentence = ''
count = 0
article_author_dict = get_author_and_article_from_json()

# Iterate through each chunk
for line in lines:
    if count % 2000 == 0:
        print(count)
    count += 1
    if line.startswith('I use '):
        original = True
        cache_triples = set()
        data = {
            "id": link,
            "extraction": triples_dict_dict,
            "author list": author_list,
            "article": article
        }
        data_list.append(data)

        link = line[6:-1]
        if link in oie_dict:
            triples_dict_dict = oie_dict[link]
        else:
            triples_dict_dict = dict()
        if link in article_author_dict.keys():
            author_list, article = article_author_dict[link]

    else:
        sentence = line.strip()
        if sentence:
            if original:
                if cache_triples:
                    if original_sentence not in triples_dict_dict:
                        triples_dict_dict[original_sentence] = cache_triples
                    else:
                        triples_dict_dict[original_sentence] += cache_triples
                original_sentence = sentence
                cache_triples = []
                original = False
            my_triples = extract_triples(nlp(sentence))
            for t in my_triples:
                for new_triple in generate_author_replacements(author_list, t):
                    if new_triple not in cache_triples and contains_named_entity(new_triple[0]) and contains_named_entity(new_triple[2]):
                        cache_triples.append(new_triple)
        else:
            original = True

data_list.pop(0)

# Write the extracted data to a JSON file
with open('triples_final_version.json', 'w') as json_file:
    json.dump(data_list, json_file, indent=4)
