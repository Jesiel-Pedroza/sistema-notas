import sqlite3
import os

# Caminho seguro e absoluto
DB_PATH = os.environ.get("DB_PATH", os.path.join(BASE_DIR, "../data/notas.db"))

def get_connection():
    # Garante que o diretório exista no ambiente do Render
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Criação da tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        );
    ''')

    # Criação da tabela de matérias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            nome TEXT NOT NULL,
            prova REAL NOT NULL,
            pim REAL NOT NULL,
            ava REAL NOT NULL,
            ex REAL,
            md REAL,
            mf REAL,
            status TEXT,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        );
    ''')

    conn.commit()
    conn.close()
