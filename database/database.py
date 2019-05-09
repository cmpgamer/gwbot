import psycopg2
from psycopg2.extras import DictCursor


def create_connection(database: str, username: str, password: str, host: str = 'localhost',
                      port: str = '5432') -> psycopg2._psycopg.connection:
    connection = psycopg2.connect(dbname=database.lower(), user=username, password=password, host=host, port=port)
    connection.cursor_factory = DictCursor
    return connection
