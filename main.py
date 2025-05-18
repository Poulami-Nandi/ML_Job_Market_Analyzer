import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
from src.preprocess import preprocess_dataframe
from src.skill_extractor import extract_skills

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

# Read Parquet file
df = pd.read_parquet("/content/train-00000-of-00001-d119c151c7ae3346.parquet")
print("Columns after loading Parquet:", df.columns)

# Rename columns
new_column_names = {
    'job_title': 'title',
    'job_posting': 'description',
    'position_level': 'position_level',
    'use_case': 'use_case',
    'cover_letter': 'cover_letter'
}
df = df.rename(columns={k: v for k, v in new_column_names.items() if k in df.columns})
print("Columns after renaming:", df.columns)

# Proceed only if 'description' is available
if 'description' in df.columns:
    df = preprocess_dataframe(df)

    print("\n--- Sample Cleaned Descriptions ---")
    for i, desc in enumerate(df['clean_description'].head()):
        print(f"Row {i}: {desc[:200]}...")
        if i >= 4: break

    df['skills'] = df['clean_description'].apply(extract_skills)

    print("\n--- Sample Extracted Skills ---")
    for i, skills in enumerate(df['skills'].head()):
        print(f"Row {i}: {skills}")
        if i >= 4: break

    all_skills = [skill for skills in df['skills'] if isinstance(skills, list) for skill in skills]
    skill_counts = pd.Series(all_skills).value_counts()

    print("\n--- Skill Counts ---")
    print(skill_counts)

    if not skill_counts.empty:
        print("\n📊 Top 10 Skills:")
        print(skill_counts.head(10))

        plt.figure(figsize=(12, 6))
        wordcloud = WordCloud(width=1000, height=400, background_color="white").generate_from_frequencies(skill_counts)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.title("Most Common Extracted ML Skills")
        plt.show()

        cols_to_save = ['title', 'location', 'skills']
        cols_to_save_existing = [col for col in cols_to_save if col in df.columns]

        df[cols_to_save_existing].to_csv("output/sample_skills.csv", index=False)
        print("✅ Saved processed data to output/sample_skills.csv")
    else:
        print("\n⚠️ No skills found to generate word cloud or save data.")
else:
    print("\nError: 'description' column not found after renaming. Cannot proceed with preprocessing and skill extraction.")
