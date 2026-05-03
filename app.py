import streamlit as st
import pandas as pd

# DATABASE
from database import (
    criar_tabela,
    criar_tabela_resultados,
    salvar_resultado,
    historico
)

# AUTH
from auth import registrar, login

# IA
from ia import explicar_erro, gerar_plano

# SIMULADOR
from simulador import gerar_simulado

# ANALYTICS
from analytics import calcular_desempenho, sugerir_materia


# =========================
# INIT
# =========================
criar_tabela()
criar_tabela_resultados()

st.set_page_config(page_title="ZEO", layout="centered")

# =========================
# SESSION STATE
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

    aba = st.radio("Escolha", ["Login", "Criar conta"])

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

    st.title("🎓 ZEO Plataforma")

    st.success(f"Bem-vindo, {st.session_state.usuario}")

    if st.button("🚪 Sair"):
        st.session_state.logado = False
        st.session_state.pagina = "login"
        st.rerun()

    st.divider()

    col1, col2 = st.columns(2)

    if col1.button("🧪 Fazer Simulado"):
        st.session_state.pagina = "simulado"

    if col2.button("📊 Ver Desempenho"):
        st.session_state.pagina = "dashboard"


# =========================
# SIMULADO
# =========================
if st.session_state.logado and st.session_state.pagina == "simulado":

    st.title("🧪 Simulado")

    materia = st.selectbox("Escolha a matéria", ["Matemática", "Português"])

    if st.button("Gerar Simulado"):
        st.session_state.questoes = gerar_simulado(materia)
        st.session_state.respostas = {}
        st.session_state.materia = materia

    if "questoes" in st.session_state:

        for i, q in enumerate(st.session_state.questoes):
            st.subheader(f"Questão {i+1}")
            st.write(q["pergunta"])

            resposta = st.radio(
                "Escolha:",
                q["alternativas"],
                key=f"q_{i}"
            )

            st.session_state.respostas[i] = resposta

        if st.button("Finalizar Simulado"):
            acertos = 0

            for i, q in enumerate(st.session_state.questoes):

                resposta = st.session_state.respostas[i]

                correta_flag = 1 if resposta == q["correta"] else 0

                salvar_resultado(
                    st.session_state.usuario,
                    st.session_state.materia,
                    correta_flag
                )

                if correta_flag:
                    acertos += 1
                else:
                    st.error(f"❌ Erro na questão {i+1}")

                    explicacao = explicar_erro(
                        q["pergunta"],
                        resposta,
                        q["correta"]
                    )

                    st.info(explicacao)

            st.success(f"🎯 Resultado: {acertos}/{len(st.session_state.questoes)}")

            if st.button("Voltar ao menu"):
                st.session_state.pagina = "menu"
                st.rerun()


# =========================
# DASHBOARD
# =========================
if st.session_state.logado and st.session_state.pagina == "dashboard":

    st.title("📊 Seu Desempenho")

    dados = historico(st.session_state.usuario)

    if not dados:
        st.warning("Você ainda não fez simulados.")
    else:
        resumo = calcular_desempenho(dados)

        tabela = []
        for materia, d in resumo.items():
            tabela.append({
                "Matéria": materia,
                "Acertos (%)": int(d["taxa"] * 100)
            })

        df = pd.DataFrame(tabela)

        st.dataframe(df)

        st.bar_chart(df.set_index("Matéria"))

        pior = sugerir_materia(resumo)

        if pior:
            st.warning(f"⚠️ Foque mais em: {pior}")

        if st.button("🤖 Gerar plano de estudo com IA"):
            plano = gerar_plano(resumo)
            st.info(plano)

    if st.button("⬅️ Voltar"):
        st.session_state.pagina = "menu"
        st.rerun()