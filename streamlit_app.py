import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

# --- Predefined skills list ---
keywords = [
    "python", "sql", "excel", "tensorflow", "keras", "pytorch", "numpy", "pandas", "nlp",
    "machine learning", "deep learning", "data science", "power bi", "tableau", "scikit-learn",
    "sklearn", "aws", "azure", "gcp", "docker", "kubernetes", "spark", "hadoop", "mlops", "git"
]

# --- Skill extraction ---
def extract_skills_from_text(text, return_counts=False):
    text = text.lower()
    found = [kw for kw in keywords if kw in text]
    return Counter(found) if return_counts else {k: found.count(k) for k in set(found)}

# --- Banner ---
st.set_page_config(page_title="ML Job Market Analyzer", layout="wide")
st.title("📊 ML Job Market Analyzer")
# 👇 Create two columns
col1, col2 = st.columns([3, 1])  # Left wider for text, right for image

# 🧾 Left side: Bio and Links
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

# 🖼️ Right side: Image
with col2:
    st.image("https://github.com/Poulami-Nandi/IV_surface_analyzer/raw/main/images/own/own_image.jpg",
             caption="Dr. Poulami Nandi",
             use_column_width=True)
st.markdown("---")

# --- Sidebar Options ---
option = st.sidebar.radio(
    "Choose input method",
    ("Upload Job Dataset", "Single Job Link", "Job Board Page Link")
)

# === OPTION 1: Upload dataset ===
if option == "Upload Job Dataset":
    uploaded_file = st.file_uploader("Upload a .parquet job listing file", type=["parquet"])
    if uploaded_file is not None:
        df = pd.read_parquet(uploaded_file)

        st.success(f"File loaded: {uploaded_file.name}")
        st.dataframe(df.head())

        # Skills frequency analysis
        all_skills = Counter()
        for text in df['description'].dropna():
            all_skills += extract_skills_from_text(text, return_counts=True)

        top_skills = all_skills.most_common(20)

        st.subheader("Top 20 Skills Frequency")
        skill_df = pd.DataFrame(top_skills, columns=["Skill", "Count"])
        st.bar_chart(skill_df.set_index("Skill"))

        st.subheader("Skill Word Cloud")
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(all_skills)
        st.image(wordcloud.to_array())

# === OPTION 2: Single Job Link ===
elif option == "Single Job Link":
    job_url = st.text_input("Paste the job post link (e.g., LinkedIn/Glassdoor/etc.)")

    if job_url:
        try:
            response = requests.get(job_url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text(separator=" ")

            skills = extract_skills_from_text(page_text, return_counts=True)
            st.success("Top extracted skills:")
            for skill, count in skills.most_common(10):
                st.markdown(f"- {skill} ({count})")

            # Skill cloud
            st.subheader("Skill Word Cloud")
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(skills)
            st.image(wordcloud.to_array())

        except Exception as e:
            st.error(f"Failed to fetch or parse job post: {e}")

# === OPTION 3: Job Board Link (Work In Progress) ===
elif option == "Job Board Page Link":
    board_url = st.text_input("Paste a job board search results page URL (e.g., LinkedIn search page)")

    st.warning("⚠️ This feature is a work in progress. Full job info extraction from job boards requires JavaScript rendering.")

    if board_url:
        st.info("Parsing HTML... but LinkedIn/Glassdoor job boards often require dynamic rendering (e.g., Selenium).")
        st.code("Use Selenium for reliable scraping of dynamic job listings.")

        try:
            response = requests.get(board_url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, "html.parser")
            all_li = soup.find_all("li")

            job_list = []
            for li in all_li:
                text = li.get_text(separator=" ", strip=True)
                if "Data" in text or "Engineer" in text:
                    job_list.append(text[:100])

            if job_list:
                st.subheader("Sample scraped text from job cards:")
                for job in job_list[:5]:
                    st.markdown(f"- {job}")
            else:
                st.info("No job-like entries detected in HTML.")
        except Exception as e:
            st.error(f"Error scraping job board: {e}")
