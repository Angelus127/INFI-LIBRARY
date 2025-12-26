from flask import Flask, Blueprint, url_for, render_template, request
from ..db import conectar, dict_cursor 
from ..services.format import format_json

library = Blueprint("library", __name__, template_folder='templates')

@library.route("/biblioteca", methods=["GET", "POST"])
def biblioteca():
    library = []
    tipo = 'libro'
    conn = conectar()
    cur = dict_cursor(conn)

    if request.method == 'POST':
        try:
            titulo = request.form["title"]
            tipo = request.form["type"]

            sql = "SELECT * from multimedia"
            condiciones = []
            parametros = []
            if titulo:
                condiciones.append("datos->>'titulo' ILIKE %s")
                parametros.append(f"%{titulo}%")

            if tipo:
                condiciones.append("tipo = %s")
                parametros.append(tipo)

            if condiciones:
                sql += " WHERE " + " AND ".join(condiciones)
            
            sql += "ORDER BY id DESC"

            cur.execute(sql, parametros)
            info = cur.fetchall()
            library = format_json(info)
            return render_template("biblioteca.html", library=library)
        except Exception as e:
            print("No se encontro registros: ", e)
            return render_template("error.html", e=e)
    else:
        try:
            cur.execute("SELECT * FROM multimedia ORDER BY id DESC")
            info = cur.fetchall()
            library = format_json(info)
            return render_template("biblioteca.html", library=library)
        except Exception as e:
            print("No se encontro registros: ", e)
            return render_template("error.html", e=e)

@library.route("/biblioteca/<string:id>")
def detalles(id):
    conn = conectar()
    cur = dict_cursor(conn)
    try:
        cur.execute("SELECT * FROM multimedia WHERE id = %s", (id,))
        info = cur.fetchone()
    except Exception as e:
        return render_template('error.html', e=e)
    
    try:
        cur.execute("SELECT * FROM usuario_multimedia WHERE multimedia_id = %s", (id,))
        user_info = cur.fetchone()
    except Exception as e:
        return render_template('error.html', e=e)
    
    media = {
        "id": info[0],
        "categoria": info[1],
        **info[2],
        "fecha_agregado": info[3],
        "puntuacion": user_info[3],
        "estado_usuario": user_info[4],
        "opinion": user_info[5]
    }
    return render_template('detalles.html', media=media)
