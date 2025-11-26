from sklearn.tree import DecisionTreeClassifier
import numpy as np

class DecisionTreeModel:
    def __init__(self, max_depth=None):
        self.model = DecisionTreeClassifier(max_depth=max_depth)

    def fit(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        preds = self.model.predict(X)
        conf = np.ones_like(preds, dtype=float) * 0.85
        return preds, conf
