"""
Feedback loop for model retraining based on false positives / false negatives.
"""
import pandas as pd
import joblib, os
from caawe_ensemble import CAAWEEnsemble

def retrain_with_feedback(new_data_path):
    new_data = pd.read_csv(new_data_path)
    X_new = new_data.drop(columns=["label"])
    y_new = new_data["label"]

    ensemble = CAAWEEnsemble()
    ensemble.load()
    ensemble.fit(X_new, y_new)
    ensemble.save()
    print(f"[Retraining] Ensemble updated with {len(new_data)} new samples.")

if __name__ == "__main__":
    retrain_with_feedback("detection/data/feedback_data.csv")
