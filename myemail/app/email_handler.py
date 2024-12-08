import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import email.utils

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def fetch_emails(email_id, password, n=5):
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])
    if not messages:
        print("No new messages.")
    else:
        emails = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_data = msg['payload']['headers']
            subject = None
            from_name = None
            from_email = None
            # Extract subject and sender information
            for values in email_data:
                name = values['name']
                if name == 'From':
                    from_name, from_email = parse_sender(values['value'])
                if name == 'Subject':
                    subject = values['value']
            try:
                # Decode the email body
                data = msg['payload']['body']["data"]
                byte_code = base64.urlsafe_b64decode(data)
                body = byte_code.decode("utf-8")
                emails.append({'subject': subject, 'sender_name': from_name, 'sender_email': from_email, 'body': body})
            except BaseException as error:
                print(f"Error: {error}")
        return emails

def parse_sender(sender):
    # Parse sender's name and email address
    name, email_address = email.utils.parseaddr(sender)
    return name, email_address
