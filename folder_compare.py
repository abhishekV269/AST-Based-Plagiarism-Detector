import os
from Parser import extract_node_sequence
from Similarity import sequence_similarity


def read_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def compare_folder(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith(".py")]

    sequences = {}

    # Extract AST sequences for all files
    for file in files:
        path = os.path.join(folder_path, file)
        code = read_file(path)
        sequences[file] = extract_node_sequence(code)

    matrix = {}

    for file1 in files:
        matrix[file1] = {}
        for file2 in files:
            if file1 == file2:
                matrix[file1][file2] = 100.0
            else:
                score = sequence_similarity(
                    sequences[file1],
                    sequences[file2]
                )
                matrix[file1][file2] = score

    return files, matrix


if __name__ == "__main__":
    folder = "submissions"
    files, matrix = compare_folder(folder)

    print("\n==============================")
    print("      SIMILARITY MATRIX")
    print("==============================\n")

    # Header row
    print(" " * 15, end="")
    for file in files:
        print(f"{file[:10]:>12}", end="")
    print()

    # Matrix rows
    for file1 in files:
        print(f"{file1[:12]:<15}", end="")
        for file2 in files:
            print(f"{matrix[file1][file2]:>12.2f}", end="")
        print()

    # Threshold filtering
    THRESHOLD = 75

    print("\n==============================")
    print("  SUSPICIOUS PAIRS (≥75%)")
    print("==============================\n")

    visited = set()

    suspicious_pairs = []

    for file1 in files:
        for file2 in files:
            if file1 != file2 and (file2, file1) not in visited:
                score = matrix[file1][file2]
                if score >= THRESHOLD:
                    print(f"{file1}  vs  {file2}  →  {score:.2f}%")
                    suspicious_pairs.append((file1, file2, score))
                visited.add((file1, file2))

    # Generate report file
    with open("report.txt", "w", encoding="utf-8") as report:
        report.write("CODE SIMILARITY ANALYSIS REPORT\n")
        report.write("=" * 40 + "\n\n")

        report.write("SIMILARITY MATRIX\n")
        report.write("-" * 40 + "\n\n")

        # Header row
        report.write(" " * 15)
        for file in files:
            report.write(f"{file[:10]:>12}")
        report.write("\n")

        # Matrix rows
        for file1 in files:
            report.write(f"{file1[:12]:<15}")
            for file2 in files:
                report.write(f"{matrix[file1][file2]:>12.2f}")
            report.write("\n")

        report.write("\n")
        report.write("SUSPICIOUS PAIRS (≥75%)\n")
        report.write("-" * 40 + "\n\n")

        for file1, file2, score in suspicious_pairs:
            report.write(f"{file1} vs {file2} → {score:.2f}%\n")

    print("\nReport saved as report.txt")