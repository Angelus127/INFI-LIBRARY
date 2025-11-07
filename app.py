from flask import Flask, render_template, request, redirect, url_for
import psycopg2, requests, json

app = Flask(__name__)
app.secret_key = "infinity-core"

# --- CONEXIÓN A BASE DE DATOS ---
conn = psycopg2.connect(
    dbname="infinitelibrary",
    user="postgres",
    password="cataleya",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Cache temporal
media_cache = {}

# -------- FUNCIONES AUXILIARES -------- #

def formatear_libro(item):
    """Limpia y estructura los datos de Google Books."""
    info = item.get("volumeInfo", {})
    imagen = info.get("imageLinks", {}).get("thumbnail", "")
    isbn = ""
    for i in info.get("industryIdentifiers", []):
        if i.get("type") == "ISBN_13":
            isbn = i.get("identifier")
            break

    return {
        "id_api": item.get("id"),
        "titulo": info.get("title"),
        "autores": info.get("authors", []),
        "isbn": isbn,
        "generos": info.get("categories", []),
        "paginas": info.get("pageCount"),
        "portada": imagen,
        "resumen": info.get("description", ""),
        "anio": info.get("publishedDate", ""),
        "fuente": "GoogleBooks"
    }

def formatear_media_anilist(item):
    """Limpia y estructura los datos de AniList."""
    title = item.get("title", {})
    return {
        "id_api": item.get("id"),
        "titulo": title.get("romaji") or title.get("english") or title.get("native"),
        "portada": item.get("coverImage", {}).get("large"),
        "descripcion": item.get("description", ""),
        "puntuacion_media": item.get("averageScore"),
        "episodios": item.get("episodes"),
        "volumenes": item.get("volumes"),
        "capitulos": item.get("chapters"),
        "generos": item.get("genres", []),
        "estado": item.get("status"),
        "formato": item.get("format"),
        "temporada": item.get("season"),
        "anio": item.get("seasonYear"),
        "duracion": item.get("duration"),
        "fuente": "AniList"
    }

# -------- RUTAS -------- #

@app.route("/", methods=["GET", "POST"])
def buscar():
    tipo = request.args.get("tipo", "LIBRO")  # LIBRO, ANIME o MANGA
    resultados = None

    if request.method == "POST":
        titulo = request.form["titulo"]
        tipo = request.form.get("tipo", "LIBRO").upper()

        if tipo == "LIBRO":
            query = f"intitle:{titulo}+subject:fiction|novel"
            url = f"https://www.googleapis.com/books/v1/volumes?q={query}&printType=books&maxResults=10"
            res = requests.get(url).json()
            items = res.get("items", [])
            resultados = [formatear_libro(i) for i in items]
        else:
            query = '''
            query ($search: String, $type: MediaType) {
                Page(perPage: 10) {
                    media(search: $search, type: $type) {
                        id
                        title { romaji english native }
                        coverImage { large }
                        description
                        averageScore
                        episodes
                        volumes
                        chapters
                        genres
                        status
                        format
                        season
                        seasonYear
                        duration
                    }
                }
            }
            '''
            variables = {"search": titulo, "type": tipo}
            res = requests.post("https://graphql.anilist.co", json={"query": query, "variables": variables}).json()
            items = res["data"]["Page"]["media"]
            resultados = [formatear_media_anilist(i) for i in items]

        # Cache local
        for item in resultados:
            media_cache[str(item["id_api"])] = item


    return render_template("buscar.html", resultados=resultados, tipo=tipo)


@app.route("/detalles/<string:media_id>", methods=["GET", "POST"])
def detalles(media_id):
    media = media_cache.get(media_id)
    if not media:
        return "Elemento no encontrado en caché. Realiza una búsqueda nuevamente."

    tipo = "libro" if media.get("fuente") == "GoogleBooks" else (
        "anime" if media.get("episodios") else "manga"
    )

    if request.method == "POST":
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

        return redirect(url_for("buscar", tipo=tipo.upper()))

    return render_template("detalles.html", media=media, tipo=tipo)


@app.route("/catalogo")
def catalogo():
    cur.execute("SELECT tipo, datos FROM multimedia ORDER BY id DESC;")
    registros = cur.fetchall()
    catalogo = [{"tipo": tipo, **datos} for tipo, datos in registros]
    return render_template("catalogo.html", catalogo=catalogo)

# ------------------------------------ #

if __name__ == "__main__":
    app.run(debug=True)
