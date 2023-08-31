import xml.etree.ElementTree as ET
import os

directory = ['data/RTP/XML/clean_split_data_05_11_2022_1993_01_01_2022_12_31', 'data/TAP/XML/clean_split_data_05_11_2022_1993_01_01_2022_12_30']
key2file = {'CoiStatement': "CoiStatement1.txt", 'Funding': "Funding1.txt", 'Acknowledgement': "Acknowledgement1.txt"}


def extract(direct, file):
    # This function takes a directory and a file as input and write the extractions to the 3 files created

    path = os.path.join(direct, file)
    tree = ET.parse(path)
    root = tree.getroot()
    # Load the xml file to a python object

    for (k, v) in key2file.items():
        c = root.iter(k)
        f1 = open(v, 'a')
        for tag in c:
            f1.write(tag.text + '\n')


for d in directory:
    for f in os.listdir(d):
        extract(d, f)

