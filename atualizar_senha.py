from database import get_connection
from werkzeug.security import generate_password_hash

def atualizar_senha(email, nova_senha):
    nova_senha_hash = generate_password_hash(nova_senha)
    conn = get_connection()
    conn.execute("UPDATE usuarios SET senha = ? WHERE email = ?", (nova_senha_hash, email))
    conn.commit()
    conn.close()
    print(f"Senha atualizada com sucesso para: {email}")

# Atualizar senha do admin
atualizar_senha("jesiel@jespedsys.com.br", "admin123")
