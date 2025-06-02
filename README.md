# 📊 ML Job Market Analyzer

An interactive Streamlit dashboard that analyzes machine learning job listings and extracts top skill trends across the industry.

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live_App-ff4b4b?logo=streamlit&logoColor=white)](https://mljobmarketanalyzer-fwxncqfv3ugxaxrq5zrxez.streamlit.app/)

![Banner](https://github.com/Poulami-Nandi/IV_surface_analyzer/raw/main/images/own/own_image.jpg)

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

1. **Upload Dataset**:
    - Upload a `.parquet` file with job descriptions (must have a 'description' column).

2. **Single Job Link**:
    - Paste a URL to a specific job description.
    - HTML is parsed, and skill keywords are extracted.

3. **Job Board Page (Beta)**:
    - Provide a link to a job search result (LinkedIn, Glassdoor, etc.).
    - Requires `Selenium` for full dynamic content parsing.

---

## 🛠️ Technologies Used

- `Streamlit` for the web app UI
- `BeautifulSoup` for parsing static job descriptions
- `Selenium` for scraping dynamic job boards (JS-rendered pages)
- `Pandas`, `Matplotlib`, `WordCloud`, `Counter` for analysis

---

## 👤 Author

**Dr. Poulami Nandi**  
Physicist | Quant Researcher | Data Scientist  
- 📧 Email: [nandi.poulami91@gmail.com](mailto:nandi.poulami91@gmail.com), [pnandi@sas.upenn.edu](mailto:pnandi@sas.upenn.edu)  
- 🌐 [LinkedIn](https://www.linkedin.com/in/poulami-nandi-a8a12917b/) • [GitHub](https://github.com/Poulami-Nandi) • [Google Scholar](https://scholar.google.co.in/citations?user=bOYJeAYAAAAJ&hl=en)

---

## 📎 License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.