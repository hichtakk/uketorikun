import httplib2
import os
from datetime import datetime
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from slackbot_settings import SCOPES, SPREADSHEET_ID, SA_CREDENTIAL_PATH


def write_package_info(reporter, addressee, deliverer, image_url):
    # Service Account
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SA_CREDENTIAL_PATH, SCOPES)
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    rangeName = 'A3:C3'
    body = {
        'values': ['', str(datetime.now()), reporter, '', addressee, '', '', deliverer, '', '', '', '', image_url],
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID, range=rangeName,
        valueInputOption='USER_ENTERED', body=body).execute()
