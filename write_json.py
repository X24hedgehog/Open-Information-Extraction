import spacy
import json
from reverb_algo import extract_triples
import requests
from bs4 import BeautifulSoup
from extract_predicate import oie_dict

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


def generate_author_replacements(authors, triple):
    phrases_to_replace = ["The author", "The authors",
                          "the author", "the authors", "The Author", "The Authors"]
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


with open('oie_output_v3.txt.conj', 'r') as file:
    lines = file.readlines()


# Initialize a list to store the extracted data
data_list = []
link = ''
triples = []
author_list = []
article = ''

# Iterate through each chunk
for line in lines:
    if line.startswith('I use '):
        cache_triples = set()
        data = {
            "id": link,
            "extraction": triples,
            "author list": author_list,
            "article": article
        }
        data_list.append(data)

        link = line[6:-1]
        triples = list(oie_dict[link])
        author_list, article = extract_authors_and_title(link)

    else:
        sentence = line.strip()
        if sentence:
            my_triples = extract_triples(nlp(sentence))
            for t in my_triples:
                for new_triple in generate_author_replacements(author_list, t):
                    if new_triple not in cache_triples and contains_named_entity(new_triple[0]) and contains_named_entity(new_triple[2]):
                        triples.append(new_triple)
                        cache_triples.add(new_triple)

data_list.pop(0)

# Write the extracted data to a JSON file
with open('triples_with_link_v2.json', 'w') as json_file:
    json.dump(data_list, json_file, indent=4)
