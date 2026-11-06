"""CODELAB — Laboratório de Qualidade do Código e Refatoração."""
from __future__ import annotations

import streamlit as st

from components import carregar_css, sidebar_brand

st.set_page_config(
    page_title="CODELAB — Qualidade do Código e Refatoração",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

carregar_css()
sidebar_brand()

navegacao = st.navigation(
    {
        "Laboratório": [
            st.Page("pages/01_Visao_Geral.py", title="Visão Geral", icon=":material/home:", default=True),
            st.Page("pages/02_Laboratorio.py", title="Laboratório Prático", icon=":material/science:"),
            st.Page("pages/03_Comparacao.py", title="Comparação de Código", icon=":material/compare_arrows:"),
            st.Page("pages/04_Testes.py", title="Testes Automatizados", icon=":material/check_circle:"),
        ],
        "Conceitos": [
            st.Page("pages/05_Qualidade.py", title="Qualidade do Código", icon=":material/verified:"),
            st.Page("pages/06_Code_Smells.py", title="Code Smells", icon=":material/bug_report:"),
            st.Page("pages/07_Refatoracao.py", title="Técnicas de Refatoração", icon=":material/build:"),
            st.Page("pages/08_Ferramentas.py", title="Ferramentas e Métricas", icon=":material/analytics:"),
        ],
        "Recursos": [
            st.Page("pages/09_Referencias.py", title="Referências", icon=":material/menu_book:"),
        ],
    }
)

navegacao.run()
