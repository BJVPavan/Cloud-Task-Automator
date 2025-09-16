import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    creds = None
    # Load existing token
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token_file:
            creds = pickle.load(token_file)
    # If no valid credentials, login
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=61658)
        with open('token.pkl', 'wb') as token_file:
            pickle.dump(creds, token_file)
    service = build('gmail', 'v1', credentials=creds)
    return service

def list_unread_emails():
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
    messages = results.get('messages', [])
    email_list = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        snippet = msg_data.get('snippet', '')
        email_list.append({'id': msg['id'], 'snippet': snippet})
    
    return email_list

def mark_email_as_read(email_id):
    service = get_gmail_service()
    service.users().messages().modify(
        userId='me',
        id=email_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()
