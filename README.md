# 📊 ML Job Market Analyzer

An interactive Streamlit dashboard that analyzes machine learning job listings and extracts top skill trends across the industry.

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live_App-ff4b4b?logo=streamlit&logoColor=white)](https://mljobmarketanalyzer-fwxncqfv3ugxaxrq5zrxez.streamlit.app/)

<img src="https://github.com/Poulami-Nandi/IV_surface_analyzer/raw/main/images/own/own_image.jpg" alt="Poulami Nandi" width="180"/>

---

## 🚀 Features

- Upload your own job listings dataset (in `.parquet` format) and visualize key skills.
- Extract skills from a **single job post URL** (LinkedIn, Glassdoor, etc.).
- **[Beta]** Parse job board search result pages for bulk job extraction using `Selenium`.
- WordCloud and frequency bar charts of top in-demand skills.
- Streamlined interface via [Streamlit](https://streamlit.io).

---

## 🔍 Use Cases

- Identify top skills for ML roles in different companies or regions.
- Compare how job market requirements shift across postings.
- Extract keywords from public job boards and websites.

---

## 🧪 Input Modes

### 1. 📁 Upload Dataset (Recommended)

Upload a `.parquet` file that includes at least a `description` column.  
This triggers a detailed pipeline:

- Cleans and preprocesses all job descriptions
- Scans for 30+ predefined ML/DS skills (e.g., Python, SQL, TensorFlow)
- Displays:
  - Top skill frequencies via a bar chart
  - Word Cloud of skills
  - A preview of the uploaded dataset

**Sample Code Snippet:**

```python
uploaded_file = st.file_uploader("Upload a .parquet job listing file", type=["parquet"])
if uploaded_file is not None:
    df = pd.read_parquet(uploaded_file)

    all_skills = Counter()
    for text in df['description'].dropna():
        all_skills += extract_skills_from_text(text, return_counts=True)

    top_skills = all_skills.most_common(20)

    st.bar_chart(pd.DataFrame(top_skills, columns=["Skill", "Count"]).set_index("Skill"))

    wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(all_skills)
    st.image(wordcloud.to_array())
```

---

### 2. 🔗 Single Job Link

Paste a URL to a job post. The app fetches the content and scans for keywords, then displays:
- Top skills with counts
- Word Cloud

---

### 3. 🌐 Job Board Page (Beta)

Paste a job board search results page link. Scrapes all listed jobs using `Selenium`. Output includes:
- Company, title, location
- Aggregated top skills and their frequency
- Word cloud from all job posts

---

## 🛠️ Technologies Used

- `Streamlit` for web UI
- `BeautifulSoup` + `requests` for basic scraping
- `Selenium` for dynamic job boards
- `pandas`, `Counter`, `matplotlib`, `wordcloud`

---

## 👤 Author

**Dr. Poulami Nandi**  
Physicist | Quant Researcher | Data Scientist  
- 📧 Email: [nandi.poulami91@gmail.com](mailto:nandi.poulami91@gmail.com), [pnandi@sas.upenn.edu](mailto:pnandi@sas.upenn.edu)  
- 🌐 [LinkedIn](https://www.linkedin.com/in/poulami-nandi-a8a12917b/) • [GitHub](https://github.com/Poulami-Nandi) • [Google Scholar](https://scholar.google.co.in/citations?user=bOYJeAYAAAAJ&hl=en)

---

## 📎 License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.
