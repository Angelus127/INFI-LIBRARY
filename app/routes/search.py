from flask import Flask, render_template, request, redirect, url_for, Blueprint, session
from ..services.temp import temp_create
from ..services.format import formatear_libro, formatear_media_anilist
import requests, os
from dotenv import load_dotenv

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
            url = "https://api.hardcover.app/v1/graphql"

            query = """
            query GetEditionsFromTitle ($titulo: String!) {
                editions(where: { title: { _eq: $titulo } }){
                    isbn_13
                    isbn_10
                    title
                    image {
                        url
                    }
                    publisher {
                        name
                    }
                    book {
                        id
                        subtitle
                        contributions {
                            author {
                                name
                            }
                        }
                        release_date
                        pages
                        description
                        rating
                        cached_tags
                    }
                }
            }
            """

            headers = {
                "Authorization": f"Bearer {os.getenv('BOOKS_API')}",
                "Content-Type": "application/json"
            }

            res = requests.post(
                url,
                headers=headers,
                json={
                    "query": query,
                    "variables": {
                        "titulo": titulo
                    }
                }
            ).json()

            if "errors" in res:
                print("GRAPHQL ERROR:", res["errors"])

            libros = res.get("data", {}).get("editions", [])
            resultados = [formatear_libro(b) for b in libros]
            
        else:
            query = '''
            query ($search: String, $type: MediaType) {
                Page(perPage: 20) {
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