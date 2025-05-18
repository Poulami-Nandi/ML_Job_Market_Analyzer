import spacy

nlp = spacy.load("en_core_web_sm")

COMMON_SKILLS = [
    "python", "sql", "machine learning", "deep learning", "pandas", "numpy",
    "tensorflow", "keras", "scikit-learn", "nlp", "aws", "pytorch", "docker"
]

def extract_skills(text):
    if not isinstance(text, str):
        return []
    doc = nlp(text)
    tokens = [token.text.lower() for token in doc]
    found_skills = []
    text_lower = text.lower()
    for skill in COMMON_SKILLS:
        if skill in text_lower:
            found_skills.append(skill)
    return list(set(found_skills))
