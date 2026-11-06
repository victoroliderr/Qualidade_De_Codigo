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
    badge,
    code_block,
    editor_header,
    diff_html,
    table as tabela,
    callout,
    ler_codigo,
)

carregar_css()

hero(
    "Painéis Before / After",
    "Comparação de código",
    "Os dois painéis são preenchidos a partir dos ficheiros reais do projecto. O diff é calculado em tempo de execução.",
    ["pedido_original.py", "pedido_refatorado.py", "diff real"],
)

codigo_original = ler_codigo("pedido_original.py")
codigo_refatorado = ler_codigo("pedido_refatorado.py")

modo = st.segmented_control(
    "Vista",
    ["Lado a lado", "Original", "Refatorado", "Diferenças"],
    default="Lado a lado",
    key="vista_comparacao",
)

if modo == "Lado a lado":
    col_orig, col_ref = st.columns(2, gap="medium")
    with col_orig:
        code_block(codigo_original, filename="pedido_original.py", label="BEFORE")
    with col_ref:
        code_block(codigo_refatorado, filename="pedido_refatorado.py", label="AFTER")

elif modo == "Original":
    code_block(codigo_original, filename="pedido_original.py", label="BEFORE")

elif modo == "Refatorado":
    code_block(codigo_refatorado, filename="pedido_refatorado.py", label="AFTER")

else:
    st.markdown(
        f'<div class="cl-pill-row">{badge("Linhas retiradas / substituídas", "red")}'
        f'{badge("Linhas novas", "green")}{badge("Contexto mantido", "blue")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(diff_html(codigo_original, codigo_refatorado), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
section_title("Leitura estrutural", "A mesma responsabilidade global, distribuída de forma diferente.")

tabela(
    ["Aspecto", "Código original", "Código refatorado"],
    [
        ["Organização", "Uma função central", "Quatro funções com papéis definidos"],
        ["Cálculo", "Integrado no corpo de <code>processar_pedido</code>", "Isolado em <code>calcular_valor_base</code>"],
        ["Descontos", "<code>if/elif</code> com multiplicadores embutidos", "Dicionário <code>taxas_desconto</code> + <code>.get()</code>"],
        ["Fatura", "Integrada na mesma função", "Isolada em <code>emitir_fatura_impressa</code>"],
        ["Coordenação", "Misturada com o cálculo", "<code>processar_pedido</code> apenas orquestra"],
        ["Extensibilidade", "Exige alterar o condicional", "Exige acrescentar uma entrada ao dicionário"],
    ],
)

section_title("As quatro funções da versão refatorada", "Cada função tem uma responsabilidade explícita.")
f1, f2, f3, f4 = st.columns(4, gap="medium")
with f1:
    card("calcular_valor_base", "Percorre os itens e devolve a soma de preço × quantidade. Não conhece descontos nem faturas.", "accent", "01", "Cálculo")
with f2:
    card("aplicar_desconto_cliente", "Consulta a taxa no dicionário e aplica-a ao valor base. Um tipo desconhecido recebe 0%.", "violet", "02", "Regra")
with f3:
    card("emitir_fatura_impressa", "Apresenta cliente e total no formato da fatura. Não calcula valores.", "green", "03", "Saída")
with f4:
    card("processar_pedido", "Coordena as três funções anteriores e devolve o total com desconto.", "amber", "04", "Coordenação")

st.markdown("<br>", unsafe_allow_html=True)
callout(
    "<strong>Técnica principal demonstrada:</strong> <em>Extrair Método</em>. "
    "O corpo da função original foi dividido em funções pequenas com nomes que explicam a "
    "responsabilidade. A tabela de descontos é uma melhoria adicional de organização de regras, "
    "identificada separadamente do exemplo académico.",
    "violet",
)

st.markdown("<br>", unsafe_allow_html=True)
with st.expander("Legenda do diff"):
    st.markdown(
        "- **Fundo vermelho discreto** — linha retirada ou substituída na versão refatorada.\n"
        "- **Fundo verde discreto** — linha nova introduzida na versão refatorada.\n"
        "- **Linhas cinzentas** — contexto mantido entre as duas versões.\n"
        "- **Cabeçalho azul (`@@`)** — localização do bloco alterado no ficheiro."
    )
