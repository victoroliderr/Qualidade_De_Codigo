from __future__ import annotations

import copy
import io
import json
import math
import sys
import time
from contextlib import redirect_stdout
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
    badge,
    stepper,
    result_panel,
    callout,
    console,
    code_block,
    table as tabela,
)
from implementacoes import pedido_original, pedido_refatorado

carregar_css()

TIPOS = ["COMUM", "VIP", "PREMIUM"]

PRESETS = {
    "comum": {
        "cliente": "João Silva",
        "tipo": "COMUM",
        "itens": [{"nome": "Produto A", "preco": 50.0, "quantidade": 2}],
    },
    "vip": {
        "cliente": "Maria Santos",
        "tipo": "VIP",
        "itens": [{"nome": "Produto A", "preco": 100.0, "quantidade": 1}],
    },
    "premium": {
        "cliente": "Empresa XYZ",
        "tipo": "PREMIUM",
        "itens": [{"nome": "Produto A", "preco": 200.0, "quantidade": 1}],
    },
}


def formatar_real(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def limpar_chaves_produtos():
    for chave in list(st.session_state):
        if chave.startswith("prod_"):
            del st.session_state[chave]


def proximo_id() -> int:
    identificador = st.session_state.contador_produto
    st.session_state.contador_produto = identificador + 1
    return identificador


def aplicar_preset(chave: str):
    preset = PRESETS[chave]
    limpar_chaves_produtos()
    st.session_state.cliente_nome = preset["cliente"]
    st.session_state.cliente_tipo = preset["tipo"]
    st.session_state.produtos = [
        {
            "id": proximo_id(),
            "nome": item["nome"],
            "preco": item["preco"],
            "quantidade": item["quantidade"],
        }
        for item in preset["itens"]
    ]
    st.session_state.resultado_comparacao = None


def adicionar_produto():
    novo_id = proximo_id()
    st.session_state.produtos.append(
        {"id": novo_id, "nome": "Novo produto", "preco": 10.0, "quantidade": 1}
    )


def remover_produto(produto_id: int):
    st.session_state.produtos = [
        item for item in st.session_state.produtos if item["id"] != produto_id
    ]
    for sufixo in ("nome", "preco", "qtd"):
        chave = f"prod_{sufixo}_{produto_id}"
        if chave in st.session_state:
            del st.session_state[chave]
    st.session_state.resultado_comparacao = None


if "contador_produto" not in st.session_state:
    st.session_state.contador_produto = 0
if "produtos" not in st.session_state:
    aplicar_preset("comum")
if "resultado_comparacao" not in st.session_state:
    st.session_state.resultado_comparacao = None

hero(
    "Laboratório prático · Etapas 01—03",
    "Processamento de pedidos",
    "Configura um pedido, executa as duas implementações com os mesmos dados e confirma que o comportamento externo foi preservado.",
    ["Código real", "Execução real", "pytest"],
)

tem_resultado = st.session_state.resultado_comparacao is not None
stepper(
    [
        ("Configurar pedido", "Cliente e produtos"),
        ("Executar", "Original + refatorado"),
        ("Comparar", "Valores, faturas e estado"),
    ],
    active=3 if tem_resultado else 1,
)

section_title("Etapa 01 · Configurar pedido", "Escolhe um exemplo do relatório ou constrói o teu próprio pedido.")

st.markdown(
    f'<div class="cl-pill-row">{badge("Exemplos do relatório", "violet")}'
    f'<span class="cl-small cl-muted">Os três casos oficiais produzem R$ 100,00, R$ 90,00 e R$ 170,00.</span></div>',
    unsafe_allow_html=True,
)

p1, p2, p3, p4 = st.columns([1, 1, 1, 1.2], gap="small")
with p1:
    st.button("COMUM · R$ 100", key="preset_comum", use_container_width=True, on_click=aplicar_preset, args=("comum",))
with p2:
    st.button("VIP · R$ 90", key="preset_vip", use_container_width=True, on_click=aplicar_preset, args=("vip",))
with p3:
    st.button("PREMIUM · R$ 170", key="preset_premium", use_container_width=True, on_click=aplicar_preset, args=("premium",))
with p4:
    st.button("Adicionar produto", key="preset_limpar", use_container_width=True, on_click=adicionar_produto)

with st.container(border=True):
    col_cliente, col_tipo = st.columns([1.6, 1], gap="medium")
    with col_cliente:
        st.text_input("Nome do cliente", key="cliente_nome", placeholder="Ex.: João Silva")
    with col_tipo:
        st.selectbox(
            "Tipo de cliente",
            TIPOS,
            key="cliente_tipo",
            help="COMUM: 0% · VIP: 10% · PREMIUM: 15%",
        )

    st.markdown(
        f'<div class="cl-pill-row">{badge("Itens do pedido", "blue")}'
        f'<span class="cl-small cl-muted">Nome do produto, preço unitário e quantidade.</span></div>',
        unsafe_allow_html=True,
    )

    for indice, produto in enumerate(list(st.session_state.produtos)):
        pid = produto["id"]
        c_nome, c_preco, c_qtd, c_remover = st.columns([2.6, 1.2, 1, 0.8], gap="small")
        with c_nome:
            chave = f"prod_nome_{pid}"
            extra = {} if chave in st.session_state else {"value": produto["nome"]}
            st.text_input("Produto", key=chave, placeholder="Nome do produto", **extra)
        with c_preco:
            chave = f"prod_preco_{pid}"
            extra = {} if chave in st.session_state else {"value": float(produto["preco"])}
            st.number_input("Preço (R$)", key=chave, min_value=0.0, step=1.0, format="%.2f", **extra)
        with c_qtd:
            chave = f"prod_qtd_{pid}"
            extra = {} if chave in st.session_state else {"value": int(produto["quantidade"])}
            st.number_input("Qtd.", key=chave, min_value=1, step=1, **extra)
        with c_remover:
            st.markdown("<div style='height:1.55rem'></div>", unsafe_allow_html=True)
            st.button(
                "Remover",
                key=f"remover_{pid}",
                use_container_width=True,
                on_click=remover_produto,
                args=(pid,),
            )

itens_execucao = []
itens_tabela = []
for produto in st.session_state.produtos:
    pid = produto["id"]
    nome = st.session_state.get(f"prod_nome_{pid}", produto["nome"]) or "Produto sem nome"
    preco = float(st.session_state.get(f"prod_preco_{pid}", produto["preco"]))
    quantidade = int(st.session_state.get(f"prod_qtd_{pid}", produto["quantidade"]))
    itens_execucao.append({"preco": preco, "quantidade": quantidade})
    itens_tabela.append([nome, formatar_real(preco), str(quantidade), formatar_real(preco * quantidade)])

tabela(["Produto", "Preço unitário", "Quantidade", "Subtotal"], itens_tabela)

valor_base_visual = sum(item["preco"] * item["quantidade"] for item in itens_execucao)
st.markdown(
    f'<div class="cl-callout"><strong>Valor base do pedido:</strong> {formatar_real(valor_base_visual)} '
    f'· <strong>Cliente:</strong> {st.session_state.cliente_nome or "Sem nome"} '
    f'· <strong>Tipo:</strong> {st.session_state.cliente_tipo}</div>',
    unsafe_allow_html=True,
)

pedido_execucao = {
    "cliente": st.session_state.cliente_nome,
    "tipo_cliente": st.session_state.cliente_tipo,
    "itens": itens_execucao,
}

with st.expander("Ver os dados exactos enviados às implementações"):
    code_block(
        json.dumps(pedido_execucao, ensure_ascii=False, indent=2),
        filename="pedido_execucao.json",
        language="json",
    )

section_title("Etapa 02 · Executar", "As duas implementações recebem cópias independentes do mesmo pedido.")

st.markdown(
    '<div class="cl-flow">'
    '<span class="cl-flow-node">PEDIDO</span><span class="cl-flow-arrow">→</span>'
    '<span class="cl-flow-node">pedido_original.py</span><span class="cl-flow-arrow">↔</span>'
    '<span class="cl-flow-node">pedido_refatorado.py</span><span class="cl-flow-arrow">→</span>'
    '<span class="cl-flow-node highlight">COMPARAÇÃO</span></div>',
    unsafe_allow_html=True,
)

executar = st.button("EXECUTAR COMPARAÇÃO", type="primary", use_container_width=True)


def executar_implementacao(funcao, pedido):
    saida = io.StringIO()
    inicio = time.perf_counter()
    with redirect_stdout(saida):
        try:
            valor = funcao(copy.deepcopy(pedido))
            erro = None
        except Exception as excecao:  # pragma: no cover - apresentado na interface
            valor = None
            erro = f"{type(excecao).__name__}: {excecao}"
    duracao = (time.perf_counter() - inicio) * 1000
    return {"valor": valor, "fatura": saida.getvalue(), "erro": erro, "duracao_ms": duracao}


if executar:
    resultado_original = executar_implementacao(pedido_original.processar_pedido, pedido_execucao)
    resultado_refatorado = executar_implementacao(pedido_refatorado.processar_pedido, pedido_execucao)
    valores_iguais = (
        resultado_original["valor"] is not None
        and resultado_refatorado["valor"] is not None
        and math.isclose(resultado_original["valor"], resultado_refatorado["valor"], rel_tol=1e-9, abs_tol=1e-9)
    )
    faturas_iguais = resultado_original["fatura"] == resultado_refatorado["fatura"]
    preservado = valores_iguais and faturas_iguais and not resultado_original["erro"] and not resultado_refatorado["erro"]
    st.session_state.resultado_comparacao = {
        "original": resultado_original,
        "refatorado": resultado_refatorado,
        "valores_iguais": valores_iguais,
        "faturas_iguais": faturas_iguais,
        "preservado": preservado,
        "pedido": pedido_execucao,
    }
    st.rerun()

resultado = st.session_state.resultado_comparacao

if resultado is None:
    st.markdown(
        '<div class="cl-empty">Ainda não existe execução. Configura o pedido e clica em '
        "<strong>EXECUTAR COMPARAÇÃO</strong>.</div>",
        unsafe_allow_html=True,
    )
else:
    section_title("Etapa 03 · Comparar", "Valores devolvidos, fatura emitida e estado de cada execução.")
    original = resultado["original"]
    refatorado = resultado["refatorado"]

    col_orig, col_ref = st.columns(2, gap="medium")
    with col_orig:
        result_panel(
            "VERSÃO ORIGINAL",
            formatar_real(original["valor"]) if original["valor"] is not None else "Sem valor",
            original["fatura"] if original["fatura"] else (original["erro"] or "Sem saída."),
            "ok" if original["erro"] is None else "erro",
        )
    with col_ref:
        result_panel(
            "VERSÃO REFATORADA",
            formatar_real(refatorado["valor"]) if refatorado["valor"] is not None else "Sem valor",
            refatorado["fatura"] if refatorado["fatura"] else (refatorado["erro"] or "Sem saída."),
            "ok" if refatorado["erro"] is None else "erro",
        )

    st.markdown("<br>", unsafe_allow_html=True)
    if resultado["preservado"]:
        st.markdown(
            '<div class="cl-callout success"><strong>COMPORTAMENTO PRESERVADO</strong><br>'
            "As duas implementações devolveram o mesmo valor e produziram exactamente a mesma "
            "fatura para o mesmo pedido.</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="cl-callout danger"><strong>COMPARAÇÃO NÃO VALIDADA</strong><br>'
            "Os resultados divergiram. A refatoração não pode ser considerada equivalente "
            "para este pedido sem uma análise adicional.</div>",
            unsafe_allow_html=True,
        )

    r1, r2, r3, r4 = st.columns(4, gap="medium")
    with r1:
        st.metric("Valor original", formatar_real(original["valor"]) if original["valor"] is not None else "—")
    with r2:
        st.metric("Valor refatorado", formatar_real(refatorado["valor"]) if refatorado["valor"] is not None else "—")
    with r3:
        st.metric("Faturas iguais", "Sim" if resultado["faturas_iguais"] else "Não")
    with r4:
        st.metric("Tempo total", f"{(original['duracao_ms'] + refatorado['duracao_ms']):.2f} ms")

    with st.expander("O que aconteceu nesta execução?"):
        st.markdown(
            "1. O pedido foi copiado para duas estruturas independentes.\n"
            "2. A versão original calculou o total, aplicou o desconto com `if/elif` e imprimiu a fatura.\n"
            "3. A versão refatorada delegou o cálculo, o desconto e a fatura em três funções e coordenou-as em `processar_pedido`.\n"
            "4. O `print` foi capturado com `io.StringIO` e `contextlib.redirect_stdout`.\n"
            "5. Os valores e as faturas foram comparados sem simulação."
        )
        console(
            "ORIGINAL >>\n"
            + (original["fatura"] or "(sem saída)")
            + "\nREFATORADO >>\n"
            + (refatorado["fatura"] or "(sem saída)")
        )

    st.markdown("<br>", unsafe_allow_html=True)
    c_ver, c_testes, _ = st.columns([1.1, 1.1, 1.8])
    with c_ver:
        if st.button("Ver comparação de código", use_container_width=True):
            st.switch_page("pages/03_Comparacao.py")
    with c_testes:
        if st.button("Executar testes", use_container_width=True):
            st.switch_page("pages/04_Testes.py")

st.markdown("<br>", unsafe_allow_html=True)
section_title("Porque é que a comparação é verdadeira", "A interface usa exactamente os módulos do projecto.")
c1, c2, c3 = st.columns(3, gap="medium")
with c1:
    card("Módulos reais", "A execução importa pedido_original.py e pedido_refatorado.py; não existe uma segunda implementação escondida na interface.", "accent", "PY")
with c2:
    card("Dados independentes", "Cada versão recebe uma cópia profunda do pedido, evitando que uma execução altere a outra.", "violet", "CP")
with c3:
    card("Saída capturada", "O texto da fatura é recolhido com StringIO e redirect_stdout antes de ser comparado.", "green", "IO")
