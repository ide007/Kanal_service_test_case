from pprint import pprint

from psycopg2 import OperationalError


import db_connection as db


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as err:
        print(f'The error {err} occured')


def main():
    select = 'SELECT * FROM test_data'
    connect = db.connection
    data = execute_read_query(connect, select)

    pprint(data)
    return data


if __name__ == '__main__':
    main()
