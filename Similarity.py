import difflib

def sequence_similarity(seq1, seq2):
    matcher = difflib.SequenceMatcher(None, seq1, seq2)
    return matcher.ratio() * 100