from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from app.db import conectar, dict_cursor

auth = Blueprint("auth", __name__, template_folder="templates")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = conectar()
        cur = dict_cursor(conn)

        cur.execute(
            "SELECT id, password FROM usuario WHERE username = %s",
            (username,)
        )
        user = cur.fetchone()

        if not user:
            return render_template("login.html", error="Usuario o contraseña incorrectos")
        if not check_password_hash(user["password"], password):
            return render_template("login.html", error="Usuario o contraseña incorrectos")

        session.clear()
        session["user_id"] = user["id"]
        session["username"] = username

        return redirect(url_for("home.index"))

    return render_template("login.html")

@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))