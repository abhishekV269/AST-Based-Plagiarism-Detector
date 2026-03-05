## AST-Based Plagiarism Detector – See Beyond the Surface
It uses **Abstract Syntax Trees (AST)** to understand the true structural skeleton of Python programs and catches similarities that simple string or token comparison would miss.
Perfect for university TAs, professors, coding bootcamp instructors, and anyone who wants to preserve academic integrity without spending hours manually reviewing submissions.

## What makes this detector special?
- Doesn't care about variable names, whitespace, or comments  
- Resistant to common obfuscation tricks (renaming, reordering independent statements, inverting loops, etc.)  
- Compares the **deep structure** of the logic using Python’s native AST  
- Clean, modern **Streamlit** interface – beautiful and actually pleasant to use  
- Instantly highlights the **most suspicious pairs**  
- Shows a clear similarity percentage + top matching code structures  
- One-click export of a professional similarity report (CSV / Markdown)

## How It Works
Python source code is parsed using Python's ast module.
AST node types are extracted from each program.
Node sequences are compared using sequence similarity.
Structural similarity score is calculated.
Files with similarity above threshold are flagged.

## Tech Stack
Python
AST (Abstract Syntax Tree)
Streamlit
Sequence Matching



##Try it – 60 seconds setup
```bash
# 1. Clone & enter
git clone https://github.com/abhishekV269/AST-Based-Plagiarism-Detector.git
cd AST-Based-Plagiarism-Detector

# 2. Install (preferably in venv)
pip install -r requirements.txt

# 3. Run 
streamlit run app.py

