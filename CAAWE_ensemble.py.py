"""
CAAWE: Confidence-Aware Adaptive Weighted Ensemble
Implements SQLi detection using KNN, Decision Tree, Random Forest, and SVM.
Weights are adjusted dynamically based on recent performance confidence.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from base_models.knn_model import KNNModel
from base_models.decision_tree_model import DecisionTreeModel
from base_models.random_forest_model import RandomForestModel
from base_models.svm_model import SVMModel
import requests, json, joblib, os, time

DMCM_ENDPOINT = "http://127.0.0.1:5005/api/mitigation"

class CAAWEEnsemble:
    def __init__(self):
        self.models = {
            "knn": KNNModel(),
            "dt": DecisionTreeModel(),
            "rf": RandomForestModel(),
            "svm": SVMModel()
        }
        self.weights = {m: 1.0/len(self.models) for m in self.models}
        self.scaler = StandardScaler()

    def fit(self, X, y):
        X_scaled = self.scaler.fit_transform(X)
        for name, model in self.models.items():
            model.fit(X_scaled, y)

    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        preds, confs = {}, {}
        for name, model in self.models.items():
            preds[name], confs[name] = model.predict(X_scaled)
        final_pred = self._weighted_vote(preds, confs)
        return final_pred, confs

    def _weighted_vote(self, preds, confs):
        combined = []
        for i in range(len(next(iter(preds.values())))):
            votes = {}
            for name in preds:
                p = preds[name][i]
                weight = self.weights[name] * confs[name][i]
                votes[p] = votes.get(p, 0) + weight
            combined.append(max(votes, key=votes.get))
        return np.array(combined)

    def update_weights(self, X_val, y_val):
        X_scaled = self.scaler.transform(X_val)
        scores = {}
        for name, model in self.models.items():
            y_pred, conf = model.predict(X_scaled)
            scores[name] = f1_score(y_val, y_pred)
        total = sum(scores.values())
        for name in self.weights:
            self.weights[name] = scores[name] / total if total > 0 else 1.0/len(self.models)

    def save(self, path="detection/models/ensemble.joblib"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({"models": self.models, "scaler": self.scaler, "weights": self.weights}, path)

    def load(self, path="detection/models/ensemble.joblib"):
        obj = joblib.load(path)
        self.models, self.scaler, self.weights = obj["models"], obj["scaler"], obj["weights"]

def send_alert(flow_data):
    try:
        requests.post(DMCM_ENDPOINT, json=flow_data, timeout=0.3)
    except Exception as e:
        print(f"[CAAWE] Mitigation dispatch failed: {e}")

def main():
    data = pd.read_csv("detection/data/PASD.csv")
    X = data.drop(columns=["label"])
    y = data["label"]
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=42)

    ensemble = CAAWEEnsemble()
    ensemble.fit(X_train, y_train)
    y_pred, confs = ensemble.predict(X_val)

    print(f"Accuracy: {accuracy_score(y_val, y_pred):.3f}")
    print(f"F1: {f1_score(y_val, y_pred):.3f}")
    ensemble.update_weights(X_val, y_val)
    ensemble.save()

    # Send alerts for detected SQLi flows
    for i, pred in enumerate(y_pred):
        if pred == 1:  # attack
            flow_info = {"flow_src": f"h{i}", "flow_dst": f"s{i}", "timestamp": time.time()}
            send_alert(flow_info)

if __name__ == "__main__":
    main()
