from flask import Flask, render_template, session, redirect, url_for
from auth import auth
from database import init_db
from flask import request
from database import get_connection



app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = "sua_chave_secreta"
app.register_blueprint(auth)



@app.route("/dashboard")
def dashboard():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    materias = conn.execute("SELECT * FROM materias WHERE usuario_id = ?", (session["usuario_id"],)).fetchall()
    conn.close()

    return render_template("dashboard.html", nome=session["nome"], materias=materias)


@app.route("/nova_materia", methods=["GET", "POST"])
def nova_materia():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        nome = request.form["nome"]
        prova = float(request.form["prova"])
        pim = float(request.form["pim"])
        ava = float(request.form["ava"])
        ex = request.form.get("ex")
        ex = float(ex) if ex else None

        # Cálculo da MD
        md = round((7 * prova + 2 * pim + ava) / 10, 2)

        # Arredondamento se necessário
        if 6.7 <= md < 7.0:
            md = 7.0

        if md >= 7.0:
            mf = md
        elif ex is not None:
            mf = round((md + ex) / 2, 2)
            if 4.75 <= mf < 5.0:
                mf = 5.0
        else:
            mf = None

        # Definir status
        if md >= 7.0 or (mf is not None and mf >= 5.0):
            status = "Aprovado"
        elif mf is not None and mf < 5.0:
            status = "Reprovado"
        else:
            status = "Exame"

        conn = get_connection()
        conn.execute("""
            INSERT INTO materias (usuario_id, nome, prova, pim, ava, ex, md, mf, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (session["usuario_id"], nome, prova, pim, ava, ex, md, mf, status))
        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("nova_materia.html")

@app.route("/editar_materia/<int:id>", methods=["GET", "POST"])
def editar_materia(id):
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    materia = conn.execute(
        "SELECT * FROM materias WHERE id = ? AND usuario_id = ?",
        (id, session["usuario_id"])
    ).fetchone()

    if not materia:
        return "Matéria não encontrada", 404

    if request.method == "POST":
        ex = request.form.get("ex")
        ex = float(ex) if ex else None

        md = materia["md"]
        mf = md

        if md < 7.0 and ex is not None:
            mf = round((md + ex) / 2, 2)
            if 4.75 <= mf < 5.0:
                mf = 5.0

        # Atualiza status
        if mf >= 5.0:
            status = "Aprovado"
        else:
            status = "Reprovado"

        conn.execute("""
            UPDATE materias SET ex = ?, mf = ?, status = ?
            WHERE id = ? AND usuario_id = ?
        """, (ex, mf, status, id, session["usuario_id"]))
        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    conn.close()
    return render_template("editar_materia.html", materia=materia)
@app.route("/excluir_materia/<int:id>", methods=["POST"])
def excluir_materia(id):
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    conn.execute(
        "DELETE FROM materias WHERE id = ? AND usuario_id = ?",
        (id, session["usuario_id"])
    )
    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    import os
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


