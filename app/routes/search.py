from flask import Flask, render_template, request, redirect, url_for, Blueprint, session
from ..services.temp import temp_create
from ..services.format import formatear_libro, formatear_media_anilist
import requests

media_cache = {}

search = Blueprint("search", __name__, template_folder='templates')


@search.route("/buscar", methods=["GET", "POST"])
def buscar():
    tipo = request.args.get("tipo", "LIBRO")
    resultados = []

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
                        countryOfOrigin
                    }
                }
            }
            '''
            variables = {"search": titulo, "type": tipo}
            res = requests.post("https://graphql.anilist.co", json={"query": query, "variables": variables}).json()
            items = res["data"]["Page"]["media"]
            resultados = [formatear_media_anilist(i) for i in items]

        for item in resultados:
            media_cache[str(item["id_api"])] = item
        
        temp_file_name = temp_create(media_cache)
        session['media_cache_file'] = temp_file_name

    return render_template("buscar.html", resultados=resultados, tipo=tipo)