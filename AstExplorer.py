import ast
from collections import Counter
import math

def extract_node_sequence(code):
    tree = ast.parse(code)
    sequence = []

    def dfs(node):
        node_type = type(node).__name__

        ignore_nodes = {"Load", "Store", "Expr", "Module"}

        if node_type not in ignore_nodes:
            sequence.append(node_type)

        for child in ast.iter_child_nodes(node):
            dfs(child)

    dfs(tree)
    return sequence

import difflib

def sequence_similarity(seq1, seq2):
    matcher = difflib.SequenceMatcher(None, seq1, seq2)
    return matcher.ratio() * 100

    # Create vectors
    vec1 = [counter1.get(node, 0) for node in all_nodes]
    vec2 = [counter2.get(node, 0) for node in all_nodes]

    # Dot product
    dot_product = sum(a*b for a, b in zip(vec1, vec2))

    # Magnitudes
    mag1 = math.sqrt(sum(a*a for a in vec1))
    mag2 = math.sqrt(sum(b*b for b in vec2))

    if mag1 == 0 or mag2 == 0:
        return 0

    return (dot_product / (mag1 * mag2)) * 100


code1 = """
x = 15
y = 20
print(x + y)
"""

code2 = """
for i in range(5):
    print(i)
"""

nodes1 = extract_node_sequence(code1)
nodes2 = extract_node_sequence(code2)

counter1 = Counter(nodes1)
counter2 = Counter(nodes2)

score = sequence_similarity(nodes1, nodes2)

print("Similarity Score: {:.2f}%".format(score))