import pandas as pd
import os

# Define paths
current_dir = os.path.dirname(os.path.abspath(__file__))

# 1. Load Phishing Data (assuming these are all phishing)
df_phish = pd.read_csv(os.path.join(current_dir, "final_dataset.csv"))
# If your CSV has a different column name for the URL, change 'url' below
df_phish = df_phish[['url']].copy() 
df_phish['label'] = 1  # Label 1 = Phishing

# 2. Load Tranco Safe Data
# Tranco usually has no headers, so we name them 'rank' and 'url'
df_safe = pd.read_csv(os.path.join(current_dir, "tranco_oneml_safe.csv"), names=['rank', 'url'], header=None)
df_safe['url'] = "https://www." + df_safe['url'] # Make it a full URL
df_safe['label'] = 0  # Label 0 = Safe
df_safe = df_safe[['url', 'label']]

# 3. Balance the dataset
# To prevent the model from being biased, we take an equal number of safe and phishing URLs
sample_size = min(len(df_phish), len(df_safe))
df_phish_sampled = df_phish.sample(n=sample_size, random_state=42)
df_safe_sampled = df_safe.sample(n=sample_size, random_state=42)

# 4. Combine and Shuffle
final_df = pd.concat([df_phish_sampled, df_safe_sampled], ignore_index=True)
final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)

# 5. Save
final_df.to_csv(os.path.join(current_dir, "balanced_labeled_dataset.csv"), index=False)
print(f"Success! Created dataset with {sample_size} phishing and {sample_size} safe URLs.")