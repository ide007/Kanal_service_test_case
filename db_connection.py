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
connection = create_connection('postgres', 'postgres', 'admin',
                               '127.0.0.1', '5432')


drop_db_if_exists = 'DROP DATABASE IF EXISTS kanal_service'
create_database(connection, drop_db_if_exists)
create_database_query = 'CREATE DATABASE kanal_service'
create_database(connection, create_database_query)
connection = create_connection('kanal_service', 'postgres', 'admin',
                               '127.0.0.1', '5432')

# создание таблицы
create_table_query = 'CREATE TABLE IF NOT EXISTS public.test_data' \
                     '(id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ' \
                     '(INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 10000 CACHE 1),' \
                     'num text NOT NULL, ' \
                     'order_num text NOT NULL, ' \
                     'order_cost_us text NOT NULL, ' \
                     'delivery_date text NOT NULL,' \
                     'order_cost_ru text, ' \
                     'CONSTRAINT test_data_pkey PRIMARY KEY (id)) ' \
                     'TABLESPACE pg_default; ' \
                     'ALTER TABLE IF EXISTS public.test_data ' \
                     'OWNER to postgres;'
create_database(connection, create_table_query)

# создаём список кортежей, для загрузки в БД
data = [tuple(i) for i in get_data.main()]
data_records = ", ".join(["%s"] * len(data))

insert_query = (
    f'INSERT INTO test_data (num, order_num, order_cost_us, delivery_date,'
    f' order_cost_ru) VALUES {data_records}'
)

# загружаем данные в БД.
connection.autocommit = True
cur = connection.cursor()
cur.execute(insert_query, data)
