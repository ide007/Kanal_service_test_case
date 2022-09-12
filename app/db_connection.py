"""
Модуль для работы с базой данных. Создает подключение к БД, создает свою БД, а
также таблицу для хранения данных.
"""
import psycopg2
from psycopg2 import OperationalError

import get_data


def create_connection(db_name, db_user, db_pass, db_host, db_port):
    """
    Функция для создания подключения к БД PostgreSQL.
    :param db_name: имя БД по умолчанию
    :param db_user: логин пользователя
    :param db_pass: пароль пользователя
    :param db_host: хост БД
    :param db_port: порт БД
    :return:
    """
    connection_to_db = None
    try:
        connection_to_db = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port
        )
        print(f'Connecting to database {db_name} successfully.')
    except OperationalError as err:
        print(f'Connecting to database {db_name} failed with error: {err}')

    return connection_to_db


def create_database(connect_to_db, query):
    """
    Функция для работы с БД, выполнения команд SQL.
    :param connect_to_db: подключение к БД.
    :param query: команды(скрипт) на языке SQL.
    :return: результат выполнения команд.
    """
    connect_to_db.autocommit = True
    # инициализация курсора
    cursor = connect_to_db.cursor()
    try:
        cursor.execute(query)
        print(f"{query} executed successfully")
    except OperationalError as err:
        print(f"The error '{err}' occurred")

# инициализация подключения к БД.
connection = create_connection('postgres',
                               'postgres',
                               'admin',
                               'db',
                               '5432')

# сброс таблицы в случаи повторного использования.
drop_table_if_exists = 'DROP TABLE IF EXISTS public.test_data'
create_database(connection, drop_table_if_exists)
# получение названия столбцов для создания таблицы.
data = [tuple(i) for i in get_data.main()]
columns = data[0]
data = data[1:]
# создание таблицы
create_table_query = f'CREATE TABLE IF NOT EXISTS public.test_data' \
                     f'(id smallserial PRIMARY KEY,' \
                     f'"{columns[0]}"  smallserial NOT NULL, ' \
                     f'"{columns[1]}" int NOT NULL, ' \
                     f'"{columns[2]}" int NOT NULL, ' \
                     f'"{columns[3]}" text  NOT NULL,' \
                     f'"{columns[4]}" real NOT NULL) ' \
                     f'TABLESPACE pg_default; ' \
                     f'ALTER TABLE IF EXISTS public.test_data ' \
                     f'OWNER to postgres;'
create_database(connection, create_table_query)

# создаём список кортежей, для загрузки в БД
data_records = ", ".join(["%s"] * len(data))

insert_query = (
    f'INSERT INTO test_data ("{columns[0]}", "{columns[1]}", "{columns[2]}", '
    f'"{columns[3]}", "{columns[4]}") VALUES {data_records}'
)

# загружаем данные в БД.
connection.autocommit = True
cur = connection.cursor()
cur.execute(insert_query, data)
