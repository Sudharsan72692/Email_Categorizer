def categorize_email(email_text, model, vectorizer):
    # Preprocess the email text
    email_vectorized = vectorizer.transform([email_text])
    # Predict category
    category = model.predict(email_vectorized)[0]
    return category
