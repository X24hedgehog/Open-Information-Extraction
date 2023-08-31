import json
import os
import requests
from bs4 import BeautifulSoup

directory = ['data/RTP/PDF/json_extract_05_11_2022', 'data/TAP/PDF/json_extract_05_11_2022']
key2file = {'CoiStatement': "CoiStatement.txt", 'Funding': "Funding.txt", 'Acknowledgement': "Acknowledgement.txt"}
res = []


def get_authors_from_pubmed_link(pubmed_link):
    try:
        response = requests.get(pubmed_link)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        author_div = soup.find('div', class_='inline-authors')

        if author_div:
            authors = [author.get_text(strip=True) for author in author_div.find_all('a')]
            authors = [author for author in authors if not author.isdigit()]
            return authors
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def replace_author_phrases_with_names(content, authors):
    phrases_to_replace = ["The author", "The authors", "the author", "the authors", "The Author", "The Authors"]
    author_list = ', '.join(authors)
    for phrase in phrases_to_replace:
        content = content.replace(phrase, author_list)

    return content


def generate_author_replacements(authors, triple):
    phrases_to_replace = ["The author", "The authors", "the author", "the authors", "The Author", "The Authors"]
    new_triples = []

    subject, predicate, object_ = triple

    for author in authors:
        for phrase in phrases_to_replace:
            new_subject = subject.replace(phrase, author, 1)
            new_triple = (new_subject, predicate, object_)
            new_triples.append(new_triple)

    return new_triples


def extract(direct, file):
    # This function takes a directory and a file as input and write the extractions to the 3 files created

    path = os.path.join(direct, file)
    file_name = open(path, 'r')
    data = json.load(file_name)

    for dic in data:
        for (k, v) in dic.items():
            # dic is a dictionary, we only use the pair with key "content" for actual contents and PDF_pmid_URI for links to paper

            if k == "PDF_pmid_URI":
                current_link = v
                f1 = open("Statement_with_link.txt", "a")
                f1.write(current_link + ' ')
                f1.close()

            if k == 'content':
                assert isinstance(v, dict)

                for (k1, v1) in v.items():
                    if k1 in ['CoiStatement', 'Funding', 'Acknowledgement']:
                        # current_file = key2file[k1]
                        f1 = open("Statement_with_link.txt", "a")
                        f1.write(v1 + '\n')
                        f1.close()


for d in directory:
    for f in os.listdir(d):
        extract(d, f)

