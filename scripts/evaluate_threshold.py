import json
import torch
import torch.nn.functional as F
from tqdm import tqdm
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score

MODEL_PATH = "../models/fake_news_model"
DATA_PATH = "../data/processed/clean_data.json"

device = "cuda" if torch.cuda.is_available() else "cpu"

# ===== Load model =====
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.to(device)
model.eval()

# ===== Load data =====
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    item["label"] = 0 if item["label"] == "FAKE" else 1

dataset = Dataset.from_list(data)

def get_probs(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=64
    ).to(device)

    with torch.no_grad():
        logits = model(**inputs).logits

    probs = F.softmax(logits, dim=1)[0]
    return probs[0].item(), probs[1].item()  # fake, real


# ===== Collect probabilities once =====
print("🔄 Collecting probabilities...")
all_probs = []
all_labels = []

for item in tqdm(dataset):
    fake_p, real_p = get_probs(item["text"])
    all_probs.append((fake_p, real_p))
    all_labels.append(item["label"])

# ===== Test thresholds =====
print("\n📊 Testing thresholds...\n")

for threshold in [x/100 for x in range(50, 91, 5)]:
    preds = []

    for fake_p, real_p in all_probs:
        if fake_p > threshold:
            preds.append(0)
        else:
            preds.append(1)

    acc = accuracy_score(all_labels, preds)
    print(f"Threshold {threshold:.2f} → Accuracy: {acc*100:.2f}%")