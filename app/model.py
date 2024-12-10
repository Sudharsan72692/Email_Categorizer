from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import joblib

def train_model(X, y):
    model = MultinomialNB()
    model.fit(X, y)
    return model

def save_model(model, vectorizer, model_path, vectorizer_path):
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    report = classification_report(y_test, predictions)
    print(report)
