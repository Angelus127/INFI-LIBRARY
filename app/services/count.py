from ..db import conectar, dict_cursor

conn = conectar()
cur = dict_cursor(conn)

def contador():
    cur.execute(f"SELECT tipo, COUNT(*) AS count FROM multimedia GROUP BY tipo")
    conteos_raw = cur.fetchall()
    conteos = {fila['tipo']: fila['count'] for fila in conteos_raw}
    cur.execute(f"SELECT COUNT(*) FROM multimedia")
    conteos['total'] = cur.fetchone()['count']
    return conteos