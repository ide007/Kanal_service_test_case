from pprint import pprint

import apiclient
import httplib2
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

import currency_rate as cr


def google_authorize(filename):
    CREDENTIALS_FILE = filename
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    return credentials.google_authorize(httplib2.Http())


def add_column(lst):
    lst[0].append('стоимость,\u20bd')
    for i in range(1, len(lst)):
        lst[i].append(cr.currency_rate(int(lst[i][2])))
    return lst


def get_values(spreadsheet_id):

    spreadsheet_id = spreadsheet_id
    http_auth = google_authorize('creds.json')

    try:
        service = apiclient.discovery.build('sheets', 'v4', http=http_auth)
        value = service.spreadsheets().values().batchGet(
            spreadsheetId=spreadsheet_id,
            ranges='Лист1',
            majorDimension='ROWS').execute()
        return value.get('valueRanges')[0].get('values')
    except HttpError as err:
        print(f'An error occurred: {err}')


if __name__ == '__main__':
    data = get_values('1iEudEKROWhVjCkJQk1OdYpokrc8DL5iG4Zze_VCy8VE')
    new = add_column(data)
    pprint(new)
