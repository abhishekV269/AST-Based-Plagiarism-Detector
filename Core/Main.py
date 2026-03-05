from Parser import extract_node_sequence
from Similarity import sequence_similarity


def read_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


file1 = "sample1.py"
file2 = "sample2.py"

code1 = read_file(file1)
code2 = read_file(file2)

nodes1 = extract_node_sequence(code1)
nodes2 = extract_node_sequence(code2)

score = sequence_similarity(nodes1, nodes2)

print(f"Comparing {file1} and {file2}")
print("Similarity Score: {:.2f}%".format(score))