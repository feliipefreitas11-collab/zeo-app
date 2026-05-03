import streamlit as st

# =========================
# CONFIG
# =========================
st.set_page_config(layout="wide")

# =========================
# IDIOMAS
# =========================
idiomas = {
    "Português": {
        "login": "Login",
        "criar": "Criar conta",
        "usuario": "Usuário",
        "senha": "Senha",
        "entrar": "Entrar",
        "home": "Início",
        "simulado": "Simulado",
        "ia": "IA Tutor",
        "dashboard": "Dashboard",
        "sair": "Sair",
        "bem_vindo": "Bem-vindo ao ZEO 🚀",
        "escolha": "Escolha o que deseja fazer:",
    },
    "English": {
        "login": "Login",
        "criar": "Create account",
        "usuario": "User",
        "senha": "Password",
        "entrar": "Enter",
        "home": "Home",
        "simulado": "Quiz",
        "ia": "AI Tutor",
        "dashboard": "Dashboard",
        "sair": "Logout",
        "bem_vindo": "Welcome to ZEO 🚀",
        "escolha": "Choose what you want to do:",
    },
    "Español": {
        "login": "Login",
        "criar": "Crear cuenta",
        "usuario": "Usuario",
        "senha": "Contraseña",
        "entrar": "Entrar",
        "home": "Inicio",
        "simulado": "Simulado",
        "ia": "Tutor IA",
        "dashboard": "Panel",
        "sair": "Salir",
        "bem_vindo": "Bienvenido a ZEO 🚀",
        "escolha": "Elige lo que deseas hacer:",
    },
}

# =========================
# ESTADO INICIAL
# =========================
if "pagina" not in st.session_state:
    st.session_state.pagina = "lang"

if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = ""

if "idioma" not in st.session_state:
    st.session_state.idioma = "Português"

# =========================
# BANCO SIMPLES (MEMÓRIA)
# =========================
if "usuarios_db" not in st.session_state:
    st.session_state.usuarios_db = {}

def registrar(user, senha):
    if user in st.session_state.usuarios_db:
        return False
    st.session_state.usuarios_db[user] = senha
    return True

def login(user, senha):
    return st.session_state.usuarios_db.get(user) == senha

# =========================
# TELA IDIOMA
# =========================
def tela_idioma():
    st.title("🌍 Escolha seu idioma")

    idioma = st.selectbox(
        "",
        ["Português", "English", "Español"]
    )

    if st.button("Continuar"):
        st.session_state.idioma = idioma
        st.session_state.pagina = "login"
        st.rerun()

# =========================
# LOGIN
# =========================
def tela_login():
    lang = idiomas[st.session_state.idioma]

    st.title("🔐 ZEO Login")

    aba = st.radio("", [lang["login"], lang["criar"]])

    user = st.text_input(lang["usuario"])
    senha = st.text_input(lang["senha"], type="password")

    if aba == lang["login"]:
        if st.button(lang["entrar"]):
            if login(user, senha):
                st.session_state.logado = True
                st.session_state.usuario = user
                st.session_state.pagina = "home"
                st.rerun()
            else:
                st.error("❌ Dados inválidos")

    else:
        if st.button(lang["criar"]):
            if registrar(user, senha):
                st.success("Conta criada!")
            else:
                st.error("Usuário já existe")

# =========================
# HOME (NOVA EXPERIÊNCIA)
# =========================
def tela_home():
    lang = idiomas[st.session_state.idioma]

    st.title(lang["bem_vindo"])
    st.write(lang["escolha"])

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📝 " + lang["simulado"]):
            st.session_state.pagina = "simulado"
            st.session_state.q_index = 0
            st.session_state.pontos = 0
            st.rerun()

    with col2:
        if st.button("🤖 " + lang["ia"]):
            st.session_state.pagina = "ia"
            st.rerun()

    with col3:
        if st.button("📊 " + lang["dashboard"]):
            st.session_state.pagina = "dashboard"
            st.rerun()

# =========================
# SIMULADO (CORRIGIDO)
# =========================
def tela_simulado():
    perguntas = [
        {"q": "Quanto é 2 + 2?", "op": ["3", "4", "5"], "c": "4"},
        {"q": "Capital do Brasil?", "op": ["RJ", "SP", "Brasília"], "c": "Brasília"},
    ]

    if "q_index" not in st.session_state:
        st.session_state.q_index = 0
        st.session_state.pontos = 0

    q = perguntas[st.session_state.q_index]

    st.title("📝 Simulado")
    st.write(q["q"])

    escolha = st.radio("", q["op"], key=f"q_{st.session_state.q_index}")

    if st.button("Responder"):
        if escolha == q["c"]:
            st.success("✅ Correto")
            st.session_state.pontos += 1
        else:
            st.error(f"❌ Errado! Resposta: {q['c']}")

        st.session_state.q_index += 1

        if st.session_state.q_index >= len(perguntas):
            st.success(f"🎯 Pontuação: {st.session_state.pontos}")
            st.session_state.pagina = "home"
        else:
            st.rerun()

    if st.button("⬅️ Voltar"):
        st.session_state.pagina = "home"
        st.rerun()

# =========================
# IA
# =========================
def tela_ia():
    st.title("🤖 IA Tutor")
    pergunta = st.text_input("Digite sua dúvida")

    if st.button("Perguntar"):
        st.write("Resposta simulada da IA...")

    if st.button("⬅️ Voltar"):
        st.session_state.pagina = "home"
        st.rerun()

# =========================
# DASHBOARD
# =========================
def tela_dashboard():
    st.title("📊 Dashboard")
    st.write("Em desenvolvimento...")

    if st.button("⬅️ Voltar"):
        st.session_state.pagina = "home"
        st.rerun()

# =========================
# ROTEADOR
# =========================
if st.session_state.pagina == "lang":
    tela_idioma()

elif not st.session_state.logado:
    tela_login()

elif st.session_state.pagina == "home":
    tela_home()

elif st.session_state.pagina == "simulado":
    tela_simulado()

elif st.session_state.pagina == "ia":
    tela_ia()

elif st.session_state.pagina == "dashboard":
    tela_dashboard()