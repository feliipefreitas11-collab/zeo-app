import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI

# módulos internos
from database import criar_tabela
from auth import login, registrar
from simulador import gerar_questao
from ia import perguntar

# =========================
# CONFIG
# =========================
st.set_page_config(layout="wide")
criar_tabela()

# API KEY (Streamlit Secrets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# =========================
# SESSION
# =========================
if "logado" not in st.session_state:
    st.session_state.logado = False

if "pagina" not in st.session_state:
    st.session_state.pagina = "login"

# =========================
# LOGIN / CADASTRO
# =========================
if not st.session_state.logado:

    st.title("🔐 ZEO Login")

    aba = st.selectbox("Escolha", ["Login", "Criar conta"])

    if aba == "Login":
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            if login(usuario, senha):
                st.session_state.logado = True
                st.session_state.usuario = usuario
                st.session_state.pagina = "menu"
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos")

    else:
        novo_user = st.text_input("Novo usuário")
        nova_senha = st.text_input("Nova senha", type="password")

        if st.button("Registrar"):
            if registrar(novo_user, nova_senha):
                st.success("Conta criada!")
            else:
                st.error("Usuário já existe")

# =========================
# MENU PRINCIPAL
# =========================
else:

    st.sidebar.title(f"👋 {st.session_state.usuario}")
    menu = st.sidebar.radio(
        "Menu",
        ["Simulado", "Dashboard", "IA Tutor", "Sair"]
    )

    # =========================
    # SIMULADO
    # =========================
    if menu == "Simulado":

        st.title("📝 Simulado")

        questao = gerar_questao()

        st.write(questao["pergunta"])
        resposta = st.radio("Escolha:", questao["alternativas"])

        if st.button("Responder"):
            if resposta == questao["correta"]:
                st.success("✅ Correto!")
            else:
                st.error(f"❌ Errado! Resposta correta: {questao['correta']}")

    # =========================
    # DASHBOARD
    # =========================
    elif menu == "Dashboard":

        st.title("📊 Dashboard Escolar")

        dados = {
            "Aluno": ["João", "Maria", "Pedro"],
            "Nota": [700, 850, 600],
            "Matéria": ["Matemática", "Português", "História"]
        }

        df = pd.DataFrame(dados)
        st.dataframe(df)

        fig = px.bar(df, x="Aluno", y="Nota", color="Matéria")
        st.plotly_chart(fig)

    # =========================
    # IA TUTOR
    # =========================
    elif menu == "IA Tutor":

        st.title("🤖 Tutor com IA")

        pergunta_user = st.text_area("Faça sua pergunta")

        if st.button("Perguntar"):
            if pergunta_user:
                resposta = perguntar(pergunta_user)
                st.success(resposta)

    # =========================
    # SAIR
    # =========================
    elif menu == "Sair":
        st.session_state.logado = False
        st.session_state.pagina = "login"
        st.rerun()