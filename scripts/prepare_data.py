import json

# Load raw data
with open("../data/raw/news_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

processed = []

for item in data:
    text = item["text"].strip()
    label = item["label"].upper()
    language = item["language"]

    processed.append({
        "text": text,
        "label": label,
        "language": language,
        "category": item.get("category", "general"),
        "source": item.get("source", "unknown")
    })

# Save processed data
with open("../data/processed/clean_data.json", "w", encoding="utf-8") as f:
    json.dump(processed, f, indent=2, ensure_ascii=False)

print("✅ Data cleaned and saved!")