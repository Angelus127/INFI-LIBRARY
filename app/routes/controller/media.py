from flask import Flask, Blueprint, session, request, render_template, redirect, url_for
from ...services.temp import temp_read, temp_cleanup
from app.db import conectar, dict_cursor
import os, json

media = Blueprint("media", __name__, template_folder='templates')

@media.route("/agregar/<string:media_id>", methods=["GET", "POST"])
def guardar_media(media_id):
    temp_file_name = session.get('media_cache_file')

    if temp_file_name and os.path.exists(temp_file_name):
        media_cache = temp_read(temp_file_name)

    media = media_cache.get(media_id)
    if not media:
        return "Elemento no encontrado en cache"

    tipo = "libro" if media.get("fuente") == "GoogleBooks" else (
        "anime" if media.get("episodios") else "manga"
    )

    if request.method == "POST":
        conn = conectar()
        cur = dict_cursor(conn)
        username = request.form["usuario"]
        puntuacion = request.form.get("puntuacion")
        estado = request.form["estado"]
        reseña = request.form.get("reseña")

        # Obtener ID del usuario
        cur.execute("SELECT id FROM usuario WHERE username = %s", (username,))
        usuario = cur.fetchone()
        if not usuario:
            return "Usuario no encontrado."
        usuario_id = usuario[0]

        # Insertar multimedia si no existe
        cur.execute("SELECT id FROM multimedia WHERE datos->>'id_api' = %s", (media_id,))
        existente = cur.fetchone()
        if existente:
            multimedia_id = existente[0]
        else:
            cur.execute(
                "INSERT INTO multimedia (tipo, datos) VALUES (%s, %s) RETURNING id",
                (tipo, json.dumps(media))
            )
            multimedia_id = cur.fetchone()[0]

        # Insertar relación usuario-multimedia
        cur.execute("""
            INSERT INTO usuario_multimedia (usuario_id, multimedia_id, puntuacion, estado, opinion)
            VALUES (%s, %s, %s, %s, %s);
        """, (usuario_id, multimedia_id, puntuacion, estado, reseña))
        conn.commit()
        temp_cleanup(temp_file_name)

        return redirect(url_for("buscar", tipo=tipo.upper()))

    return render_template("agregar.html", media=media, tipo=tipo)