import os.path

from google.auth.transport.requests import Request
from google.oauth2 import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from shared.controllers.audited import AuditedModelController
from tickets.models import Incidencia

from flask import request
from flask.templating import render_template

from flask_login import login_required

from configuration import INDEX_URL
from shared.views import ListView
from shared.engine import session


INCIDENCE_DETAIL_URL = '/incidences/detail'

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


class IncidenceListView(ListView):

    decorators = [login_required]

    list_title = "Listado de Incidencias"
    page_title = "Incidencias"
    active_menu_item = "incidences"

    controller = IncidenceController(session)
    url = INDEX_URL

    def get_action_buttons_html(self) -> str:
        return render_template("incidence/action-buttons.html")

    def get_list_html(self):

        with_ticket = 'with_ticket' in request.args.keys()
        without_ticket = 'without_ticket' in request.args.keys()
        all_incidences = not (with_ticket or without_ticket)
        search_params = request.args.get('search')

        has_ticket = None
        filtering_args = []

        if not all_incidences:
            has_ticket = True if with_ticket else False

        if search_params:
            statement = Incidencia.AF_descripcion.ilike("%" + search_params + "%")
            filtering_args.append(statement)

        incidence_list = self.controller.filter(order_by='NU_incidencia', *filtering_args)
        
        if has_ticket is not None:
            incidence_list = tuple(filter(lambda i: i.has_ticket == has_ticket, incidence_list))
        
        if len(incidence_list) == 0:
            return None

        for incidence in incidence_list:
            incidence.TI_fecha_creacion = format(incidence.TI_fecha_creacion, r'%Y-%m-%d %H:%M')

        content = render_template(
            'incidence/list.html',
            incidences=incidence_list,
            incidence_detail_url=INCIDENCE_DETAIL_URL
        )

        return content






