import json
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)
from sklearn.metrics import accuracy_score

DATA_PATH = "../data/processed/clean_data.json"
MODEL_PATH = "../models/fake_news_model"


# ===== LOAD DATA =====
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"📊 Total samples: {len(data)}")

# ===== LABEL FIX =====
for item in data:
    item["label"] = 0 if item["label"] == "FAKE" else 1

dataset = Dataset.from_list(data)

# ===== TOKENIZER & MODEL =====
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)


def tokenize(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        padding="max_length",
        max_length=96
    )


dataset = dataset.map(tokenize, batched=True)
dataset = dataset.train_test_split(test_size=0.1)

model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=2
)

device = "cuda" if torch.cuda.is_available() else "cpu"
print("🚀 Using device:", device)
model.to(device)


# ===== METRICS =====
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = logits.argmax(axis=1)
    return {"accuracy": accuracy_score(labels, preds)}


# ===== TRAINING ARGS =====
training_args = TrainingArguments(
    output_dir="../models/checkpoints",
    num_train_epochs=3,                  # important
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,

    evaluation_strategy="epoch",
    save_strategy="epoch",
    save_total_limit=2,

    logging_steps=100,
    fp16=torch.cuda.is_available(),

    dataloader_num_workers=0,           # Windows safe
)


# ===== TRAIN =====
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    compute_metrics=compute_metrics,
)

trainer.train()

# ===== SAVE =====
trainer.save_model(MODEL_PATH)
tokenizer.save_pretrained(MODEL_PATH)

print("✅ Full training complete. Model saved.")