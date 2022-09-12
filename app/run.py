"""
Модуль для чтения данных из БД.
"""
from pprint import pprint
from psycopg2 import OperationalError

import db_connection as db


def execute_read_query(connection, query):
    """
    Функция для выгрузки данных ид БД.
    :param connection: подключение к БД
    :param query: sql запрос
    :return: выборка согласно запросу в query
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except OperationalError as err:
        print(f'The error {err} occured')


def main():
    """
    Функция для запуска модуля. Возвращает все записи таблицы test_data.
    :return: data
    """
    select = 'SELECT * FROM test_data'
    connect = db.connection
    data = execute_read_query(connect, select)

    print("Data from db-postgres:")
    pprint(data)
    # return data


if __name__ == '__main__':
    main()
