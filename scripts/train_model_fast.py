import json
import random
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# 📁 Load processed data
with open("../data/processed/clean_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"📊 Total data loaded: {len(data)}")

# 🔥 FAST TRAINING (sample limit)
MAX_SAMPLES = 20000

if len(data) > MAX_SAMPLES:
    data = random.sample(data, MAX_SAMPLES)

print(f"⚡ Using {len(data)} samples for training")

# 🧠 Prepare data
texts = [item["text"] for item in data]
labels = [item["label"] for item in data]

# 🔄 Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42
)

# 🧠 Vectorization (text → numbers)
vectorizer = TfidfVectorizer(
    max_features=10000,   # limit features (speed boost)
    ngram_range=(1, 2)    # better understanding
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 🤖 Model
model = LogisticRegression(max_iter=200)

print("🚀 Training model...")
model.fit(X_train_vec, y_train)

# 📊 Evaluate
y_pred = model.predict(X_test_vec)
acc = accuracy_score(y_test, y_pred)

print(f"✅ Training Accuracy: {acc * 100:.2f}%")

# 💾 Save model + vectorizer
with open("../models/model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("../models/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("💾 Model saved successfully!")