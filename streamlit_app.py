import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os
import subprocess
import spacy
from spacy.cli import download
import spacy

# Load the model as a package (it’s installed with pip via requirements.txt)
nlp = spacy.load("en_core_web_sm")
from src.preprocess import preprocess_dataframe
from src.skill_extractor import extract_skills

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import requests
from bs4 import BeautifulSoup

# ---------------------
# Page Configuration & Banner
# ---------------------
st.set_page_config(page_title="ML Job Market Analyzer", layout="wide")

col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("**👤 Created by:** Dr. Poulami Nandi  \n"
                "Physicist · Quant Researcher · Data Scientist")

    st.markdown("**🏛️ Affiliations:**  \n"
                "[University of Pennsylvania](https://live-sas-physics.pantheon.sas.upenn.edu/people/poulami-nandi) · "
                "[IIT Kanpur](https://www.iitk.ac.in/) · "
                "[IIT Gandhinagar](https://www.usief.org.in/home-institution-india/indian-institute-of-technology-gandhinagar/) · "
                "[UC Davis](https://www.ucdavis.edu/) · "
                "[TU Wien](http://www.itp.tuwien.ac.at/CPT/index.htm?date=201838&cats=xbrbknmztwd)")

    st.markdown("**📧 Email:**  \n"
                "[nandi.poulami91@gmail.com](mailto:nandi.poulami91@gmail.com), "
                "[pnandi@sas.upenn.edu](mailto:pnandi@sas.upenn.edu)")

    st.markdown("**🔗 Links:**  \n"
                "[LinkedIn](https://www.linkedin.com/in/poulami-nandi-a8a12917b/)  |  "
                "[GitHub](https://github.com/Poulami-Nandi)  |  "
                "[Google Scholar](https://scholar.google.co.in/citations?user=bOYJeAYAAAAJ&hl=en)")

with col2:
    st.image("https://github.com/Poulami-Nandi/IV_surface_analyzer/raw/main/images/own/own_image.jpg", width=100)

# ---------------------
# Sidebar Configuration
# ---------------------
st.sidebar.header("⚙️ Input Options")
input_mode = st.sidebar.radio("Choose Input Mode", ["Upload Dataset", "Provide Web Link", "Job Board Link"])

top_n_skills = st.sidebar.slider("Top N Skills to Display", min_value=5, max_value=30, value=10)
enable_wordcloud = st.sidebar.checkbox("Show WordCloud", value=True)
enable_barplot = st.sidebar.checkbox("Show Bar Chart", value=True)

keywords = ["python", "sql", "tensorflow", "pytorch", "ml", "ai", "docker", "spark", "pandas", "sklearn"]

# ---------------------
# Helper Functions
# ---------------------
def extract_skills_from_text(text):
    skill_counts = {}
    for kw in keywords:
        if kw in text.lower():
            skill_counts[kw] = skill_counts.get(kw, 0) + 1
    return skill_counts

from collections import Counter

def extract_skills_from_text(text, return_counts=False):
    words = text.lower()
    found = [kw for kw in keywords if kw in words]
    if return_counts:
        return Counter(found)
    return {k: found.count(k) for k in set(found)}

def scrape_job_description(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all(['p', 'li', 'div'])
        job_text = ' '.join(p.get_text(separator=' ', strip=True) for p in paragraphs)
        return job_text
    except Exception as e:
        st.error(f"❌ Error fetching job description from URL: {e}")
        return ""

def scrape_job_board(url):
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.find_all("li")

        job_list = []
        for job in job_cards:
            full_text = job.get_text(separator=" ", strip=True)

            if any(skip in full_text for skip in [
                "Privacy", "Cookie", "Policy", "Terms", "Copyright", "Guest Controls", "Accessibility"
            ]):
                continue

            title_tag = job.find(["h3", "h2", "a"])
            company_tag = job.find("h4") or job.find("span", class_="base-search-card__subtitle")
            location_tag = job.find("span", class_="job-search-card__location")

            title = title_tag.get_text(strip=True) if title_tag else ""
            company = company_tag.get_text(strip=True) if company_tag else "Unknown"
            location = location_tag.get_text(strip=True) if location_tag else "Unknown"

            # Heuristic skip
            if len(title) < 4 or title.lower() in ["about", "jobs", "people"]:
                continue

            # ✅ Extract skill frequency dict
            skill_counts = extract_skills_from_text(full_text, return_counts=True)

            if skill_counts:
                top_skills_str = ", ".join(f"{k}({v})" for k, v in skill_counts.most_common(5))
            else:
                top_skills_str = "None Detected"

            job_list.append({
                "Company Name": company,
                "Job Title": title[:100],
                "Location": location,
                "Published Date": "N/A",  # Could insert today's date or leave blank
                "Top Skills": top_skills_str
            })

        return pd.DataFrame(job_list)

    except Exception as e:
        st.error(f"❌ Error scraping job board: {e}")
        return pd.DataFrame()


# ---------------------
# Main Logic
# ---------------------
if input_mode == "Upload Dataset":
    uploaded_file = st.file_uploader("Upload Job Dataset (.parquet)", type=["parquet"])
    if uploaded_file:
        df = pd.read_parquet(uploaded_file)
        df["description"] = df["description"].astype(str)

        job_filter = st.sidebar.text_input("Keyword Filter (Job Titles / Description)", value="machine learning")
        min_length = st.sidebar.slider("Minimum Description Length", 100, 1000, 300)

        filtered_df = df[df["description"].str.contains(job_filter, case=False, na=False)]
        filtered_df = filtered_df[filtered_df["description"].str.len() > min_length]

        combined_text = " ".join(filtered_df["description"].tolist())
        skill_counts = extract_skills_from_text(combined_text)

elif input_mode == "Provide Web Link":
    url = st.text_input("Enter Job Posting URL")
    if url:
        job_description = scrape_job_description(url)
        st.subheader("📄 Extracted Job Description (Preview)")
        st.markdown(job_description[:2000] + "..." if len(job_description) > 2000 else job_description)
        skill_counts = extract_skills_from_text(job_description)

elif input_mode == "Job Board Link":
    board_url = st.text_input("Enter Job Board URL")
    if board_url:
        board_df = scrape_job_board(board_url)
        if not board_df.empty:
            st.subheader("📋 Job Listings")
            st.dataframe(board_df)

            combined_board_text = " ".join(board_df["Job Title"].tolist())
            skill_counts = extract_skills_from_text(combined_board_text)

# ---------------------
# Visualization
# ---------------------
if 'skill_counts' in locals() and skill_counts:
    skill_df = pd.DataFrame.from_dict(skill_counts, orient="index", columns=["Count"])
    skill_df = skill_df.sort_values(by="Count", ascending=False).head(top_n_skills)

    st.subheader("📊 Extracted Skill Frequencies")

    if enable_barplot:
        st.markdown("### 🔢 Top Skills by Frequency")
        fig, ax = plt.subplots()
        skill_df.plot(kind="barh", ax=ax, legend=False)
        ax.invert_yaxis()
        ax.set_xlabel("Frequency")
        ax.set_title("Top Skills")
        st.pyplot(fig)

    if enable_wordcloud:
        st.markdown("### ☁️ Word Cloud of Top Skills")
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(skill_counts)
        fig_wc, ax_wc = plt.subplots()
        ax_wc.imshow(wordcloud, interpolation="bilinear")
        ax_wc.axis("off")
        st.pyplot(fig_wc)

else:
    st.info("🔍 Awaiting input for analysis...")
