from datasets import load_dataset
import pandas as pd

def save_hf_dataset():
    ds = load_dataset("cmagganas/GenAI-job-postings-Dataset-sample")
    df = ds["train"].to_pandas()
    df = df.rename(columns={
        'job_title': 'title',
        'job_description': 'description',
        'job_location': 'location'
    })
    df.to_csv("data/sample_jobs.csv", index=False)
    print("Dataset saved as data/sample_jobs.csv")

if __name__ == "__main__":
    save_hf_dataset()
