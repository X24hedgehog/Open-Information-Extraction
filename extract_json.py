import json
import os

print(5)
directory = ['data/RTP/PDF/json_extract_05_11_2022', 'data/TAP/PDF/json_extract_05_11_2022']
key2file = {'CoiStatement': "CoiStatement.txt", 'Funding': "Funding.txt", 'Acknowledgement': "Acknowledgement.txt"}
res = []


def extract(direct, file):
    # This function takes a directory and a file as input and write the extractions to the 3 files created

    path = os.path.join(direct, file)
    file_name = open(path, 'r')
    data = json.load(file_name)
    # Load the json object to a python object, data is a list of dictionaries

    for dic in data:
        for (k, v) in dic.items():
            # dic is a dictionary, we only use the pair with key "content"

            if k == 'content':
                assert isinstance(v, dict)

                for (k1, v1) in v.items():
                    if k1 in ['CoiStatement', 'Funding', 'Acknowledgement']:
                        current_file = key2file[k1]
                        f1 = open(current_file, "a")
                        f1.write(v1 + '\n')
                        f1.close()
                        res.append(v1)


for d in directory:
    for f in os.listdir(d):
        extract(d, f)


# print(res)

f1 = open("CoiStatement1.txt", "w")
f1.write("Leo is the best." + '\n')
f1.close()
