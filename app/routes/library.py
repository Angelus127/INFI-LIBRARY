from flask import Flask, Blueprint,jsonify
from ..db import conectar, dict_cursor 

library = Blueprint("library", __name__, template_folder='templates')

@library.route("/biblioteca")
def biblioteca():
    library = []
    conn = conectar()
    cur = dict_cursor(conn)
    try:
        cur.execute("SELECT * FROM multimedia")
        info = cur.fetchall()
        for fila in info:
            library.append({
                "id": fila[0],
                "categoria": fila[1],
                **fila[2],
                "fecha_agregado": fila[3]
            })
        return jsonify(library)
    except Exception as e:
        print("No se encontro registros: ", e)
        return jsonify({"error": "No se encontraron registros"}), 500