def criar_tabela_resultados():
    conn = conectar()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS resultados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        materia TEXT,
        correta INTEGER
    )
    """)

    conn.commit()
    conn.close()


def salvar_resultado(usuario, materia, correta):
    conn = conectar()
    c = conn.cursor()

    c.execute("""
    INSERT INTO resultados (usuario, materia, correta)
    VALUES (?, ?, ?)
    """, (usuario, materia, correta))

    conn.commit()
    conn.close()


def historico(usuario):
    conn = conectar()
    c = conn.cursor()

    c.execute("""
    SELECT materia, correta FROM resultados WHERE usuario = ?
    """, (usuario,))

    dados = c.fetchall()
    conn.close()
    return dados