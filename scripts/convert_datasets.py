import pandas as pd
import json
import re

# 📁 OUTPUT FILE
OUTPUT_FILE = "../data/raw/news_data.json"

# 🧠 Clean text function
def clean_text(text):
    text = str(text)
    text = re.sub(r"http\S+", "", text)  # remove URLs
    text = re.sub(r"[^a-zA-Z0-9\u0900-\u097F\s]", "", text)  # keep Hindi + English
    text = re.sub(r"\s+", " ", text).strip()
    return text


# 🧩 Convert Kaggle Fake News Dataset
def process_kaggle(fake_path, true_path):
    data = []

    fake_df = pd.read_csv(fake_path)
    true_df = pd.read_csv(true_path)

    for _, row in fake_df.iterrows():
        text = clean_text(row.get("text", ""))
        if len(text) > 20:
            data.append({
                "text": text,
                "label": "FAKE",
                "language": "en",
                "category": "news",
                "source": "kaggle"
            })

    for _, row in true_df.iterrows():
        text = clean_text(row.get("text", ""))
        if len(text) > 20:
            data.append({
                "text": text,
                "label": "REAL",
                "language": "en",
                "category": "news",
                "source": "kaggle"
            })

    print(f"✅ Kaggle data processed: {len(data)} samples")
    return data


# 🧩 Convert LIAR Dataset
def process_liar(file_path):
    data = []

    df = pd.read_csv(file_path, sep="\t", header=None)

    for _, row in df.iterrows():
        label = row[1]
        text = clean_text(row[2])

        if label in ["false", "pants-fire", "barely-true"]:
            final_label = "FAKE"
        elif label in ["true", "mostly-true"]:
            final_label = "REAL"
        else:
            continue

        if len(text) > 15:
            data.append({
                "text": text,
                "label": final_label,
                "language": "en",
                "category": "politics",
                "source": "liar"
            })

    print(f"✅ LIAR data processed: {len(data)} samples")
    return data


# 🧩 Convert Hindi Dataset

def process_hindi(file_path):
    data = []

    df = pd.read_csv(file_path)

    print("🧠 Hindi Columns:", df.columns)

    for _, row in df.iterrows():
        # Fix column name issue (comma problem)
        text = row.get("text") or row.get(",text")
        label = row.get("label")

        if not text:
            continue

        text = clean_text(text)

        # Handle numeric labels
        if str(label) == "0":
            final_label = "FAKE"
        elif str(label) == "1":
            final_label = "REAL"
        else:
            continue

        if len(text) > 10:
            data.append({
                "text": text,
                "label": final_label,
                "language": "hi",
                "category": "news",
                "source": "hindi_dataset"
            })

    print(f"✅ Hindi data processed: {len(data)} samples")
    return data


# 🧩 MAIN FUNCTION

def main():
    print("🚀 Script started...")

    all_data = []

    try:
        kaggle_data = process_kaggle(
            "../datasets/Fake.csv",
            "../datasets/True.csv"
        )
        all_data.extend(kaggle_data)
    except Exception as e:
        print("❌ Kaggle error:", e)

    try:
        liar_data = process_liar(
            "../datasets/train.tsv"
        )
        all_data.extend(liar_data)
    except Exception as e:
        print("❌ LIAR error:", e)

    try:
        hindi_data = process_hindi(
            "../datasets/hindi_news.csv"
        )
        all_data.extend(hindi_data)
    except Exception as e:
        print("❌ Hindi error:", e)

    print("📊 Total collected:", len(all_data))

    if len(all_data) == 0:
        print("❌ No data processed. Check file paths!")
        return

    unique_data = {item["text"]: item for item in all_data}
    final_data = list(unique_data.values())

    print(f"🔥 Final dataset: {len(final_data)}")

    with open("../data/raw/news_data.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    print("✅ Saved successfully!")
if __name__ == "__main__":
    main()