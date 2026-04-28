import sqlite3

def conectar():
    return sqlite3.connect("zeo.db", check_same_thread=False)

def criar_tabelas():
    conn = conectar()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        usuario TEXT UNIQUE,
        senha TEXT,
        tipo TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS resultados (
        id INTEGER PRIMARY KEY,
        usuario TEXT,
        materia TEXT,
        score REAL
    )
    """)

    conn.commit()
    conn.close()

def criar_usuario(u, s, t):
    conn = conectar()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO usuarios VALUES (NULL,?,?,?)", (u,s,t))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login(u,s):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (u,s))
    r = c.fetchone()
    conn.close()
    return r

def salvar_resultado(u, materia, score):
    conn = conectar()
    c = conn.cursor()
    c.execute("INSERT INTO resultados VALUES (NULL,?,?,?)", (u,materia,score))
    conn.commit()
    conn.close()

def ranking():
    conn = conectar()
    c = conn.cursor()
    c.execute("""
    SELECT usuario, AVG(score)
    FROM resultados
    GROUP BY usuario
    ORDER BY AVG(score) DESC
    """)
    r = c.fetchall()
    conn.close()
    return r

def historico():
    conn = conectar()
    return conn.cursor().execute("SELECT * FROM resultados").fetchall()