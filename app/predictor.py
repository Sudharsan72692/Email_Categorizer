import joblib

def load_model(model_path, vectorizer_path):
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return model, vectorizer

def classify_emails(emails, model, vectorizer):
    email_texts = [email['body'] for email in emails]
    features = vectorizer.transform(email_texts)
    predictions = model.predict(features)
    return predictions
