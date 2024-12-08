
# MYEMAIL: Email Categorizer & Composer

A Streamlit-based application for categorizing emails into predefined categories and composing new ones. The project uses machine learning to categorize emails and allows users to send emails directly from the app.

---

## **Features**

- **Email Categorization**: Classifies emails into categories like inbox, personal, work, education, spam, etc.
- **Compose and Send Emails**: Provides a user-friendly interface to compose and send emails.
- **Automatic Email Fetching**: Periodically fetches new emails from the user's Gmail account.
- **Refresh Option**: A button to refresh and view new emails received after the first fetch.

---

## **Installation**

### 1. **Clone the Repository**
```bash
git clone <repository_url>
cd myemail
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## **Setup**

### 1. **Gmail Configuration**

- Enable IMAP for your Gmail account:
  - Go to Gmail settings -> See all settings -> Forwarding and POP/IMAP -> Enable IMAP.
- Generate an **App Password**:
  - Go to your Google Account -> Security -> App Passwords -> Generate a password for the application.

### 2. **Credentials**
- Update the `config/credentials.json` file with your email credentials.

Example:
```json
{
  "email": "your_email@gmail.com",
  "app_password": "your_app_password"
}
```

---

## **Usage**

### 1. **Run the Application**
```bash
streamlit run app/app.py
```

### 2. **Features in the Application**
- **Login**: Use your Gmail credentials to log in.
- **Categorize Emails**: View categorized emails in predefined tabs.
- **Compose Emails**: Use the floating pencil button to compose and send emails.
- **Auto-Fetch**: Automatically fetches emails every minute when logged in.
- **Refresh Emails**: Click the refresh button to load newly received emails.

---

## **Folder Structure**
```
MYEMAIL/
├── app/
│   ├── app.py                  # Main Streamlit application
│   ├── email_fetcher.py        # Fetches emails via IMAP
│   ├── email_handler.py        # Processes email content
│   ├── predictor.py            # ML model prediction
│   ├── utils.py                # Utility functions
│   └── model.py                # Handles ML model loading
├── models/
│   ├── trained_model.pkl       # Pre-trained categorization model
│   └── vectorizer.pkl          # Vectorizer for text data
├── config/
│   ├── credentials.json        # Email credentials
│   └── token.json              # Authentication tokens
├── training/
│   ├── train_model.py          # Model training script
│   └── augmented_mail_5000.csv # Training dataset
└── requirements.txt            # Python dependencies
```

---

## **Dependencies**
- `Streamlit`: For the web interface
- `scikit-learn`: For machine learning model handling
- `beautifulsoup4`: For parsing email content
- `smtplib`: For sending emails
- `imaplib`: For fetching emails

Install all dependencies using the `requirements.txt` file.

---

## **Demo**
- Watch the [Demo.mp4](Demo.mp4) file for a walkthrough of the application.

---

## **Future Enhancements**
- Add support for additional email providers.
- Improve categorization accuracy with advanced ML models.
- Add scheduling features for sending emails.

---

## **License**
This project is open-source and available under the MIT License.

---

## **Contact**
For questions or contributions, please contact **[Your Email/Name]**.
