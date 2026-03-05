import streamlit as st
from Parser import extract_node_sequence
from Similarity import sequence_similarity
import pandas as pd
from itertools import combinations


st.set_page_config(page_title="AST Code Similarity Detector", layout="wide")

st.title(" AST-Based Python Plagiarism Detector ")
st.write("Upload multiple Python files to analyze structural similarity.")


uploaded_files = st.file_uploader(
    "Upload Python Files",
    type=["py"],
    accept_multiple_files=True
)


if uploaded_files and len(uploaded_files) >= 2:

    st.success(f"{len(uploaded_files)} files uploaded successfully.")

    sequences = {}
    filenames = []

    for file in uploaded_files:
        code = file.read().decode("utf-8")
        sequences[file.name] = extract_node_sequence(code)
        filenames.append(file.name)

    # ==============================
    # Compute Pairwise Similarity
    # ==============================
    pair_scores = []

    for file1, file2 in combinations(filenames, 2):
        score = sequence_similarity(
            sequences[file1],
            sequences[file2]
        )
        pair_scores.append((file1, file2, score))

    pair_scores.sort(key=lambda x: x[2], reverse=True)

    # ==============================
    # Top Similar Pairs (MAIN VIEW)
    # ==============================
    st.subheader("🏆 Top Similar Pairs")

    threshold = st.slider(
    "Set Suspicious Similarity Threshold (%)",
    min_value=0,
    max_value=100,
    value=75
    )

    for file1, file2, score in pair_scores[:10]:
        if score >= threshold:
            st.error(f"{file1}  vs  {file2}  →  {score:.2f}%")
        elif score >= 50:
            st.warning(f"{file1}  vs  {file2}  →  {score:.2f}%")
        else:
            st.write(f"{file1}  vs  {file2}  →  {score:.2f}%")

    # ==============================
    # Suspicious Section
    # ==============================
    st.subheader(" Suspicious Pairs (≥75%)")

    suspicious = [p for p in pair_scores if p[2] >= threshold]

    if suspicious:
        for file1, file2, score in suspicious:
            st.error(f"{file1}  vs  {file2}  →  {score:.2f}%")
    else:
        st.success("No high similarity pairs detected.")

    # ==============================
    # Collapsible Similarity Matrix
    # ==============================
    with st.expander(" Advanced View – Similarity Matrix"):

        matrix_data = []

        for file1 in filenames:
            row = []
            for file2 in filenames:
                if file1 == file2:
                    row.append(100.0)
                else:
                    score = sequence_similarity(
                        sequences[file1],
                        sequences[file2]
                    )
                    row.append(round(score, 2))
            matrix_data.append(row)

        df = pd.DataFrame(matrix_data, columns=filenames, index=filenames)
        st.dataframe(df)

    # ==============================
    # Collapsible AST Details
    # ==============================
    with st.expander(" Technical View – AST Node Details"):

        for file in filenames:
            st.markdown(f"### {file}")
            st.write("AST Node Count:", len(sequences[file]))
            
        import io

    st.subheader(" Export Report")

    csv_buffer = io.StringIO()
    csv_buffer.write("File 1,File 2,Similarity (%)\n")

    for file1, file2, score in pair_scores:
        csv_buffer.write(f"{file1},{file2},{score:.2f}\n")

    st.download_button(
    label=" Download Full Similarity Report (CSV)",
    data=csv_buffer.getvalue(),
    file_name="similarity_report.csv",
    mime="text/csv"
)