import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import joblib

def load_dataset(filepath):
    data = pd.read_csv(filepath)
    X = data['Message'] 
    y = data['Category']
    return X, y

def preprocess_data(X, y):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X_tfidf = vectorizer.fit_transform(X)
    return X_tfidf, y, vectorizer

def train_model(X, y):
    model = MultinomialNB()
    model.fit(X, y)
    return model

def save_artifacts(model, vectorizer, model_path, vectorizer_path):
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)

if __name__ == "__main__":
    dataset_path = 'dataset/augmented_mail_5000.csv'
    model_path = 'models/trained_model.pkl'
    vectorizer_path = 'models/vectorizer.pkl'
    X, y = load_dataset(dataset_path)

    X_tfidf, y, vectorizer = preprocess_data(X, y)

    X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

    model = train_model(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    save_artifacts(model, vectorizer, model_path, vectorizer_path)
    print(f"Model saved to {model_path}")
    print(f"Vectorizer saved to {vectorizer_path}")
