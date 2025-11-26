"""
ASID Metrics Computation
------------------------
Utility functions to compute and export detection performance metrics.
"""

from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score
import json, os, numpy as np

def compute_metrics(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred),
        "confusion_matrix": cm.tolist()
    }
    return metrics

def export_metrics(metrics, path="experiments/performance_metrics.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"[Metrics] Exported results to {path}")

if __name__ == "__main__":
    # Example test
    y_true = [0, 1, 1, 0, 1]
    y_pred = [0, 1, 0, 0, 1]
    m = compute_metrics(y_true, y_pred)
    export_metrics(m)
