import spacy
import string


def add_space_before_punctuation(sentence):
    for punctuation_mark in string.punctuation:
        sentence = sentence.replace(punctuation_mark, f" {punctuation_mark}")
    return sentence


def split_sentences_with_ner(doc):
    sentences = []
    current_sentence = ""

    for token in doc:
        current_sentence += token.text_with_ws

        # Check if the token is a sentence-ending punctuation and not part of a named entity
        if token.is_sent_end and token.ent_iob == 0:
            sentences.append(current_sentence.strip())
            current_sentence = ""

    if current_sentence:
        sentences.append(current_sentence.strip())

    return sentences


def process_sentences(input_file, output_file):
    nlp = spacy.load('en_core_web_sm')
    replacement = ["Declaration of Competing Interest ", "Declaration of competing interest ", "The authors declare that ", "The authors declare the following financial interests/personal relationships which may be considered as potential competing interests:"]
    with open(input_file, 'r', encoding='utf-8') as input_file:
        with open(output_file, 'a', encoding='utf-8') as output_file:
            for line in input_file:
                for r in replacement:
                    line = line.replace(r, "")
                # print(f'After: {line}')
                if line:
                    line = line.strip().capitalize()
                    doc = nlp(line)
                    sentences = split_sentences_with_ner(doc)
                    processed_sentences = [add_space_before_punctuation(sent) for sent in sentences]
                    output_file.write("\n".join(processed_sentences) + "\n")


if __name__ == "__main__":
    input_file_path = "CoiStatement1.txt.txt"  # Replace with the path to your input file
    output_file_path = "oie_input.txt"  # Replace with the desired output file path
    process_sentences(input_file_path, output_file_path)
