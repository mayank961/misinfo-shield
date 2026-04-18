import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_ID = "mayankbh765/misinfo-shield-model"
THRESHOLD = 0.55
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading model from HuggingFace: {MODEL_ID}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
model.to(device)
model.eval()
print("Model loaded successfully!")

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
    confidence = max(fake_prob, real_prob)
    label = "Fake" if fake_prob > real_prob else "Real"
    score = int(confidence * 100)
    return label, score, confidence
