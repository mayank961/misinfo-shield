import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering

PENDING_CLAIMS_PATH = "../data/pending_claims.json"
CLUSTERS_PATH = "../data/claim_clusters.json"

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_pending_claims():
    with open(PENDING_CLAIMS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_clusters(clusters):
    with open(CLUSTERS_PATH, "w", encoding="utf-8") as f:
        json.dump(clusters, f, indent=2, ensure_ascii=False)


def cluster_claims(claims, threshold=1.2):
    texts = [c["text"] for c in claims]

    print("🔢 Generating embeddings...")
    embeddings = model.encode(texts)

    print("🧠 Clustering similar claims...")
    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=threshold,
        metric="euclidean",
        linkage="ward"
    )
    labels = clustering.fit_predict(embeddings)

    clusters = {}
    for label, claim in zip(labels, claims):
        clusters.setdefault(int(label), []).append(claim)

    return clusters


def main():
    claims = load_pending_claims()

    if not claims:
        print("⚠️ No pending claims to cluster.")
        return

    clusters = cluster_claims(claims)

    print(f"✅ Created {len(clusters)} clusters")
    save_clusters(clusters)
    print("💾 Saved to claim_clusters.json")


if __name__ == "__main__":
    main()