from database import get_connection
from werkzeug.security import generate_password_hash

# Busca um usuário pelo e-mail
def buscar_usuario_por_email(email):
    conn = get_connection()
    user = conn.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
    conn.close()
    return user

# Cria um novo usuário com senha criptografada
def criar_usuario(nome, email, senha):
    senha_hash = generate_password_hash(senha)
    conn = get_connection()
    conn.execute(
        "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
        (nome, email, senha_hash)
    )
    conn.commit()
    conn.close()

# Lista todos os usuários cadastrados (usado no painel do admin)
def listar_todos_usuarios():
    conn = get_connection()
    usuarios = conn.execute("SELECT id, nome, email FROM usuarios").fetchall()
    conn.close()
    return usuarios
