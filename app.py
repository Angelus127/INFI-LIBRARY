from flask import Flask, render_template, request, redirect, url_for
import psycopg2, requests, json, psycopg2.extras

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
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

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
    titleAll = item.get("title", {})
    origin = item.get("countryOfOrigin")
    format_ = item.get("format")
    if origin == "JP":
        title = titleAll.get("romaji") or titleAll.get("english")
    elif origin == "KR":
        title = titleAll.get("english") or titleAll.get("romaji")  
    elif origin == "CN":
        title = titleAll.get("english") or titleAll.get("romaji")
    
    if format_ == "MANGA":
        if origin == "JP":
            kind = "MANGA"
        elif origin == "KR":
            kind = "MANHWA"
        elif origin == "CN":
            kind = "MANHUA"
    elif format_ in ("TV", "MOVIE", "OVA", "ONA"):
        if origin == "JP":
            kind = "ANIME"
        elif origin == "CN":
            kind = "DONGUA"
    else:
        kind = format_ or "UNKNOWN"
    return {
        "id_api": item.get("id"),
        "titulo": title,
        "portada": item.get("coverImage", {}).get("large"),
        "descripcion": item.get("description", ""),
        "puntuacion_media": item.get("averageScore"),
        "episodios": item.get("episodes"),
        "volumenes": item.get("volumes"),
        "capitulos": item.get("chapters"),
        "generos": item.get("genres", []),
        "estado": item.get("status"),
        "formato": format_,
        "tipo": kind,
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
            base_url = f"https://www.googleapis.com/books/v1/volumes"
            url=f"{base_url}?q=intitle:{titulo}&subject:fiction|romance|fantasy&printType=books&maxResults=10"
            res = requests.get(url).json()
            items = res.get("items", [])
            resultados = [formatear_libro(i) for i in items]
            
            if not items:
                url=f"{base_url}?q=intitle:{titulo}&maxResults=10"
                res = request.get(url).json()
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
                        countryOfOrigin
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

if __name__ == "__main__":
    app.run(debug=True)
