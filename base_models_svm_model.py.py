from sklearn.svm import SVC
import numpy as np

class SVMModel:
    def __init__(self, kernel='rbf', C=1.0):
        self.model = SVC(kernel=kernel, C=C, probability=True)

    def fit(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        preds = self.model.predict(X)
        probs = self.model.predict_proba(X)
        conf = probs.max(axis=1)
        return preds, conf
