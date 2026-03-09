from flask import Flask, Blueprint, url_for, render_template, request
from ..db import conectar, dict_cursor  
from app.formatters.json_formatter import format_json
from ..services.count import contador
from app.utils.auth import login_required

library = Blueprint("library", __name__, template_folder='templates')

@library.route("/biblioteca", methods=["GET", "POST"])
@login_required
def biblioteca():
    library = []
    tipo = 'libro'
    conn = conectar()
    cur = dict_cursor(conn)

    conteos = contador()

    if request.method == 'POST':
        try:
            titulo = request.form["title"]
            tipo = request.form["type"]
            orden = request.form["order"]
            estado = request.form["status"]

            sql = "SELECT * from multimediaView"
            condiciones = []
            parametros = []
            if titulo:
                condiciones.append("datos->>'titulo' ILIKE %s")
                parametros.append(f"%{titulo}%")

            if tipo:
                if tipo != "todos":
                    condiciones.append("tipo = %s")
                    parametros.append(tipo)
                else:
                    condiciones.append("1=1")
            
            if estado:
                condiciones.append("estado = %s")
                parametros.append(estado)

            if condiciones:
                sql += " WHERE " + " AND ".join(condiciones) 
                
            
            orden_sql = {
                'antiguos': " ORDER BY id ASC",
                'unpopular': " ORDER BY puntuacion ASC",
                'popular': " ORDER BY puntuacion DESC"
            }.get(orden, " ORDER BY id DESC")

            sql += orden_sql

            cur.execute(sql, parametros)
            info = cur.fetchall()
            library = format_json(info)
            return render_template(
                "biblioteca.html",
                library=library, 
                conteos=conteos, 
                orden=orden,
                tipo=tipo,
                estado=estado)
        except Exception as e:
            print("No se encontro registros: ", e)
            return render_template("error.html", e=e)
    else:
        try:
            cur.execute("SELECT * FROM multimediaView ORDER BY id DESC")
            info = cur.fetchall()
            library = format_json(info)
            return render_template("biblioteca.html", library=library, conteos=conteos)
        except Exception as e:
            print("No se encontro registros: ", e)
            return render_template("error.html", e=e)

@library.route("/biblioteca/<string:id>")
@login_required
def detalles(id):
    conn = conectar()
    cur = dict_cursor(conn)
    try:
        cur.execute("SELECT * FROM multimediaView WHERE id = %s", (id,))
        info = cur.fetchone()
    except Exception as e:
        return render_template('error.html', e=e)
        
    if not info[7]:
        info[7] = "-"
    
    media = {
        "id": info[0],
        "id_registro": info[1],
        "categoria": info[2],
        **info[3],
        "fecha_agregado": info[4],
        "puntaje": info[5],
        "estado_usuario": info[6],
        "opinion": info[7]
    }
    return render_template('detalles.html', media=media)
