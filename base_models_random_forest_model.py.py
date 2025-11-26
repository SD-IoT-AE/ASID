from sklearn.ensemble import RandomForestClassifier
import numpy as np

class RandomForestModel:
    def __init__(self, n_estimators=100, max_depth=None):
        self.model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)

    def fit(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        preds = self.model.predict(X)
        conf = np.ones_like(preds, dtype=float) * 0.9
        return preds, conf
