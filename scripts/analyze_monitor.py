import json
from collections import Counter

LOG_FILE = "../backend/logs/monitor_log.json"

labels = []
texts = []

with open(LOG_FILE, "r", encoding="utf-8") as f:
    for line in f:
        entry = json.loads(line)
        labels.append(entry["label"])
        texts.append(entry["input"])

print("🔍 Total problematic cases:", len(texts))
print("Label distribution:", Counter(labels))

print("\n🧠 Sample confusing inputs:\n")
for t in texts[:20]:
    print("-", t)