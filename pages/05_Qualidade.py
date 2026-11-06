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
    attribute_card,
    flow_vertical,
    table as tabela,
    callout,
    badge,
    tool,
)

carregar_css()

hero(
    "Fundamentos · Dívida técnica · Práticas",
    "Qualidade do código",
    "Um programa que funciona ainda pode ser difícil de compreender, modificar, reutilizar e manter. A qualidade mede também essa facilidade.",
    ["5 atributos", "dívida técnica", "4 práticas"],
)

st.markdown(
    '<p class="cl-lead">A qualidade do código-fonte não depende apenas de o programa produzir o '
    "resultado esperado. Depende igualmente da facilidade com que outros programadores conseguem "
    "compreender, alterar, reutilizar e manter o software ao longo do tempo.</p>",
    unsafe_allow_html=True,
)

separadores = st.tabs(["Atributos", "Dívida Técnica", "Práticas", "Ferramentas & Métricas"])

with separadores[0]:
    section_title(
        "Os cinco atributos fundamentais",
        "Cada atributo observa o código por um ângulo diferente — e todos se reforçam entre si.",
        eyebrow="Fundamentos",
    )

    linha1 = st.columns(3, gap="medium")
    with linha1[0]:
        attribute_card("LG", "Legibilidade", "Facilidade de compreender a intenção, a lógica e o fluxo do código.", "Compreensão humana", "Redução do tempo de compreensão")
    with linha1[1]:
        attribute_card("MN", "Manutenibilidade", "Facilidade de modificar ou corrigir o código sem introduzir novos problemas.", "Modificação segura", "Diminuição dos custos de manutenção")
    with linha1[2]:
        attribute_card("RE", "Reutilização", "Capacidade de usar componentes existentes em diferentes partes do sistema, evitando duplicações.", "Modularidade", "Maior velocidade de desenvolvimento")

    linha2 = st.columns(2, gap="medium")
    with linha2[0]:
        attribute_card("EF", "Eficiência", "Utilização adequada dos recursos computacionais, incluindo memória e tempo de processamento.", "Uso dos recursos", "Melhor desempenho e custos")
    with linha2[1]:
        attribute_card("CF", "Confiabilidade", "Capacidade de executar consistentemente o comportamento esperado em diferentes condições.", "Estabilidade", "Maior satisfação do utilizador")

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Relação entre atributo, foco e benefício", "Síntese apresentada no relatório académico.")
    tabela(
        ["Atributo", "Foco principal", "Benefício"],
        [
            ["Legibilidade", "Compreensão humana", "Redução do tempo de compreensão"],
            ["Manutenibilidade", "Modificação segura", "Diminuição dos custos de manutenção"],
            ["Reutilização", "Modularidade", "Maior velocidade de desenvolvimento"],
            ["Eficiência", "Uso dos recursos", "Melhor desempenho e custos"],
            ["Confiabilidade", "Estabilidade", "Maior satisfação do utilizador"],
        ],
    )

    st.markdown(
        '<div class="cl-callout violet"><strong>No laboratório:</strong> a versão refatorada '
        "melhora a legibilidade (funções com nomes claros), a manutenibilidade (responsabilidades "
        "separadas) e a reutilização (cálculo, desconto e fatura podem ser usados isoladamente). "
        "A confiabilidade é demonstrada pelos testes que comparam as duas versões.</div>",
        unsafe_allow_html=True,
    )

with separadores[1]:
    section_title(
        "Dívida Técnica",
        "Atalhos poupam tempo agora, mas transferem custo para o futuro.",
        eyebrow="Technical Debt",
    )
    st.markdown(
        '<p class="cl-lead">Quando uma equipa escolhe atalhos ou implementações de baixa qualidade '
        "para entregar rapidamente, pode criar problemas que tornam as alterações futuras cada vez "
        "mais dispendiosas. É a analogia da dívida: o esforço evitado hoje acumula juros técnicos.</p>",
        unsafe_allow_html=True,
    )

    flow_vertical(
        [
            ("Decisão por atalho / gambiarra", "Uma solução rápida concentra responsabilidades ou ignora a estrutura."),
            ("Acumulação de dívida técnica", "O atalho passa a ser dependência de outras partes do sistema."),
            ("Aumento da rigidez e fragilidade", "Cada alteração exige mais cuidado e cria mais efeitos colaterais."),
            ("Desaceleração das entregas", "A equipa gasta mais tempo a compreender e a corrigir do que a evoluir."),
        ],
    )

    section_title("Consequências da dívida não tratada")
    consequencias = [
        ("Tempo de desenvolvimento", "Aumenta o tempo necessário para acrescentar funcionalidades.", "accent", "01"),
        ("Manutenção", "Aumenta a dificuldade de compreender e alterar o código.", "violet", "02"),
        ("Bugs", "Cresce a possibilidade de introduzir defeitos em cada alteração.", "red", "03"),
        ("Velocidade da equipa", "A equipa desacelera porque depende de código frágil.", "amber", "04"),
        ("Reescrita", "Pode tornar necessária a reescrita de partes do sistema.", "green", "05"),
    ]
    for inicio in range(0, len(consequencias), 3):
        colunas = st.columns(3, gap="medium")
        for coluna, (titulo, texto, variante, icon) in zip(colunas, consequencias[inicio:inicio + 3]):
            with coluna:
                card(titulo, texto, variante, icon)

    callout(
        "<strong>Relação com o exemplo:</strong> a função original não está errada — funciona. "
        "Mas concentra cálculo, desconto e fatura, usa condicionais pouco extensíveis e valores "
        "embutidos. São atalhos estruturais que aumentam o custo de cada nova regra de negócio.",
        "warn",
    )

