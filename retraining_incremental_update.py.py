"""
Incremental learning: updates ensemble weights periodically from validation logs.
"""
from caawe_ensemble import CAAWEEnsemble
import pandas as pd

def incremental_update():
    val_data = pd.read_csv("detection/data/validation_set.csv")
    X = val_data.drop(columns=["label"])
    y = val_data["label"]
    ensemble = CAAWEEnsemble()
    ensemble.load()
    ensemble.update_weights(X, y)
    ensemble.save()
    print("[IncrementalUpdate] Weights adjusted based on validation set.")

if __name__ == "__main__":
    incremental_update()
