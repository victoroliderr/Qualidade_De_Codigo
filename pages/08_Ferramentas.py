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
    callout,
    badge,
    tool,
    table as tabela,
    code_block,
)

carregar_css()

hero(
    "Ferramentas · Métricas · Transparência",
    "Ferramentas e Métricas",
    "As ferramentas tornam a qualidade observável. As métricas só têm valor quando são efectivamente medidas — o laboratório não inventa indicadores.",
    ["SonarQube", "Pylint", "ESLint", "McCabe"],
)

section_title(
    "Ferramentas de análise",
    "Cada ferramenta actua num ecossistema diferente. Não são intercambiáveis.",
    eyebrow="Ferramentas",
)

t1, t2, t3 = st.columns(3, gap="medium")
with t1:
    tool("SonarQube", "SQ", "Plataforma de análise contínua para várias linguagens. Avalia bugs, vulnerabilidades, code smells, duplicação e dívida técnica, integrando-se em pipelines de CI.")
with t2:
    tool("Pylint", "PY", "Analisador estático específico para Python. Verifica erros prováveis, convenções de estilo, imports, nomes e complexidade. É a ferramenta adequada para este projecto Python.")
with t3:
    tool("ESLint", "JS", "Analisador estático específico para JavaScript e ecossistemas relacionados. Não deve ser apresentado como ferramenta nativa de análise Python.")

st.markdown(
    f'<div class="cl-pill-row">{badge("Python → Pylint", "green")}'
    f'{badge("JavaScript → ESLint", "amber")}{badge("Multi-linguagem → SonarQube", "violet")}</div>',
    unsafe_allow_html=True,
)
callout(
    "<strong>Nota técnica:</strong> a escolha da ferramenta depende da linguagem e do contexto. "
    "Pylint não analisa JavaScript; ESLint não analisa Python; SonarQube é uma plataforma "
    "multi-linguagem com regras próprias para cada ecossistema.",
    "",
)

st.markdown("<br>", unsafe_allow_html=True)
section_title("Análise estática vs execução", "Duas formas complementares de verificar qualidade.")
c1, c2 = st.columns(2, gap="medium")
with c1:
    card("Análise estática", "Examina o código-fonte sem o executar. Deteta padrões, violações de estilo e riscos estruturais. Não substitui testes.", "violet", "AE")
with c2:
    card("Testes automatizados", "Executam o programa com entradas controladas e comparam os resultados esperados com os obtidos. Verificam comportamento.", "green", "TA")

st.markdown("<br>", unsafe_allow_html=True)
section_title(
    "Métricas de software",
    "Indicadores que ajudam a objectivar aquilo que, de outro modo, ficaria pela impressão.",
    eyebrow="Métricas",
)

m1, m2, m3 = st.columns(3, gap="medium")
with m1:
    card("Complexidade Ciclomática de McCabe", "Mede o número de caminhos independentes de execução. Pode ser estimada como decisões + 1, ou E − N + 2 no grafo de fluxo. Mais caminhos exigem mais casos de teste.", "accent", "CC", "Foco: esforço de teste e risco")
with m2:
    card("Cobertura de Testes", "Percentagem de linhas, ramos ou funções executadas pela suíte. Uma cobertura alta não garante bons testes; uma cobertura baixa revela zonas não verificadas.", "violet", "CT", "Foco: zonas exercitadas")
with m3:
    card("Acoplamento entre Classes", "Grau de dependência entre classes ou módulos. Acoplamento alto dificulta alterações isoladas, testes e reutilização.", "green", "AC", "Foco: independência entre componentes")

st.markdown("<br>", unsafe_allow_html=True)
section_title("O que este projecto mede — e o que não mede", "Transparência sobre o alcance real do laboratório.")
tabela(
    ["Indicador", "Estado neste projecto", "Como obter uma medição real"],
    [
        ["Comportamento", "Medido: execução comparativa e pytest", "Executar as duas implementações e a suíte de testes"],
        ["Testes", "Medido: 6 testes, resultados lidos do pytest", "python -m pytest tests/test_processamento_pedidos.py -v"],
        ["Complexidade ciclomática", "Não medido", "Pylint, Radon ou SonarQube com regras de complexidade"],
        ["Cobertura de testes", "Não medido", "pytest-cov (por exemplo: pytest --cov=implementacoes)"],
        ["Acoplamento", "Não medido", "Ferramentas de análise de dependências ou inspecção manual"],
    ],
)

callout(
    "<strong>Compromisso de rigor:</strong> não são apresentados valores de complexidade, "
    "cobertura ou acoplamento como se tivessem sido calculados. O laboratório demonstra o "
    "conceito, explica como se mede e reserva cada número para uma execução real da ferramenta.",
    "warn",
)

st.markdown("<br>", unsafe_allow_html=True)
section_title("Exemplos de comandos", "Comandos ilustrativos para medir qualidade num ambiente Python.")
code_block(
    """# Análise estática com Pylint
python -m pylint implementacoes

# Cobertura de testes com pytest-cov
python -m pytest --cov=implementacoes --cov-report=term-missing

# Complexidade ciclomática com Radon
python -m radon cc implementacoes -s -a""",
    filename="comandos_qualidade.sh",
    language="bash",
)

col_a, col_b = st.columns([1.1, 2.9])
with col_a:
    if st.button("Ver os testes reais", use_container_width=True):
        st.switch_page("pages/04_Testes.py")
