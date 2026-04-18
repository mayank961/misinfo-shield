import json
import torch
from datasets import Dataset
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from tqdm import tqdm

MODEL_PATH = "../models/fake_news_model"
DATA_PATH = "../data/processed/clean_data.json"

# ===== LOAD DATA =====
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"📊 Total dataset: {len(data)}")

for item in data:
    item["label"] = 0 if item["label"] == "FAKE" else 1

dataset = Dataset.from_list(data)

# ===== LOAD MODEL =====
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval()

print("🚀 Evaluating on:", device)

# ===== TOKENIZE ONCE =====
def tokenize(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        padding="max_length",
        max_length=64
    )

dataset = dataset.map(tokenize, batched=True, batch_size=1000)

dataset.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "label"]
)

# ===== DATALOADER =====
loader = DataLoader(dataset, batch_size=256, shuffle=False)

preds = []
labels = []

print("🔄 Running predictions...")

# ===== PREDICTION LOOP WITH PROGRESS =====
with torch.no_grad():
    for batch in tqdm(loader, desc="Evaluating", unit="batch"):
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        label = batch["label"].numpy()

        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits

        batch_preds = torch.argmax(logits, dim=1).cpu().numpy()

        preds.extend(batch_preds)
        labels.extend(label)

# ===== METRICS =====
accuracy = accuracy_score(labels, preds)

print("\n📈 ===== RESULTS =====")
print(f"✅ Accuracy: {accuracy * 100:.2f}%")

print("\n📊 Classification Report:")
print(classification_report(labels, preds, target_names=["FAKE", "REAL"]))

print("\n📊 Confusion Matrix:")
print(confusion_matrix(labels, preds))