with separadores[2]:
    section_title(
        "Práticas de promoção da qualidade",
        "Mecanismos que tornam os problemas visíveis antes de chegarem à produção.",
        eyebrow="Práticas",
    )
    p1, p2 = st.columns(2, gap="medium")
    with p1:
        card("Code Review", "Revisão do código por outros programadores antes de integrar alterações. Deteta problemas de clareza, desenho e consistência.", "accent", "CR", "Revisão humana antes do merge")
    with p2:
        card("Análise Estática", "Análise automatizada do código sem o executar. Identifica padrões suspeitos, más práticas e violações de estilo.", "violet", "AE", "Ferramentas analisam o código-fonte")
    p3, p4 = st.columns(2, gap="medium")
    with p3:
        card("Testes Automatizados", "Testes que verificam se o programa continua a produzir os resultados esperados após cada alteração.", "green", "TA", "Protecção contra regressões")
    with p4:
        card("Métricas de Software", "Indicadores que permitem avaliar aspectos técnicos do código, como complexidade, cobertura e acoplamento.", "amber", "MS", "Objectividade na avaliação")

    section_title("Ferramentas mencionadas no trabalho")
    st.markdown(
        f'<div class="cl-pill-row">{badge("Python", "blue")}{badge("JavaScript", "amber")}'
        f'{badge("Multi-linguagem", "violet")}</div>',
        unsafe_allow_html=True,
    )
    f1, f2, f3 = st.columns(3, gap="medium")
    with f1:
        tool("SonarQube", "SQ", "Plataforma de análise contínua que avalia qualidade, bugs, vulnerabilidades e dívida técnica em várias linguagens.")
    with f2:
        tool("Pylint", "PY", "Ferramenta de análise estática específica para Python: estilo, erros prováveis e más práticas.")
    with f3:
        tool("ESLint", "JS", "Ferramenta de análise estática específica para JavaScript. Não é uma ferramenta nativa de análise Python.")

    callout(
        "<strong>Nota técnica:</strong> Pylint analisa Python; ESLint analisa JavaScript; "
        "SonarQube é uma plataforma multi-linguagem. As três não são intercambiáveis.",
        "",
    )

with separadores[3]:
    section_title(
        "Métricas de software",
        "Indicadores teóricos. O laboratório não inventa valores de análise que não executou.",
        eyebrow="Medição",
    )
    m1, m2, m3 = st.columns(3, gap="medium")
    with m1:
        card("Complexidade Ciclomática de McCabe", "Conta os caminhos independentes de execução de uma função. Valores mais altos indicam mais ramificações e maior esforço de teste.", "accent", "CC", "Quanto maior, mais caminhos testar")
    with m2:
        card("Cobertura de Testes", "Percentagem do código executada pela suíte de testes. Ajuda a identificar zonas sem verificação, mas não garante qualidade dos testes.", "violet", "CT", "Código exercitado pela suíte")
    with m3:
        card("Acoplamento entre Classes", "Grau de dependência entre classes ou módulos. Acoplamento elevado dificulta alterações isoladas e reutilização.", "green", "AC", "Dependências entre componentes")

    st.markdown("<br>", unsafe_allow_html=True)
    callout(
        "<strong>Transparência:</strong> esta aplicação demonstra o conceito e a execução "
        "comparativa, mas não apresenta valores de complexidade, cobertura ou acoplamento como se "
        "tivessem sido medidos. Para uma medição real seriam necessárias ferramentas dedicadas, "
        "como Pylint, SonarQube ou pytest-cov.",
        "warn",
    )
    st.markdown(
        "A página **Ferramentas e Métricas** aprofunda cada indicador e distingue o que é "
        "observável no projecto daquilo que exigiria instrumentação adicional."
    )
    if st.button("Abrir Ferramentas e Métricas", use_container_width=False):
        st.switch_page("pages/08_Ferramentas.py")
