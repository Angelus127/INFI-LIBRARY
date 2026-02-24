import psycopg2, psycopg2.extras
from app.config import Config

def conectar():
    try:
        return psycopg2.connect(Config.DATABASE_URL)
    except Exception as e:
        print("Error al conectar a la base de datos: ", e)
        return None 

def dict_cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)