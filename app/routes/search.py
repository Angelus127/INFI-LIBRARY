from flask import render_template, request, Blueprint
from app.services.search_service import search

search_bp = Blueprint("search", __name__, template_folder='templates')

@search_bp.route("/buscar", methods=["GET", "POST"])
def buscar():
    resultados = []
    tipo = request.args.get("tipo", "LIBRO")

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        tipo = request.form.get("tipo", "LIBRO").upper()
        
        if titulo:
            resultados = search(titulo, tipo)

    return render_template("buscar.html", resultados=resultados, tipo=tipo)