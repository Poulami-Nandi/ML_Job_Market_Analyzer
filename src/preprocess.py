import re

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'[^a-zA-Z0-9\\s]', '', text)
    return text.lower().strip()

def preprocess_dataframe(df):
    df = df.copy()
    df['clean_description'] = df['description'].apply(clean_text)
    return df
