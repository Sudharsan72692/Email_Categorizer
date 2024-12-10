import streamlit as st
import joblib
from utils import categorize_email
from email_handler import fetch_emails
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

model = joblib.load('models/trained_model.pkl')
vectorizer = joblib.load('models/vectorizer.pkl')

def clean_email_body(body):

    soup = BeautifulSoup(body, "html.parser")
    return soup.get_text(strip=True)

if "fetched_emails" not in st.session_state:
    st.session_state["fetched_emails"] = None
    st.session_state["categorized_emails"] = None

st.title("Email Categorizer & Composer")
st.write("Categorize your emails into predefined categories and compose new ones.")

email_text = st.text_area("Paste the email content here:")

if st.button("Categorize Email"):
    if email_text.strip():
        category = categorize_email(email_text, model, vectorizer)
        st.write(f"**Predicted Category:** {category}")
    else:
        st.error("Please enter email content.")

st.header("Fetch and Categorize Emails")
email_id = st.text_input("Enter your email ID:")
email_password = st.text_input("Enter your password:", type="password")

if st.button("Fetch Emails"):
    with st.spinner("Fetching and categorizing emails..."):
        if email_id and email_password:
            try:
                # Fetch emails
                emails = fetch_emails(email_id, email_password)

                if not emails:
                    st.error("No emails retrieved or invalid credentials.")
                else:
                    # Categorize emails
                    predictions = [categorize_email(email['body'], model, vectorizer).lower() for email in emails]

                    # Define categories (all in lowercase to match predictions)
                    categories = ["inbox", "personal", "education", "entertainment", "work", "spam"]
                    categorized_emails = {cat: [] for cat in categories}

                    # Categorize emails into respective lists
                    for email, category in zip(emails, predictions):
                        # Clean the email body for display
                        email['body'] = clean_email_body(email['body'])

                        # Add to Inbox
                        categorized_emails["inbox"].append({**email, "category": category})
                        # Add to predicted category if valid
                        if category in categories and category != "inbox":
                            categorized_emails[category].append({**email, "category": category})

                    # Save fetched emails in session state
                    st.session_state["fetched_emails"] = emails
                    st.session_state["categorized_emails"] = categorized_emails

                    st.success("Emails fetched and categorized successfully!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("Please enter email credentials.")

if st.session_state["categorized_emails"]:
    st.header("Categorized Emails")
    categories = ["inbox", "personal", "education", "entertainment", "work", "spam"]
    tabs = st.tabs([cat.capitalize() for cat in categories])  # Capitalize tab titles

    for tab, category in zip(tabs, categories):
        with tab:
            st.header(f"{category.capitalize()} Emails")
            emails_to_display = st.session_state["categorized_emails"][category]
            if emails_to_display:
                for email in emails_to_display:
                    # Use sender name and email as the expander title
                    sender_info = f"{email['sender_name']} <{email['sender_email']}>"
                    with st.expander(f"**From:** {sender_info}"):
                        st.write(f"**Email ID:** {email['sender_email']}")
                        st.write(f"**Name:** {email['sender_name']}")
                        st.write(f"**Category:** {email['category']}")
                        st.write(f"**Subject:** {email['subject']}")
                        st.write(f"**Body:**\n{email['body']}")
                        st.write("---")
            else:
                st.write(f"No emails found in {category.capitalize()} category.")

st.header("Compose & Send Email")

recipient_email = st.text_input("Recipient Email:")
subject = st.text_input("Subject:")
message_body = st.text_area("Message Body:")

if st.button("Send Email"):
    if email_id and email_password and recipient_email and subject.strip() and message_body.strip():
        try:
            smtp_server = "smtp.gmail.com"  
            smtp_port = 587
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  
                server.login(email_id, email_password)

                msg = MIMEMultipart()
                msg["From"] = email_id
                msg["To"] = recipient_email
                msg["Subject"] = subject
                msg.attach(MIMEText(message_body, "plain"))

                server.sendmail(email_id, recipient_email, msg.as_string())
                st.success("Email sent successfully!")
        except Exception as e:
            st.error(f"Failed to send email: {str(e)}")
    else:
        st.error("Please fill out all fields and ensure credentials are provided.")
