from sklearn.neighbors import KNeighborsClassifier
import numpy as np

class KNNModel:
    def __init__(self, n_neighbors=5):
        self.model = KNeighborsClassifier(n_neighbors=n_neighbors)

    def fit(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        preds = self.model.predict(X)
        conf = np.ones_like(preds, dtype=float) * 0.8
        return preds, conf
