import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = "../models/fake_news_model"
THRESHOLD = 0.55

device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.to(device)
model.eval()

def predict(text: str):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=64
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    probs = F.softmax(outputs.logits, dim=1)[0]

    fake_prob = probs[0].item()
    real_prob = probs[1].item()

    # highest confidence from model
    confidence = max(fake_prob, real_prob)

    # model’s raw label (no unverified here)
    label = "Fake" if fake_prob > real_prob else "Real"
    score = int(confidence * 100)

    return label, score, confidence