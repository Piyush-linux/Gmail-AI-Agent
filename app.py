import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
from bs4 import BeautifulSoup
import base64
from datetime import datetime
from openai import OpenAI
client = OpenAI()

class GmailSummarizer:
    def __init__(self, credentials_path='credentials.json'):
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        self.credentials_path = credentials_path
        self.creds = None
        self.service = None
        
    def authenticate(self):
        """Handles the OAuth2 authentication flow."""
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('gmail', 'v1', credentials=self.creds)

    def get_recent_emails(self, max_results=10):
        """Fetches recent emails from Gmail."""
        try:
            results = self.service.users().messages().list(
                userId='me', maxResults=max_results, labelIds=['INBOX']
            ).execute()
            
            messages = results.get('messages', [])
            return messages
        except Exception as e:
            print(f"Error fetching emails: {e}")
            return []

    def get_email_content(self, msg_id):
        """Retrieves and processes the content of a specific email."""
        try:
            message = self.service.users().messages().get(
                userId='me', id=msg_id, format='full'
            ).execute()

            headers = message['payload']['headers']
            subject = next(h['value'] for h in headers if h['name'].lower() == 'subject')
            from_email = next(h['value'] for h in headers if h['name'].lower() == 'from')
            date = next(h['value'] for h in headers if h['name'].lower() == 'date')

            # Get email body
            if 'parts' in message['payload']:
                parts = message['payload']['parts']
                data = self._get_text_from_parts(parts)
            else:
                data = base64.urlsafe_b64decode(
                    message['payload']['body']['data']
                ).decode('utf-8')

            # Clean the text content
            if data:
                soup = BeautifulSoup(data, 'html.parser')
                clean_text = soup.get_text(separator=' ', strip=True)
            else:
                clean_text = "No content available"

            return {
                'subject': subject,
                'from': from_email,
                'date': date,
                'content': clean_text[:1000]  # Limit content length for summary
            }
        except Exception as e:
            print(f"Error processing email {msg_id}: {e}")
            return None

    def _get_text_from_parts(self, parts):
        """Recursively extracts text from email parts."""
        text = ""
        for part in parts:
            if part['mimeType'] == 'text/plain':
                if 'data' in part['body']:
                    text += base64.urlsafe_b64decode(
                        part['body']['data']
                    ).decode('utf-8')
            elif part['mimeType'] == 'text/html':
                if 'data' in part['body']:
                    text += base64.urlsafe_b64decode(
                        part['body']['data']
                    ).decode('utf-8')
            elif 'parts' in part:
                text += self._get_text_from_parts(part['parts'])
        return text

    def summarize_with_openai(self, text):
        """Generates a summary using OpenAI's API."""
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Please provide a brief summary of this email in one or two sentences."},
                    {"role": "user", "content": text}
                ],
                max_tokens=100
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Summary generation failed"

    def process_recent_emails(self):
        """Main function to process and summarize recent emails."""
        self.authenticate()
        messages = self.get_recent_emails()
        
        summaries = []
        for msg in messages:
            email_data = self.get_email_content(msg['id'])
            if email_data:
                summary = self.summarize_with_openai(email_data['content'])
                summaries.append({
                    'subject': email_data['subject'],
                    'from': email_data['from'],
                    'date': email_data['date'],
                    'summary': summary
                })
        
        return summaries

def main():
    # Set your OpenAI API key
    # openai.api_key = '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'
    
    # Initialize and run the summarizer
    summarizer = GmailSummarizer()
    email_summaries = summarizer.process_recent_emails()
    
    # Print the summaries
    print("\nEmail Summaries:")
    print("===============")
    for i, summary in enumerate(email_summaries, 1):
        print(f"\n{i}. Subject: {summary['subject']}")
        print(f"From: {summary['from']}")
        print(f"Date: {summary['date']}")
        print(f"Summary: {summary['summary']}")
        print("-" * 80)

if __name__ == "__main__":
    main()