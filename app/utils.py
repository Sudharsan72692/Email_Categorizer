def categorize_email(email_text, model, vectorizer):
    email_vectorized = vectorizer.transform([email_text])
    category = model.predict(email_vectorized)[0]
    return category
