# import re
#

def extract_strings(input_file, output_file):
    # pattern = r'^(\d+\.\d+\.\d+):\s+\((?:[^;]*;){1}([^;]*);(?:[^;]*;){1}[^;]*\)$'

    with open(input_file, 'r') as file:
        lines = file.readlines()

    extracted_strings = []
    for line in lines:
        if len(line) >= 5 and line[4] == ":":
            predicate = line.split("; ")[1]
            extracted_strings.append(predicate)
        # match = re.match(pattern, line)
        # if match:
        #     extracted_strings.append(match.group(2))

    with open(output_file, 'w') as file:
        for string in extracted_strings:
            file.write(string + '\n')

    print(f"Extracted {len(extracted_strings)} predicates and saved them to {output_file}")


# Usage example
input_file_path = 'openie_with_entities/output.txt.oie'
output_file_path = 'extract_predicate.txt'
extract_strings(input_file_path, output_file_path)
