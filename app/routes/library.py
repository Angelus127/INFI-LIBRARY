from flask import Flask, Blueprint, url_for, render_template, request
from ..db import conectar, dict_cursor  
from app.formatters.json_formatter import format_json
from ..services.count import contador
from app.utils.auth import login_required
from app.utils.utils import construccion_sql
import math

library = Blueprint("library", __name__, template_folder='templates')

@library.route("/biblioteca", methods=["GET", "POST"])
@login_required
def biblioteca():
    library = []
    tipo = 'libro'
    conn = conectar()
    cur = dict_cursor(conn)

    conteos = contador()

    titulo = request.args.get("title")
    tipo = request.args.get("type")
    orden = request.args.get("order", "id")
    estado = request.args.get("status")
    page = request.args.get("page", 1, type=int)
    limite = 20
    window = 2
    offset = (page - 1) * limite

    try:
        sql = "SELECT * FROM multimediaView"
        query, parametros = construccion_sql(sql, False, titulo, tipo, estado, orden, limite, offset)
        cur.execute(query, parametros)
        info = cur.fetchall()
        library = format_json(info)

        query, parametros = construccion_sql(sql, True, titulo, tipo, estado)
        query_count = query.replace("SELECT *", "SELECT COUNT(*)")

        cur.execute(query_count, parametros)
        total_items = cur.fetchone()[0]
        total_pages = math.ceil(total_items / limite)

        start_page = max(1, page - window)
        end_page = min(total_pages, page + window)

        return render_template(
            "biblioteca.html",
            titulo=titulo,
            library=library, 
            conteos=conteos, 
            orden=orden,
            tipo=tipo,
            estado=estado,
            page=page,
            total_pages=total_pages,
            start_page=start_page,
            end_page=end_page
        )
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
