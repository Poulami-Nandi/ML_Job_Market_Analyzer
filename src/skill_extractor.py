import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

COMMON_SKILLS = ["python", "sql", "machine learning", "tensorflow", "pandas",
                 "scikit-learn", "data analysis", "deep learning", "nlp", "aws"]

def extract_skills(text):
    tokens = [token.text.lower() for token in nlp(text)]
    skills = [skill for skill in COMMON_SKILLS if skill in tokens]
    return list(set(skills))
