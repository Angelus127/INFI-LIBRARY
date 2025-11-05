from flask import Flask, render_template, request, redirect, url_for
import requests
import psycopg2
import json

app = Flask(__name__)

# Conexión a PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="infinitelibrary",
        user="postgres",
        password="cataleya"
    )

# Página de búsqueda
@app.route("/", methods=["GET"])
def search():
    query = request.args.get("q", "")
    page = int(request.args.get("page", 1))
    limit = 10
    results = []

    if query:
        start_index = (page - 1) * limit
        api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&startIndex={start_index}&maxResults={limit}"
        response = requests.get(api_url)
        data = response.json()
        results = data.get("items", [])

    return render_template("search.html", results=results, query=query, page=page, limit=limit)


# Página de detalles
@app.route("/details/<book_id>", methods=["GET", "POST"])
def details(book_id):
    api_url = f"https://www.googleapis.com/books/v1/volumes/{book_id}"
    response = requests.get(api_url)
    book = response.json()

    if request.method == "POST":
        puntuacion = request.form["puntuacion"]
        opinion = request.form["opinion"]
        estado = request.form["estado"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO multimedia (tipo, datos) VALUES (%s, %s) RETURNING id
        """, ("libro", json.dumps(book)))
        multimedia_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO usuario_multimedia (usuario_id, multimedia_id, puntuacion, estado, opinion)
            VALUES (%s, %s, %s, %s, %s)
        """, (1, multimedia_id, puntuacion, estado, opinion))

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("search"))

    return render_template("details.html", book=book)


if __name__ == "__main__":
    app.run(debug=True)
