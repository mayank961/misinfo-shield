import json

with open("../data/raw/news_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

fake = sum(1 for x in data if x["label"] == "FAKE")
real = sum(1 for x in data if x["label"] == "REAL")

print("FAKE:", fake)
print("REAL:", real)