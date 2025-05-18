import streamlit as st
import pandas as pd
from src.skill_extractor import extract_skills
from src.preprocess import preprocess_dataframe

st.title("📈 ML Job Market Analyzer")

uploaded_file = st.file_uploader("Upload job dataset (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df = preprocess_dataframe(df)
    df['skills'] = df['clean_description'].apply(extract_skills)

    st.subheader("Sample Extracted Skills")
    st.write(df[['title', 'skills']].head())

    skill_counts = pd.Series([s for lst in df['skills'] for s in lst]).value_counts()
    st.subheader("Top Skills")
    st.bar_chart(skill_counts.head(15))
