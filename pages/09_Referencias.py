from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from components import carregar_css, hero, section_title, callout

carregar_css()

hero(
    "Base bibliográfica",
    "Referências",
    "Bibliografia utilizada na versão final do trabalho Qualidade do Código e Refatoração.",
    ["5 referências", "versão final"],
)

st.markdown(
    '<p class="cl-lead">As referências abaixo correspondem à versão final do relatório académico. '
    "Não foram acrescentadas fontes adicionais.</p>",
    unsafe_allow_html=True,
)

section_title("Bibliografia", "Ordenada alfabeticamente pelo apelido do autor ou entidade.")

referencias = [
    ("AWS", "Architecting for the Cloud: AWS Best Practices", "2021"),
    ("BERGMANN, S.; IBM", "Continuous Integration and Code Quality in Modern Software Engineering", "2020"),
    ("FOWLER, Martin", "Refactoring: Improving the Design of Existing Code", "2.ª edição, 2019"),
    ("MARTIN, Robert C.", "Clean Code: A Handbook of Agile Software Craftsmanship", "2008"),
    ("SOMMERVILLE, Ian", "Engenharia de Software", "10.ª edição, 2019"),
]

for autor, titulo, ano in referencias:
    st.markdown(
        f'<div class="cl-ref"><strong>{autor}.</strong> <em>{titulo}</em>. {ano}.</div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)
callout(
    "<strong>Uso no laboratório:</strong> Fowler fundamenta o conceito de refatoração e a "
    "preservação do comportamento externo; Martin fundamenta as práticas de código limpo; "
    "Sommerville enquadra engenharia de software e qualidade; Bergmann e IBM sustentam a "
    "integração contínua e a análise de qualidade; AWS contribui para as boas práticas de "
    "arquitectura e operação.",
    "violet",
)
