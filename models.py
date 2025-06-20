from database import get_connection
from werkzeug.security import generate_password_hash

def buscar_usuario_por_email(email):
    conn = get_connection()
    user = conn.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
    conn.close()
    return user

def criar_usuario(nome, email, senha):
    senha_hash = generate_password_hash(senha)
    conn = get_connection()
    conn.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha_hash))
    conn.commit()
    conn.close()


