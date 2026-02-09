from flask import Blueprint, session, request, render_template, redirect, url_for
from app.cache.cache import cache
from app.services.genres_service import display_genre
from app.utils.auth import login_required
from app.db import conectar, dict_cursor
import json

media = Blueprint("media", __name__, template_folder='templates')

@media.route("/agregar/<string:media_id>", methods=["GET", "POST"])
@login_required
def guardar(media_id):
    media = cache.get(media_id)

    if not media:
        return "Elemento no encontrado en cache"
    
    tipo = media.get("type", "").lower()
        
    if request.method == "POST":
        conn = conectar()
        cur = dict_cursor(conn)

        username = session["username"]
        puntuacion = request.form.get("puntuacion")
        estado = request.form["estado"]
        titulo = request.form.get("title")
        reseña = request.form.get("reseña")

        if titulo:
            media["titulo"] = titulo

        generos = request.form.getlist("generos")
        if generos:
            media["generos"] = generos

        cur.execute(
            "SELECT id FROM usuario WHERE username = %s",
            (username,)
        )
        usuario = cur.fetchone()

        if not usuario:
            return "Usuario no encontrado."
        
        usuario_id = usuario[0]

        cur.execute(
            "SELECT id FROM multimedia WHERE datos->>'id_api' = %s",
            (media_id,)
        )
        existente = cur.fetchone()

        if existente:
            multimedia_id = existente[0]
        else:
            cur.execute(
                "INSERT INTO multimedia (tipo, datos) VALUES (%s, %s) RETURNING id",
                (tipo, json.dumps(media))
            )
            multimedia_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO usuario_multimedia 
            (usuario_id, multimedia_id, puntuacion, estado, opinion)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (usuario_id, multimedia_id, puntuacion, estado, reseña)
        )

        conn.commit()

        return redirect(url_for("search.buscar", tipo=tipo.upper()))

    return render_template(
        "agregar.html", 
        media=media, 
        tipo=tipo,
         generos=list(display_genre())
    )

@media.route("/actualizar/<string:media_id>", methods=["GET", "POST"])
@login_required
def actualizar(media_id):
    media = cache.get(media_id)

    if not media:
        return "Elemento no encontrado en cache"
    
    if request.method == "POST":
        conn = conectar()
        cur = dict_cursor(conn)

        multimedia_id = request.form["id"]
        titulo = request.form["title"]

        if titulo:
            media["titulo"] = titulo
        
        generos = request.form.getlist("generos")
        if generos:
            media["generos"] = generos
        
        cur.execute(
            "UPDATE multimedia SET datos = %s WHERE id = %s", 
            (json.dumps(media), id)
        )
        conn.commit()

        return redirect(url_for("search.buscar"))

    return render_template(
        "actualizar.html", 
        media=media, 
        generos=display_genre()
    )


@media.route("/eliminar/<string:media_id>", methods=["GET", "POST"])
@login_required
def eliminar(media_id):
    conn = conectar()
    if conn: 
        cur = dict_cursor(conn)
        try:
            cur.execute("DELETE FROM multimedia WHERE id = %s", (media_id,))
            conn.commit()
        except Exception as e:
            print("No se encontro registros: ", e)
            return render_template("error.html", e=e)

    return redirect(url_for("library.biblioteca"))

    