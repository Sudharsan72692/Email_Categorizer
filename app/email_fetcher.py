import imaplib
import email

def connect_to_email(email_id, password, server='imap.gmail.com'):
    mail = imaplib.IMAP4_SSL(server)
    mail.login(email_id, password)
    return mail

def fetch_emails(mail, mailbox='inbox', limit=10):
    mail.select(mailbox)
    result, data = mail.search(None, 'ALL')
    email_ids = data[0].split()[-limit:]
    emails = []

    for e_id in email_ids:
        result, msg_data = mail.fetch(e_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = msg['subject']
                body = get_email_body(msg)
                emails.append({'subject': subject, 'body': body})
    return emails

def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()
