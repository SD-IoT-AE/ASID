"""
Extracts feature vectors from P4 digests or live packet captures.
"""
import json, pandas as pd, numpy as np

def parse_digest(digest_json):
    features = []
    for d in digest_json:
        features.append({
            "flow_hash": d["flow_hash"],
            "payload_len": d["payload_len"],
            "entropy": d["entropy"],
            "encoded_ratio": d["encoded_ratio"],
            "label": 0  # default benign
        })
    return pd.DataFrame(features)

if __name__ == "__main__":
    with open("sample_digests.json") as f:
        digests = json.load(f)
    df = parse_digest(digests)
    df.to_csv("detection/data/PASD.csv", index=False)
    print("[FeatureExtractor] Extracted and saved PASD.csv")
