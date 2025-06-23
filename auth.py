from flask import Blueprint, request, redirect, render_template, session, url_for, flash
from models import buscar_usuario_por_email, criar_usuario
from werkzeug.security import check_password_hash

auth = Blueprint("auth", __name__)

# Rota de login
@auth.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        usuario = buscar_usuario_por_email(email)

        # Verifica se o usuário existe e a senha está correta
        if usuario and check_password_hash(usuario["senha"], senha):
            session["usuario_id"] = usuario["id"]
            session["nome"] = usuario["nome"]
            session["email"] = usuario["email"]  # ← necessário para painel admin
            return redirect(url_for("dashboard"))

        flash("Email ou senha incorretos.")
    return render_template("login.html")

# Rota de registro
@auth.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        if buscar_usuario_por_email(email):
            flash("E-mail já está em uso. Tente outro.")
            return render_template("registro.html")

        criar_usuario(nome, email, senha)
        flash("Usuário criado com sucesso. Faça login.")
        return redirect(url_for("auth.login"))

    return render_template("registro.html")

# Rota de logout
@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
