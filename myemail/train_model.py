import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import joblib

# Step 1: Load the dataset
def load_dataset(filepath):
    data = pd.read_csv(filepath)
    X = data['Message']  # Replace with the actual column name for email content
    y = data['Category']    # Replace with the actual column name for categories
    return X, y

# Step 2: Preprocess data
def preprocess_data(X, y):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X_tfidf = vectorizer.fit_transform(X)
    return X_tfidf, y, vectorizer

# Step 3: Train the model
def train_model(X, y):
    model = MultinomialNB()
    model.fit(X, y)
    return model

# Step 4: Save the model and vectorizer
def save_artifacts(model, vectorizer, model_path, vectorizer_path):
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)

# Main script
if __name__ == "__main__":
    dataset_path = 'dataset/augmented_mail_5000.csv'  # Path to your dataset
    model_path = 'models/trained_model.pkl'
    vectorizer_path = 'models/vectorizer.pkl'

    # Load and preprocess data
    X, y = load_dataset(dataset_path)
    X_tfidf, y, vectorizer = preprocess_data(X, y)

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

    # Train the model
    model = train_model(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Save the model and vectorizer
    save_artifacts(model, vectorizer, model_path, vectorizer_path)
    print(f"Model saved to {model_path}")
    print(f"Vectorizer saved to {vectorizer_path}")
