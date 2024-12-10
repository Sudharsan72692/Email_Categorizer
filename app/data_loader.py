import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

def load_data(filepath):
    data = pd.read_csv(filepath)
    X = data['email_text']
    y = data['category']
    return X, y
def preprocess_data(X, y):
    tfidf_vectorizer=TfidfVectorizer(stop_words='english')
    X_tfidf = tfidf_vectorizer.fit_transform(X)
    return X_tfidf, y, tfidf_vectorizer
