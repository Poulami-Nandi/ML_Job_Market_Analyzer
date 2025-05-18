import spacy

nlp = spacy.load("en_core_web_sm")

COMMON_SKILLS = [
    "python", "sql", "machine learning", "deep learning", "pandas", "numpy", 
    "tensorflow", "keras", "scikit-learn", "nlp", "aws", "pytorch", "docker"
]

def extract_skills(text):
    doc = nlp(text)
    tokens = [token.text.lower() for token in doc]
    return list(set([skill for skill in COMMON_SKILLS if skill in tokens]))
