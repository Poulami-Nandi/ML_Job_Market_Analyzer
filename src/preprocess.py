import pandas as pd
import re

# Basic text cleaning
def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.lower().strip()
    return text

def preprocess_dataframe(df):
    df = df.copy()
    df['clean_description'] = df['description'].apply(clean_text)
    return df
