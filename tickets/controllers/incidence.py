import os.path

from google.auth.transport.requests import Request
from google.oauth2 import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from shared.controllers.audited import AuditedModelController
from tickets.models import Incidencia

class IncidenceController(AuditedModelController[Incidencia]):
    
    model = Incidencia
    model_pk_field = 'NU_incidencia'


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class IncidenceSyncController:
    def __init__(self, credentials_file='credentials.json', token_file='token.json'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.creds = self._load_credentials()
        self.service = build('gmail', 'v1', credentials=self.creds)

    def _load_credentials(self):
        creds = None
        if os.path.exists(self.token_file):
            creds = credentials.Credentials.from_authorized_user_file(self.token_file, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_file, 'wb') as token:
                token.write(creds.to_json())
        return creds

    def get_inbox_messages(self, label_ids=['INBOX']):
        try:
            results = self.service.users().messages().list(userId='me',
                                                    labelIds=label_ids).execute()
            messages = results.get('messages', [])

            if not messages:
                print('No messages found.')
                return

            print('Messages:')
            for message in messages:
                msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
                print(msg['snippet'])

        except HttpError as error:
            print(f'An error occurred: {error}')





