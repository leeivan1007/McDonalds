from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1xTpOMFn8VsmRwYoN0hw47NOmnmd1LEyWIfmJDFjHPU4'
SAMPLE_RANGE_NAME = 'test_for_automation!A1:Z50'


def check_auth():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def load_items_from_json_file(path=''):
    items = open('crawling/items.json')
    items = json.load(items)

    sorted_data = []
    for topic in items:
        batch_data = items[topic]
        names = []
        prices = []
        for key in batch_data:
            names.append(key)
            prices.append(batch_data[key])
        sorted_data.append(names)
        sorted_data.append(prices)

    body = {'values': sorted_data,
            'majorDimension': 'COLUMNS'}
    return body


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    credentials = check_auth()
    body = load_items_from_json_file('crawling/items.json')

    # Call the Sheets API
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
        valueInputOption='RAW', body=body).execute()


if __name__ == '__main__':
    main()
