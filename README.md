# 📈 ML Job Market Analyzer

A Python-based NLP project that extracts and visualizes machine learning skills from real-world job descriptions. This tool helps you understand which tools, technologies, and roles are in demand by parsing job posting text, extracting skills using NLP, and generating charts and word clouds.

---

## 🚀 Project Highlights

- 📄 Load job postings from Hugging Face datasets or Parquet files
- 🧹 Clean and normalize job descriptions
- 🧠 Extract in-demand ML skills using spaCy and custom keyword lists
- 📊 Visualize top skills via bar charts and word clouds
- 📦 Export structured outputs for use in dashboards or analysis

---

## 🗂 Project Structure

```
MLJobMarketAnalyzer/
├── data/                     # Dataset files (e.g., .parquet or .csv)
├── output/                   # Exported CSVs and processed data
├── src/                      # Core logic modules
│   ├── preprocess.py         # Cleaning text and job descriptions
│   └── skill_extractor.py    # Skill extraction using NLP
├── tests/                    # Unit tests for core modules
│   └── test_src_modules.py   # Tests for text cleaning and skill extraction
├── main.py                   # Entry-point script for local processing
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation (you are here)
```

---

## 🧠 Core Modules

### 🔹 `src/preprocess.py`
Functions:
- `clean_text(text)` – Lowercases, removes punctuation, handles nulls
- `preprocess_dataframe(df)` – Adds a `clean_description` column based on `description`

### 🔹 `src/skill_extractor.py`
Functions:
- `extract_skills(text)` – Uses spaCy and a list of common ML skills to extract keywords

Example list includes:
```python
["python", "sql", "machine learning", "deep learning", "tensorflow", "keras", ...]
```

---

## 🧪 Unit Tests

Tested with `unittest` in `tests/test_src_modules.py`:
- Cleans text inputs correctly
- Handles missing/empty strings
- Extracts skills from various realistic job postings

Run tests using:
```bash
python -m unittest discover -s tests
```

---

## 📊 Visual Output

- **Word cloud** of most common skills
- **Bar chart** for top N skills
- **CSV export** with extracted skills per job

---

## 💾 How to Use

1. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

2. (Optional) Load dataset from Hugging Face:
```python
from datasets import load_dataset

# Load and convert to DataFrame
ds = load_dataset("cmagganas/GenAI-job-postings-Dataset-sample")
df = ds['train'].to_pandas()
```

3. Process the data:
```bash
python main.py
```

4. Output:
- `output/sample_skills.csv` — extracted skills per job
- word cloud + bar chart (opens in matplotlib window)

---

## 📈 Use Cases

- 📚 Educational tool to teach NLP + data cleaning
- 📊 Job market research and skill demand tracking
- 💼 Add to GitHub portfolio to showcase data pipeline and NLP skills

---

## 🧩 Future Enhancements

- [ ] Add BERTopic or LDA topic modeling
- [ ] Streamlit dashboard interface
- [ ] Salary and location-based visualizations
- [ ] Integration with real-time job boards

---

## 👤 Author

**Poulami Nandi**  
Postdoctoral Researcher • Data Scientist • Quant Researcher  
🔗 [LinkedIn](https://www.linkedin.com/in/poulami-nandi/)  
📫 nandi.poulami91@gmail.com

---

## 📜 License

This project is licensed under the **MIT License** — free to use, modify, and share.
