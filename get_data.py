"""
Данный модуль случит для получения данных из Гугл таблиц
"""
from pprint import pprint

import apiclient
import httplib2
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

import currency_rate as cr


def google_authorize(filename):
    """
    Функция для авторизации сервисного аккаунта гугл.
    :param file: json файл с данными для авторизации.
    :return: авторизованная сервисная учетная запись
    """
    CREDENTIALS_FILE = filename
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    return credentials.authorize(httplib2.Http())


def get_values(spreadsheet_id, filename):
    """
    Функция для получения данных с Google Sheets через Google API.
    :param spreadsheet_id: уникальный id документа.
    :return: данные всех колонок и строк документа,
             не зависимо от размера таблицы.
    """
    # получение доступа, через авторизацию учетной записи.
    http_auth = google_authorize(filename)

    try:
        service = apiclient.discovery.build('sheets', 'v4', http=http_auth)
        # запрос таблицы целиком.
        value = service.spreadsheets().values().batchGet(
            spreadsheetId=spreadsheet_id,
            ranges='Лист1',
            majorDimension='ROWS').execute()
        # фильтрация данных только из таблицы.
        return value.get('valueRanges')[0].get('values')
    # обработка ошибок.
    except HttpError as err:
        print(f'An error occurred: {err}')


def add_column(lst):
    """
    Функция для добавления данных с учетом курса валюты.
    :param lst: исходный список списков.
    :return: отредактированный список списков
    """
    # добавление названия колонки
    lst[0].append('стоимость в руб,\u20bd')
    # текущий курс валюты.
    curr_rate = float(cr.currency_rate())
    # вычисляем стоимость в рублях и добавляем данные в таблицу.
    for i in range(1, len(lst)):
        _ = f'{curr_rate * int(lst[i][2]):.{2}f}'
        lst[i].append(_)
    return lst


def main():
    """
    Функция для запуска модуля. Возвращает отредактированный список списков.
    :return: data
    """
    data = add_column(get_values(
        '1iEudEKROWhVjCkJQk1OdYpokrc8DL5iG4Zze_VCy8VE',
        'creds.json')
    )
    # pprint(data)
    return data


if __name__ == '__main__':
    main()
