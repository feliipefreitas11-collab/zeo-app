import sqlite3

def conectar():
    return sqlite3.connect("zeo.db", check_same_thread=False)

def login(usuario, senha):
    conn = conectar()
    c = conn.cursor()

    c.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha))
    result = c.fetchone()

    conn.close()
    return result is not None


def registrar(usuario, senha):
    conn = conectar()
    c = conn.cursor()

    try:
        c.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
        conn.commit()
        conn.close()
        return True
    except:
        return False