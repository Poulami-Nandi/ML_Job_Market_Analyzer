import re

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'[^a-zA-Z0-9\s-]', '', text)
    return text.lower().strip()

def preprocess_dataframe(df):
    df = df.copy()
    if 'description' in df.columns:
        df['clean_description'] = df['description'].apply(clean_text)
    else:
        df['clean_description'] = ""
        print("Warning: 'description' column not found for cleaning.")
    return df
