import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import email.utils

# Add send scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    """Force new authentication flow each time"""
    try:
        # Remove existing token if present
        if os.path.exists('token.json'):
            os.remove('token.json')
            
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        
        # Optionally save token temporarily
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
        return creds
    except Exception as e:
        print(f"Authentication failed: {e}")
        return None

def fetch_emails(email_id=None, password=None, n=5):
    """Removed unused parameters, added better error handling"""
    creds = authenticate_gmail()
    if not creds:
        return None
        
    try:
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages', [])
        
        if not messages:
            print("No new messages.")
            return []
            
        emails = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_data = msg['payload']['headers']
            subject = None
            from_name = None 
            from_email = None
            
            for values in email_data:
                name = values['name']
                if name == 'From':
                    from_name, from_email = parse_sender(values['value'])
                if name == 'Subject':
                    subject = values['value']
                    
            try:
                data = msg['payload']['body']["data"]
                byte_code = base64.urlsafe_b64decode(data)
                body = byte_code.decode("utf-8")
                emails.append({
                    'subject': subject,
                    'sender_name': from_name,
                    'sender_email': from_email,
                    'body': body
                })
            except Exception as error:
                print(f"Error processing message: {error}")
                
        return emails
        
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return None

def parse_sender(sender):
    name, email_address = email.utils.parseaddr(sender)
    return name, email_address