from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from components import (
    carregar_css,
    hero,
    section_title,
    card,
    stat,
    flow,
    callout,
    badge,
)

carregar_css()

hero(
    "Laboratório interactivo · Python · pytest",
    "CODELAB",
    "Descobre como a refatoração transforma a estrutura do código sem alterar o seu comportamento.",
    ["2 implementações", "3 perfis de cliente", "pytest"],
)

st.markdown(
    '<p class="cl-lead">Este laboratório demonstra, na prática, os princípios de '
    "<strong>Qualidade do Código</strong> e <strong>Refatoração</strong>. A partir do "
    "processamento de pedidos de uma loja virtual, compara uma implementação original com uma "
    "versão refatorada, executa as duas versões com os mesmos dados, confronta faturas e corre "
    "uma suíte de testes automatizados com pytest.</p>",
    unsafe_allow_html=True,
)

section_title(
    "O processo de refatoração",
    "Melhorar a estrutura interna sem modificar o comportamento externo observado.",
    eyebrow="Visão geral",
)
flow(["CÓDIGO ORIGINAL", "ANÁLISE", "REFATORAÇÃO", "TESTES", "CÓDIGO MELHOR ORGANIZADO"], highlight=2)

st.markdown("<br>", unsafe_allow_html=True)
section_title("Áreas do laboratório", "Cada página cumpre uma etapa concreta da demonstração.")

areas = [
    (
        "Laboratório Prático",
        "Configura um pedido, executa as duas implementações e compara valores e faturas.",
        "accent",
        "01",
        "pages/02_Laboratorio.py",
        "Abrir laboratório",
    ),
    (
        "Comparação de Código",
        "Lê os módulos reais e apresenta os painéis Before/After, o diff e as responsabilidades.",
        "violet",
        "02",
        "pages/03_Comparacao.py",
        "Comparar código",
    ),
    (
        "Testes Automatizados",
        "Executa o pytest a sério e mostra o estado real de cada teste e da consola.",
        "green",
        "03",
        "pages/04_Testes.py",
        "Executar testes",
    ),
    (
        "Qualidade do Código",
        "Explora atributos, dívida técnica, práticas, ferramentas e métricas.",
        "",
        "04",
        "pages/05_Qualidade.py",
        "Explorar conceitos",
    ),
    (
        "Code Smells",
        "Galeria interactiva de maus cheiros com exemplos Python e técnicas de correção.",
        "amber",
        "05",
        "pages/06_Code_Smells.py",
        "Ver galeria",
    ),
    (
        "Técnicas de Refatoração",
        "Extrair Método, eliminar duplicação, renomear e simplificar condicionais.",
        "red",
        "06",
        "pages/07_Refatoracao.py",
        "Ver técnicas",
    ),
]

for linha in range(0, len(areas), 3):
    colunas = st.columns(3, gap="medium")
    for coluna, (titulo, texto, variante, icon, destino, acao) in zip(colunas, areas[linha:linha + 3]):
        with coluna:
            card(titulo, texto, variante, icon)
            if st.button(acao, key=f"atalho_{icon}", use_container_width=True):
                st.switch_page(destino)

st.markdown("<br>", unsafe_allow_html=True)
section_title("Indicadores do laboratório", "Dados estruturais da demonstração — não são resultados de execução.")
m1, m2, m3, m4 = st.columns(4, gap="medium")
with m1:
    stat("02", "Implementações", "Original e refatorada", "accent")
with m2:
    stat("03", "Perfis de cliente", "COMUM · VIP · PREMIUM", "violet")
with m3:
    stat("04", "Funções refatoradas", "Responsabilidades separadas", "green")
with m4:
    stat("06", "Testes pytest", "3 académicos + 3 complementares", "")

st.markdown("<br>", unsafe_allow_html=True)
section_title("Como conduzir a demonstração", "Uma sequência curta, pensada para a defesa.")
passos = st.columns(3, gap="medium")
with passos[0]:
    card("1 · Configurar", "Escolhe um cliente COMUM, VIP ou PREMIUM e monta o pedido com produtos e quantidades.", "accent", "01")
with passos[1]:
    card("2 · Executar", "As duas implementações correm com cópias independentes dos mesmos dados. A fatura é capturada com StringIO.", "violet", "02")
with passos[2]:
    card("3 · Validar", "Compara valores e faturas, confirma o comportamento preservado e executa o pytest.", "green", "03")

st.markdown("<br>", unsafe_allow_html=True)
callout(
    "<strong>Princípio central:</strong> a refatoração altera a estrutura interna do software "
    "sem modificar o seu comportamento externo observado. É esse contrato que o laboratório "
    "verifica em cada execução.",
    "violet",
)

st.markdown("<br>", unsafe_allow_html=True)
coluna_cta, _ = st.columns([1.2, 2.8])
with coluna_cta:
    if st.button("EXPLORAR LABORATÓRIO", type="primary", use_container_width=True):
        st.switch_page("pages/02_Laboratorio.py")
