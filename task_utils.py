from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def list_unread_emails():
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])
    detailed_msgs = []
    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id']).execute()
        snippet = m.get('snippet', '')
        detailed_msgs.append({'id': msg['id'], 'snippet': snippet})
    return detailed_msgs

def mark_email_as_read(msg_id):
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()

# Minimal ML-based ranking simulation for demo
def rank_tasks(tasks):
    # Simple scoring: longer snippet = higher priority
    for task in tasks:
        task['score'] = len(task['snippet'])
    ranked = sorted(tasks, key=lambda x: x['score'], reverse=True)
    return ranked
