import spacy
import re


def add_space_before_punctuation(input_string):
    input_string = input_string.strip()
    if input_string[-1] == '.':
        # If the period exists, add a space before it
        modified_string = input_string[:-1] + ' .'
    else:
        # If the period doesn't exist, add space and a period at the end
        modified_string = input_string + '.'
    modified_sentence = re.sub(r',\s*([A-Z])', r' , \1', modified_string)
    return modified_sentence


def split_sentences_with_pos(doc):
    sentence_beginning_tag = ["NOUN", "PRON", "DET", "PROPN", "INTJ", "ADP", "SCONJ"]
    sentences = []
    current_sentence = ""
    token_cache = []
    verb_existence = False
    for token in doc:
        token_cache.append([token, token.pos_])
    for i in range(len(token_cache)):
        token, pos = token_cache[i][0], token_cache[i][1]
        # print(token, pos)
        current_sentence += token.text_with_ws
        if pos in ["VERB", "AUX"]:
            verb_existence = True

        if i == len(token_cache)-1 or (verb_existence and token.pos_ == "PUNCT" and token.text == "." and i < len(token_cache) and token_cache[i+1][1] in sentence_beginning_tag):
            sentences.append(current_sentence.strip())
            current_sentence = ""
            verb_existence = False

    if current_sentence:
        sentences.append(current_sentence.strip())
    return sentences


def split_sentences(input_file, output_file):
    nlp = spacy.load('en_core_web_sm')
    sentences = []
    replacement = ["Declaration of Competing Interest ", "Declaration of competing interest ",
                   "The authors declare that ", "the author declares that ", "Conflict of interest statement", "Acknowledgements References"
                   "The authors declare the following financial interests/personal relationships which may be considered as potential competing interests:"]

    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('https:'):
                line_content = line.strip().split(" ", 1)
                link, sentence_content = line_content[0], line_content[1]
                sentences.append('I use ' + link + '.')
            else:
                sentence_content = line
            for r in replacement:
                sentence_content = sentence_content.replace(r, "")
            doc = nlp(sentence_content)
            collected_sentences = split_sentences_with_pos(doc)
            processed_sentences = [add_space_before_punctuation(sent) for sent in collected_sentences]
            sentences += processed_sentences


    with open(output_file, 'w') as out_file:
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence.startswith('I use'):
                if not sentence[0].isupper():
                    sentence = sentence[0].capitalize() + sentence[1:]
                if not sentence.endswith("."):
                    sentence = sentence + " ."
            out_file.write(sentence + "\n")


if __name__ == "__main__":
    input_file_path = "Statement_with_link.txt"  # Replace with the path to your input file
    output_file_path = "oie_input_3.txt"  # Replace with the desired output file path
    split_sentences(input_file_path, output_file_path)
