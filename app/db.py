import psycopg2, psycopg2.extras
from .config import Config

def conectar():
    try:
        return psycopg2.connect(**Config.DB_CONFIG)
    except Exception as e:
        print("Error al conectar a la base de datos: ", e)
        return None 

def dict_cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)