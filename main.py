import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os
from src.preprocess import preprocess_dataframe
from src.skill_extractor import extract_skills
from datetime import datetime
import re # Import re for clean_text
import spacy # Import spacy for extract_skills
from sklearn.feature_extraction.text import CountVectorizer # Import needed here

# --- Place function definitions here ---
# These should ideally be imported from src modules, but for notebook execution,
# defining them here or ensuring they were run in a previous cell is necessary.
# Copying definitions from ipython-input-23- for clarity within this cell.

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # Modify cleaning: Keep letters, numbers, and whitespace, and also hyphens
    # This is less aggressive and might preserve skill phrases better
    text = re.sub(r'[^a-zA-Z0-9\s-]', '', text)
    return text.lower().strip()

# Assuming the preprocess_dataframe also relies on 'description' column handling
def preprocess_dataframe(df):
    df = df.copy()
    # Ensure 'description' column exists before applying clean_text
    if 'description' in df.columns:
        df['clean_description'] = df['description'].apply(clean_text)
    else:
        df['clean_description'] = "" # Create an empty column if 'description' is missing
        print("Warning: 'description' column not found for cleaning.")
    return df

# Define DummyNLP class BEFORE extract_skills function
class DummyNLP:
    def __call__(self, text):
        return [] # Return empty list for simplified testing

# Define nlp and COMMON_SKILLS before extract_skills
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    print(f"Error loading spacy model: {e}. Please run `!python -m spacy download en_core_web_sm`")
    # Assign the dummy object if loading fails
    nlp = DummyNLP()


COMMON_SKILLS = [
    "python", "sql", "machine learning", "deep learning", "pandas", "numpy",
    "tensorflow", "keras", "scikit-learn", "nlp", "aws", "pytorch", "docker"
]


def extract_skills(text):
    # Handle non-string input gracefully
    if not isinstance(text, str):
        return []
    # Check if nlp is a dummy object, if so return empty to prevent errors
    # DummyNLP is now defined in this cell's scope BEFORE this function
    if isinstance(nlp, DummyNLP):
         return []

    doc = nlp(text)
    # Use lemma_ for potentially better matching, but keep token.text for common skills
    tokens = [token.text.lower() for token in doc]
    # Also consider checking for phrases in the COMMON_SKILLS list
    found_skills = []
    text_lower = text.lower()
    for skill in COMMON_SKILLS:
        # Check if the skill phrase exists in the cleaned text
        if skill in text_lower:
            found_skills.append(skill)
    return list(set(found_skills))

# Flatten skill list into binary matrix (define before use)
def build_skill_matrix(skill_series, top_n=15):
    # Ensure skill_counts is defined before calling this function
    if 'skill_counts' not in globals():
        print("Warning: skill_counts not defined. Cannot build skill matrix.")
        return pd.DataFrame() # Return empty if skill_counts is missing

    top = skill_counts.head(top_n).index.tolist()
    binary_matrix = []
    for skills in skill_series:
        row = [1 if s in skills else 0 for s in top]
        binary_matrix.append(row)
    return pd.DataFrame(binary_matrix, columns=top)


# --- End of function definitions ---


# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

# 1. Load and Prepare Data
file_path = "/content/train-00000-of-00001-d119c151c7ae3346.parquet"
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Data file not found: {file_path}")

df = pd.read_parquet(file_path)
print("Loaded data with columns:", df.columns.tolist())

# 2. Rename Columns
rename_map = {
    'job_title': 'title',
    'job_posting': 'description',
    'position_level': 'position_level',
    'use_case': 'use_case',
    'cover_letter': 'cover_letter'
}
df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

if 'description' not in df.columns:
    raise ValueError("'description' column missing. Cannot proceed.")

# 3. Preprocess Descriptions
df = preprocess_dataframe(df)
print(df['clean_description'])

# 4. Extract Skills
# This line now correctly references the extract_skills and DummyNLP defined above
df['skills'] = df['clean_description'].apply(extract_skills)

# 5. Compute Skill Frequencies
all_skills = [s for skills in df['skills'] if isinstance(skills, list) for s in skills]
skill_counts = pd.Series(all_skills).value_counts()

# 6. Save Top N Skills to CSV
if not skill_counts.empty: # Check if skill_counts is not empty before slicing/saving
    top_skills = skill_counts.head(20)
    top_skills.to_csv("output/top_skills.csv")
else:
    print("\n⚠️ No skills found to save top skills CSV.")


# 7. Generate Word Cloud
if not skill_counts.empty: # Only generate if there are skills
    plt.figure(figsize=(12, 6))
    wordcloud = WordCloud(width=1000, height=400, background_color="white").generate_from_frequencies(skill_counts)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("Most Common Extracted ML Skills")
    plt.tight_layout()
    plt.savefig("output/skills_wordcloud.png")
    plt.show()
else:
     print("\n⚠️ No skills found to generate word cloud.")


# 8. Skill Frequency Bar Chart
if not skill_counts.empty: # Only generate if there are skills
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_skills.values, y=top_skills.index, palette="viridis")
    plt.xlabel("Frequency")
    plt.ylabel("Skill")
    plt.title("Top 20 Extracted ML Skills")
    plt.tight_layout()
    plt.savefig("output/skills_barplot.png")
    plt.show()
else:
    print("\n⚠️ No skills found to generate bar chart.")


# 9. Skill Occurrence Heatmap
# Only generate if there are enough skills for a meaningful heatmap (e.g., > 1)
if not skill_counts.empty and len(skill_counts) > 1:
    skill_matrix = build_skill_matrix(df['skills'], top_n=min(15, len(skill_counts))) # Adjust top_n based on available skills
    if not skill_matrix.empty and skill_matrix.shape[1] > 1: # Check if matrix is not empty and has enough columns
        correlation = skill_matrix.corr()

        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation, annot=True, cmap="coolwarm")
        plt.title("Skill Co-occurrence Correlation Heatmap")
        plt.tight_layout()
        plt.savefig("output/skills_heatmap.png")
        plt.show()
    else:
         print("\n⚠️ Not enough distinct top skills to generate heatmap.")

else:
    print("\n⚠️ No skills or not enough distinct skills to generate heatmap.")


# 10. Save Processed Job Data
save_cols = [col for col in ['title', 'location', 'skills', 'description'] if col in df.columns]
df[save_cols].to_csv("output/processed_jobs.csv", index=False)

print("\nOutputs saved to output/ directory:")
print("- processed_jobs.csv")
if not skill_counts.empty:
    print("- top_skills.csv")
if not skill_counts.empty:
     print("- skills_wordcloud.png")
if not skill_counts.empty:
    print("- skills_barplot.png")
if not skill_counts.empty and len(skill_counts) > 1 and skill_matrix.shape[1] > 1:
    print("- skills_heatmap.png")
