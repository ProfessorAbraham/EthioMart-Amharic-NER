
import pandas as pd
import re
import os

def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).strip()
    # Normalize spacing and remove emojis/symbols (optional)
    text = re.sub(r'[^\w\s፡።መንደር፣፤፥ቤትአበባዋጋብር0-9በ]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def preprocess_csv(input_path='telegram_data.csv', output_path='cleaned_telegram_data.csv'):
    if not os.path.exists(input_path):
        print("❌ telegram_data.csv not found.")
        return

    df = pd.read_csv(input_path)

    # Drop duplicates and clean nulls
    df.drop_duplicates(subset=['Channel Username', 'ID'], inplace=True)
    df = df[df['Message'].notna()]

    # Clean text
    df['Cleaned_Message'] = df['Message'].apply(clean_text)

    # Save cleaned version
    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned data saved to {output_path}")

if __name__ == "__main__":
    preprocess_csv()
