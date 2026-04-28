import streamlit as st
import os
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from openai import OpenAI

from database import *

# =====================
# CONFIG
# =====================
st.set_page_config(layout="wide")
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

criar_tabelas()

# =====================
# SESSION
# =====================
if "page" not in st.session_state:
    st.session_state.page = "login"

if "user" not in st.session_state:
    st.session_state.user = None

if "tipo" not in st.session_state:
    st.session_state.tipo = None

# =====================
# LOGIN / CADASTRO
# =====================
if st.session_state.page == "login":

    st.title("🔐 ZEO Login")

    tipo = st.selectbox("Tipo", ["aluno","professor"])
    u = st.text_input("Usuário")
    s = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if login(u,s):
            st.session_state.user = u
            st.session_state.tipo = tipo
            st.session_state.page = "menu"
            st.rerun()
        else:
            st.error("Login inválido")

    st.divider()

    st.subheader("Criar conta")

    nu = st.text_input("Novo usuário")
    ns = st.text_input("Nova senha", type="password")

    if st.button("Cadastrar"):
        if criar_usuario(nu,ns,tipo):
            st.success("Conta criada")
        else:
            st.error("Usuário já existe")

# =====================
# MENU
# =====================
elif st.session_state.page == "menu":

    st.title(f"🧠 ZEO | {st.session_state.user}")

    if st.session_state.tipo == "aluno":

        col1, col2, col3 = st.columns(3)

        if col1.button("📘 Simulado"):
            st.session_state.page = "simulado"

        if col2.button("🤖 Tutor IA"):
            st.session_state.page = "ia"

        if col3.button("🏆 Ranking"):
            st.session_state.page = "ranking"

    else:
        if st.button("📊 Dashboard"):
            st.session_state.page = "dashboard"

    if st.button("🚪 Sair"):
        st.session_state.user = None
        st.session_state.page = "login"

# =====================
# SIMULADO IA
# =====================
elif st.session_state.page == "simulado":

    st.title("📘 Simulado Inteligente")

    materia = st.selectbox("Matéria", ["Matemática","Português","História"])

    if st.button("Gerar prova com IA"):

        prompt = f"""
        Gere 3 questões de {materia} estilo ENEM com 4 alternativas e gabarito.
        """

        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )

        st.session_state.prova = r.choices[0].message.content

    if "prova" in st.session_state:
        st.write(st.session_state.prova)

    nota = st.slider("Nota simulada", 0,100)

    if st.button("Salvar resultado"):
        salvar_resultado(st.session_state.user, materia, nota)
        st.success("Salvo!")

    if st.button("Voltar"):
        st.session_state.page = "menu"

# =====================
# IA TUTOR
# =====================
elif st.session_state.page == "ia":

    st.title("🤖 Tutor IA")

    pergunta = st.text_input("Pergunta")

    if st.button("Perguntar"):
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":pergunta}]
        )
        st.write(r.choices[0].message.content)

    if st.button("Voltar"):
        st.session_state.page = "menu"

# =====================
# RANKING
# =====================
elif st.session_state.page == "ranking":

    st.title("🏆 Ranking")

    data = ranking()
    df = pd.DataFrame(data, columns=["Aluno","Média"])

    st.dataframe(df)

    if st.button("Voltar"):
        st.session_state.page = "menu"

# =====================
# DASHBOARD PROFESSOR
# =====================
elif st.session_state.page == "dashboard":

    st.title("📊 Dashboard Escolar")

    data = historico()
    df = pd.DataFrame(data, columns=["id","Aluno","Matéria","Nota"])

    st.dataframe(df)

    fig = px.bar(df, x="Aluno", y="Nota", color="Matéria")
    st.plotly_chart(fig)

    if st.button("Voltar"):
        st.session_state.page = "menu"