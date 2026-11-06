from __future__ import annotations

import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import streamlit as st

from implementacoes import (
    exemplo_original,
    exemplo_refatorado,
    extensao_original,
    extensao_refatorada,
)


PASTA = Path(__file__).resolve().parent
SECOES = [
    "Visão geral",
    "Simulador",
    "Comparação do código",
    "Testes",
    "Qualidade",
    "Conceitos",
]

st.set_page_config(
    page_title="Laboratório de Qualidade do Código",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
        --tinta: #142b45;
        --texto: #26384b;
        --suave: #62758a;
        --linha: #d7e0ea;
        --papel: #f4f7fb;
        --branco: #ffffff;
        --azul: #2364a0;
        --verde: #087f70;
        --verde-claro: #e5f5f1;
        --ambar: #a96312;
    }

    .stApp { background: var(--papel); color: var(--texto); }
    [data-testid="stSidebar"] {
        background: #eaf0f6;
        border-right: 1px solid var(--linha);
    }
    [data-testid="stSidebar"] section { padding-top: 1.25rem; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: var(--suave);
    }
    .block-container {
        max-width: 1320px;
        padding-top: 2.1rem;
        padding-bottom: 4rem;
    }
    h1, h2, h3 { color: var(--tinta); letter-spacing: -0.025em; }
    h1 { font-size: clamp(2rem, 4vw, 3.15rem) !important; line-height: 1.08 !important; }
    h2 { margin-top: 1.6rem !important; }
    p, li { line-height: 1.65; }
    [data-testid="stCaptionContainer"] { color: var(--suave); }
    div.stButton > button[kind="primary"] {
        background: var(--azul);
        border: 1px solid var(--azul);
        border-radius: 8px;
        min-height: 2.8rem;
        padding: 0.55rem 1.05rem;
        font-weight: 650;
    }
    div.stButton > button[kind="primary"]:hover {
        background: #174d80;
        border-color: #174d80;
    }
    div.stButton > button:focus-visible, input:focus-visible {
        outline: 3px solid #66b8ad !important;
        outline-offset: 2px;
    }
    [data-testid="stCode"] {
        border: 1px solid var(--linha);
        border-radius: 9px;
        background: #f8fafc;
    }
    [data-testid="stMetric"] {
        background: var(--branco);
        border: 1px solid var(--linha);
        border-radius: 9px;
        padding: 0.8rem 1rem;
    }
    .hero {
        background: var(--tinta);
        color: #f4f8fc;
        border-radius: 14px;
        padding: clamp(1.5rem, 4vw, 3rem);
        border-left: 6px solid #56b7a6;
        margin: 0.2rem 0 1.4rem;
    }
    .hero h1 { color: #ffffff !important; max-width: 820px; margin-bottom: .8rem; }
    .hero p { color: #d6e2ee; max-width: 760px; font-size: 1.08rem; margin: 0; }
    .hero-kicker { color: #9ad9cd; font-size: .84rem; margin-bottom: .7rem; }
    .flow {
        display: grid;
        grid-template-columns: 1fr auto 1fr auto 1fr;
        align-items: center;
        gap: .8rem;
        padding: 1rem 1.15rem;
        border-top: 1px solid #d7e0ea;
        border-bottom: 1px solid #d7e0ea;
        background: #fff;
        margin: 1.2rem 0 1.8rem;
    }
    .flow-step { color: #26384b; }
    .flow-step strong { display: block; color: #142b45; font-size: .97rem; }
    .flow-step span { color: #62758a; font-size: .87rem; }
    .flow-mark { color: #087f70; font-weight: 700; font-size: 1.2rem; }
    .section-note {
        border-left: 3px solid #56b7a6;
        padding: .75rem 1rem;
        background: #eaf5f3;
        border-radius: 0 7px 7px 0;
        color: #244c50;
        margin: .7rem 0 1rem;
    }
    .version-label {
        display: inline-block;
        color: #52667b;
        font-size: .88rem;
        margin-bottom: .35rem;
    }
    .result-heading {
        border-bottom: 1px solid #d7e0ea;
        padding-bottom: .6rem;
        margin-bottom: .4rem;
    }
    .sidebar-brand {
        font-size: 1.05rem;
        color: #142b45;
        font-weight: 750;
        line-height: 1.3;
        margin: .15rem 0 .2rem;
    }
    @media (max-width: 760px) {
        .block-container { padding: 1.2rem 1rem 2.5rem; }
        .flow { grid-template-columns: 1fr; gap: .35rem; }
        .flow-mark { transform: rotate(90deg); width: 1rem; }
    }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { scroll-behavior: auto !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def fonte(caminho: str) -> str:
    """Lê o módulo executado para que a interface mostre o código real."""
    return (PASTA / caminho).read_text(encoding="utf-8")


def capturar_saida(funcao, usuario: dict) -> str:
    saida = io.StringIO()
    with redirect_stdout(saida):
        funcao(usuario)
    return saida.getvalue()


def texto_de_saida(saida: str) -> str:
    return saida.rstrip("\n") if saida else "Nenhuma notificação foi emitida."


def achatar_suite(suite):
    for teste in suite:
        if isinstance(teste, unittest.TestSuite):
            yield from achatar_suite(teste)
        else:
            yield teste


def executar_suite_de_testes() -> dict:
    from tests.test_comportamento import TestComportamentoRefatoracao

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        TestComportamentoRefatoracao
    )
    casos = list(achatar_suite(suite))
    relatorio = io.StringIO()
    resultado = unittest.TextTestRunner(stream=relatorio, verbosity=0).run(suite)
    falhas = {
        caso.id(): detalhe
        for caso, detalhe in [*resultado.failures, *resultado.errors]
    }

    registos = []
    for caso in casos:
        erro = falhas.get(caso.id(), "")
        registos.append(
            {
                "nome": getattr(caso, "descricao", caso.shortDescription() or caso.id()),
                "esperado": getattr(caso, "resultado_esperado", "Verificação concluída."),
                "obtido": getattr(caso, "resultado_obtido", "O teste terminou antes de obter uma saída."),
                "aprovado": not bool(erro),
                "erro": erro,
            }
        )

    return {
        "registos": registos,
        "executados": resultado.testsRun,
        "falhas": len(resultado.failures) + len(resultado.errors),
        "output": relatorio.getvalue(),
    }


def cabecalho(titulo: str, descricao: str) -> None:
    st.title(titulo)
    st.write(descricao)


with st.sidebar:
    st.markdown('<div class="sidebar-brand">Laboratório de<br>Qualidade do Código</div>', unsafe_allow_html=True)
    st.caption("Demonstração de refatoração em Python")
    pagina = st.radio("Explorar", SECOES, label_visibility="visible")
    st.divider()
    st.caption("Exemplo principal: Extrair Método")
    st.caption("Extensão: reutilização e eliminação de duplicação")


if pagina == "Visão geral":
    st.markdown(
        """
        <section class="hero">
          <div class="hero-kicker">Laboratório interactivo em Python</div>
          <h1>Laboratório de Qualidade do Código</h1>
          <p>Compreender, comparar e experimentar a refatoração na prática.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="flow">
          <div class="flow-step"><strong>Mesmo utilizador</strong><span>Uma entrada controlada</span></div>
          <div class="flow-mark">→</div>
          <div class="flow-step"><strong>Duas estruturas</strong><span>Original e refatorada</span></div>
          <div class="flow-mark">→</div>
          <div class="flow-step"><strong>Mesmo comportamento</strong><span>Saídas executadas e comparadas</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.subheader("O que vais observar")
    st.write(
        "O programa verifica se um utilizador é administrador e, nesse caso, "
        "emite uma notificação. A versão original executa essa acção dentro "
        "da função de processamento. A versão refatorada extrai a notificação "
        "para uma função própria."
    )
    original, refatorado = st.columns(2)
    with original:
        st.markdown("#### Código original")
        st.write("Funciona e representa o ponto de partida do exemplo académico.")
        st.code(fonte("implementacoes/exemplo_original.py"), language="python")
    with refatorado:
        st.markdown("#### Código refatorado")
        st.write("A notificação ganha um nome e uma responsabilidade próprios.")
        st.code(fonte("implementacoes/exemplo_refatorado.py"), language="python")
    st.markdown(
        '<div class="section-note"><strong>Ideia central:</strong> a estrutura interna muda; '
        'o resultado visível para a mesma entrada deve permanecer igual.</div>',
        unsafe_allow_html=True,
    )
    st.subheader("Como navegar")
    st.write(
        "Use o menu lateral para executar o simulador, abrir o código dos módulos "
        "reais, correr os testes e rever os conceitos de qualidade abordados no trabalho."
    )


elif pagina == "Simulador":
    cabecalho(
        "Simulador",
        "Escolhe os mesmos dados e executa as duas implementações para comparar as saídas reais.",
    )
    coluna_pessoa, coluna_operacao = st.columns([1, 1.4])
    with coluna_pessoa:
        nome = st.selectbox("Utilizador de teste", ["Ana", "João"])
    with coluna_operacao:
        operacao = st.selectbox(
            "Operação",
            ["Processar utilizador", "Processar relatório (extensão)"],
        )
    eh_admin = nome == "Ana"
    st.caption(f"Perfil seleccionado: {'Administradora' if eh_admin else 'Utilizador comum'}. Os mesmos dados serão enviados às duas versões.")
    if operacao == "Processar relatório (extensão)":
        st.info("Esta operação pertence à extensão didáctica de reutilização e eliminação de duplicação.")

    if st.button("Executar comparação", type="primary"):
        usuario = {"nome": nome, "admin": eh_admin}
        if operacao == "Processar relatório (extensão)":
            funcao_original = extensao_original.processar_relatorio
            funcao_refatorada = extensao_refatorada.processar_relatorio
        else:
            funcao_original = exemplo_original.processar_usuario
            funcao_refatorada = exemplo_refatorado.processar_usuario

        saida_original = capturar_saida(funcao_original, usuario)
        saida_refatorada = capturar_saida(funcao_refatorada, usuario)
        st.session_state["ultima_comparacao"] = {
            "operacao": operacao,
            "nome": nome,
            "original": saida_original,
            "refatorada": saida_refatorada,
        }

    comparacao = st.session_state.get("ultima_comparacao")
    if comparacao:
        st.markdown("### Resultado da execução")
        st.caption(f"{comparacao['operacao']} · {comparacao['nome']}")
        original, refatorado = st.columns(2)
        with original:
            st.markdown('<div class="result-heading"><span class="version-label">Versão original</span></div>', unsafe_allow_html=True)
            st.code(texto_de_saida(comparacao["original"]), language="text")
        with refatorado:
            st.markdown('<div class="result-heading"><span class="version-label">Versão refatorada</span></div>', unsafe_allow_html=True)
            st.code(texto_de_saida(comparacao["refatorada"]), language="text")
        if comparacao["original"] == comparacao["refatorada"]:
            st.success("As saídas são iguais. O comportamento foi preservado para esta entrada.")
        else:
            st.error("As saídas diferem. O comportamento não foi preservado para esta entrada.")
    else:
        st.markdown(
            '<div class="section-note">Escolhe um cenário e executa a comparação para ver o resultado produzido pelo código.</div>',
            unsafe_allow_html=True,
        )


elif pagina == "Comparação do código":
    cabecalho(
        "Comparação do código",
        "Os blocos abaixo são lidos directamente dos módulos que o simulador e os testes executam.",
    )
    exemplo, extensao = st.tabs(["Exemplo principal · Extrair Método", "Extensão · Reutilização"])
    with exemplo:
        st.markdown(
            '<div class="section-note">No exemplo do trabalho, a versão original funciona. '
            'A refatorada separa a notificação para tornar a responsabilidade explícita.</div>',
            unsafe_allow_html=True,
        )
        original, refatorado = st.columns(2)
        with original:
            st.markdown("#### Versão original")
            st.code(fonte("implementacoes/exemplo_original.py"), language="python", line_numbers=True)
        with refatorado:
            st.markdown("#### Versão refatorada")
            st.code(fonte("implementacoes/exemplo_refatorado.py"), language="python", line_numbers=True)
        st.write("`notificar_admin` dá um nome à acção de notificar. `processar_usuario` continua a decidir quando essa acção deve ocorrer.")
    with extensao:
        st.info("Exemplo adicional: a extensão acrescenta o processamento de relatórios; não faz parte do código exacto do exemplo académico.")
        original, refatorado = st.columns(2)
        with original:
            st.markdown("#### Repetição na versão original")
            st.code(fonte("implementacoes/extensao_original.py"), language="python", line_numbers=True)
        with refatorado:
            st.markdown("#### Função reutilizada")
            st.code(fonte("implementacoes/extensao_refatorada.py"), language="python", line_numbers=True)
        st.write("Na versão original, o mesmo `print` aparece nas duas operações. Na versão refatorada, ambas chamam uma única função de notificação.")


elif pagina == "Testes":
    cabecalho(
        "Testes automatizados",
        "A suite usa unittest e verifica as saídas realmente produzidas pelas funções Python.",
    )
    st.write("Inclui administradores e utilizadores comuns no exemplo principal e na extensão, além de comparações directas entre as versões.")
    if st.button("Executar testes", type="primary"):
        try:
            st.session_state["resultado_testes"] = executar_suite_de_testes()
        except Exception as erro:
            st.session_state["erro_testes"] = f"{type(erro).__name__}: {erro}"
            st.session_state.pop("resultado_testes", None)
        else:
            st.session_state.pop("erro_testes", None)

    if st.session_state.get("erro_testes"):
        st.error(f"Não foi possível executar a suite: {st.session_state['erro_testes']}")
    resultado = st.session_state.get("resultado_testes")
    if resultado:
        aprovados = resultado["executados"] - resultado["falhas"]
        metricas = st.columns(3)
        metricas[0].metric("Testes executados", resultado["executados"])
        metricas[1].metric("Aprovados", aprovados)
        metricas[2].metric("Falhados", resultado["falhas"])
        if resultado["falhas"] == 0:
            st.success(f"Suite concluída: {aprovados} de {resultado['executados']} testes aprovados.")
        else:
            st.error(f"Suite concluída com {resultado['falhas']} teste(s) falhado(s).")
        for registo in resultado["registos"]:
            simbolo = "✓" if registo["aprovado"] else "✗"
            with st.expander(f"{simbolo} {registo['nome']}", expanded=not registo["aprovado"]):
                st.markdown("**Resultado esperado**")
                st.code(registo["esperado"], language="text")
                st.markdown("**Resultado obtido**")
                st.code(registo["obtido"], language="text")
                st.caption("Estado: aprovado" if registo["aprovado"] else "Estado: falhado")
                if registo["erro"]:
                    st.code(registo["erro"], language="text")
    else:
        st.markdown(
            '<div class="section-note">Os resultados só aparecem depois de executar a suite.</div>',
            unsafe_allow_html=True,
        )


elif pagina == "Qualidade":
    cabecalho(
        "Análise da qualidade do código",
        "A refatoração altera a organização. Os efeitos devem ser explicados com precisão, sem notas ou métricas inventadas.",
    )
    st.markdown("#### Legibilidade")
    st.write("`notificar_admin` torna explícito o que a função auxiliar faz. Quem lê `processar_usuario` consegue distinguir a decisão da acção chamada.")
    st.markdown("#### Manutenibilidade")
    st.write("Na extensão, a forma de emitir a notificação está num único local. Uma alteração nessa acção pode ser feita na função partilhada.")
    st.markdown("#### Reutilização")
    st.write("A operação de utilizador e a operação de relatório podem chamar a mesma `notificar_admin`, sem repetir a instrução de notificação.")
    st.markdown("#### Eficiência")
    st.write("Este exemplo procura melhorar a estrutura e a manutenção. Não demonstra uma aceleração da execução nem uma redução do consumo de memória.")
    st.markdown("#### Confiabilidade")
    st.write("Os testes executam as funções e verificam as saídas. A igualdade entre versões é confirmada para os cenários cobertos pela suite.")


elif pagina == "Conceitos":
    cabecalho(
        "Conceitos de refatoração",
        "Um code smell é um sinal de que a estrutura merece atenção; por si só, não prova que o programa esteja funcionalmente errado.",
    )
    st.markdown("### Code smells")
    st.markdown("- **Métodos demasiado longos:** juntam etapas diferentes e tornam a leitura e a alteração mais difíceis.\n- **Lógica duplicada:** a mesma regra aparece em vários locais e pode divergir quando é alterada.\n- **Nomes pouco claros:** escondem a intenção do código.\n- **Condicionais complexas:** acumulam decisões difíceis de seguir.")
    st.markdown("### Técnicas de refatoração")
    st.markdown("- **Extrair Método:** mover uma responsabilidade para uma função com nome claro.\n- **Eliminar duplicação:** centralizar uma regra repetida e reutilizá-la.\n- **Renomear elementos:** escolher nomes que descrevem a intenção.\n- **Simplificar condicionais:** tornar as decisões mais directas.\n- **Usar cláusulas de guarda:** tratar condições de saída cedo quando isso clarifica o fluxo.")
    st.markdown("### Exemplos pequenos em Python")
    tab1, tab2, tab3 = st.tabs(["Extrair Método", "Renomear", "Simplificar condicional"])
    with tab1:
        st.code('def processar(pedido):\n    validar(pedido)\n    total = calcular_total(pedido)\n    guardar(total)\n\n# Uma etapa pode ganhar uma função própria:\ndef calcular_total(pedido):\n    return sum(item["preco"] for item in pedido["itens"])', language="python")
        st.caption("Separar uma etapa ajuda a dar-lhe um nome, testar e reutilizar.")
    with tab2:
        st.code('def proc(x):\n    return x["preco"] * x["qtd"]\n\n# Nome mais claro:\ndef calcular_subtotal(item):\n    return item["preco"] * item["quantidade"]', language="python")
        st.caption("O nome descreve a intenção e reduz a necessidade de comentários explicativos.")
    with tab3:
        st.code('def pode_aceder(usuario):\n    if not usuario["ativo"]:\n        return False\n    if not usuario["admin"]:\n        return False\n    return True', language="python")
        st.caption("Cláusulas de guarda deixam as condições de saída visíveis antes do caminho principal.")
