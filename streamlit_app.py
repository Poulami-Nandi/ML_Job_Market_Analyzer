import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os
import subprocess
import spacy
from spacy.cli import download

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

from src.preprocess import preprocess_dataframe
from src.skill_extractor import extract_skills

st.set_page_config(page_title="ML Job Market Analyzer", layout="wide")
st.title("📈 ML Job Market Analyzer")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload a job dataset (Parquet or CSV)", type=["csv", "parquet"])

if uploaded_file:
    # Load dataset
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_parquet(uploaded_file)

    # Column renaming
    rename_map = {
        'job_title': 'title',
        'job_posting': 'description',
        'position_level': 'position_level',
        'use_case': 'use_case',
        'cover_letter': 'cover_letter'
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Preprocess and extract skills
    df = preprocess_dataframe(df)
    df['skills'] = df['clean_description'].apply(extract_skills)

    st.success("✅ Data loaded and processed successfully")

    # Show raw and cleaned data
    with st.expander("🔍 Preview Data"):
        st.dataframe(df[['title', 'description', 'skills']].head())

    # Skill frequency
    all_skills = [s for skills in df['skills'] if isinstance(skills, list) for s in skills]
    skill_counts = pd.Series(all_skills).value_counts()
    top_skills = skill_counts.head(20)

    # --- Word Cloud ---
    st.subheader("☁️ Word Cloud of Skills")
    wordcloud = WordCloud(width=1000, height=400, background_color="white").generate_from_frequencies(skill_counts)
    fig_wc, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig_wc)

    # --- Bar Chart ---
    st.subheader("📊 Top 20 Skills by Frequency")
    fig_bar, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=top_skills.values, y=top_skills.index, ax=ax, palette="viridis")
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Skill")
    st.pyplot(fig_bar)

    # --- Heatmap ---
    st.subheader("🔥 Skill Co-occurrence Heatmap")
    def build_skill_matrix(skill_series, top_n=15):
        top = skill_counts.head(top_n).index.tolist()
        binary_matrix = []
        for skills in skill_series:
            row = [1 if s in skills else 0 for s in top]
            binary_matrix.append(row)
        return pd.DataFrame(binary_matrix, columns=top)

    skill_matrix = build_skill_matrix(df['skills'])
    correlation = skill_matrix.corr()

    fig_heatmap, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig_heatmap)

    # --- Downloadable CSV ---
    st.subheader("📥 Download Processed Results")
    save_cols = [col for col in ['title', 'description', 'skills'] if col in df.columns]
    st.download_button(
        label="Download CSV",
        data=df[save_cols].to_csv(index=False),
        file_name="processed_skills.csv",
        mime="text/csv"
    )
else:
    st.info("👆 Upload a CSV or Parquet job dataset to get started.")
