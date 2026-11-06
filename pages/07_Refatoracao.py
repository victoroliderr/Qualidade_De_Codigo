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
    flow,
    code_block,
    table as tabela,
)

carregar_css()

hero(
    "Conceito · Técnicas · Dupla alternância",
    "Técnicas de Refatoração",
    "Refatorar é alterar a estrutura interna de um sistema de software sem modificar o seu comportamento externo observado.",
    ["Martin Fowler", "Extrair Método", "4 técnicas"],
)

st.markdown(
    '<div class="cl-quote">“Refactoring is the process of changing a software system in such a way '
    "that it does not alter the external behavior of the code yet improves its internal structure.”"
    "<br><strong>— Martin Fowler, Refactoring: Improving the Design of Existing Code</strong></div>",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)
section_title("O que muda — e o que não muda", "A estrutura interna melhora; o resultado observado permanece.")
flow(
    [
        "Estrutura original",
        "Aplicação de técnicas",
        "Estrutura interna melhorada",
        "Mesmo comportamento externo",
    ],
    highlight=2,
)

c1, c2 = st.columns(2, gap="medium")
with c1:
    card("O que a refatoração faz", "Reorganiza funções, nomes, condicionais e dependências para tornar o código mais legível e fácil de manter.", "accent", "✓")
with c2:
    card("O que a refatoração não faz", "Não acrescenta funcionalidades, não altera regras de negócio e não muda o resultado devolvido ao utilizador.", "red", "✕")

st.markdown("<br>", unsafe_allow_html=True)
section_title("Princípio da dupla alternância", "Duas actividades distintas, executadas em etapas separadas.")
d1, d2 = st.columns(2, gap="medium")
with d1:
    card("1 · Refatorar", "Melhorar a estrutura sem adicionar novas funcionalidades. O comportamento é preservado e validado pelos testes.", "violet", "R")
with d2:
    card("2 · Adicionar funcionalidade", "Introduzir comportamento novo numa etapa própria, já sobre uma estrutura mais clara.", "green", "F")
callout(
    "<strong>Porque separar?</strong> Se a estrutura e o comportamento mudarem ao mesmo tempo, "
    "deixa de ser possível saber qual alteração causou uma regressão. A dupla alternância mantém "
    "a refatoração verificável.",
    "violet",
)

st.markdown("<br>", unsafe_allow_html=True)
section_title("Técnicas apresentadas no relatório", "Exemplos pequenos em Python para cada técnica.")

tecnicas = st.tabs(
    [
        "Extrair Método",
        "Eliminar Duplicação",
        "Renomear Elementos",
        "Simplificar Condicionais",
    ]
)

with tecnicas[0]:
    st.markdown(
        f'<div class="cl-pill-row">{badge("Aplicada no exemplo da loja virtual", "green")}'
        f'{badge("Técnica principal demonstrada", "blue")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='cl-lead'>Transformar uma parte de uma função numa função independente, com um "
        "nome que explique a sua responsabilidade.</p>",
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        code_block(
            """def processar_pedido(pedido):
    total = 0
    for item in pedido['itens']:
        total += item['preco'] * item['quantidade']

    if pedido['tipo_cliente'] == 'VIP':
        total = total * 0.90

    print(f"Total: R$ {total:.2f}")
    return total""",
            filename="antes.py",
            label="ANTES",
        )
    with c2:
        code_block(
            """def calcular_valor_base(itens):
    return sum(item['preco'] * item['quantidade']
               for item in itens)

def processar_pedido(pedido):
    total = calcular_valor_base(pedido['itens'])
    if pedido['tipo_cliente'] == 'VIP':
        total = total * 0.90

    print(f"Total: R$ {total:.2f}")
    return total""",
            filename="depois.py",
            label="DEPOIS",
        )
    card("No projecto", "A versão refatorada extrai calcular_valor_base, aplicar_desconto_cliente e emitir_fatura_impressa. processar_pedido passa a coordenar.", "accent", "01")

with tecnicas[1]:
    st.markdown(
        f'<div class="cl-pill-row">{badge("Explicada teoricamente", "violet")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='cl-lead'>Centralizar lógica repetida para evitar manter várias implementações "
        "do mesmo comportamento. Substitute Algorithm substitui uma implementação por outra mais "
        "clara; Pull Up Method move comportamento comum para um nível superior.</p>",
        unsafe_allow_html=True,
    )
    code_block(
        """def aplicar_taxa_expresso(pedido):
    pedido["total"] += TAXA_EXPRESSO

def processar_encomenda_normal(pedido):
    if pedido["expresso"]:
        aplicar_taxa_expresso(pedido)

def processar_encomenda_oferta(pedido):
    if pedido["expresso"]:
        aplicar_taxa_expresso(pedido)""",
        filename="duplicacao_eliminada.py",
        label="EXEMPLO TEÓRICO",
    )
    card("Resultado", "Uma única função concentra a regra. Os dois fluxos reutilizam-na e passam a partilhar o mesmo comportamento.", "green", "02")

with tecnicas[2]:
    st.markdown(
        f'<div class="cl-pill-row">{badge("Explicada teoricamente", "violet")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='cl-lead'>Substituir nomes pouco claros por nomes que expliquem a função das "
        "variáveis, funções e classes.</p>",
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        code_block(
            """def calc(p, t):
    x = 0
    for i in p:
        x += i['preco'] * i['quantidade']
    if t == 'VIP':
        x = x * 0.90
    return x""",
            filename="antes.py",
            label="ANTES",
        )
    with c2:
        code_block(
            """def calcular_total_com_desconto(itens, tipo_cliente):
    valor_base = 0
    for item in itens:
        valor_base += item['preco'] * item['quantidade']
    if tipo_cliente == 'VIP':
        valor_base = valor_base * 0.90
    return valor_base""",
            filename="depois.py",
            label="DEPOIS",
        )
    card("Resultado", "O nome da função, dos parâmetros e da variável passa a revelar a intenção, reduzindo a necessidade de comentários.", "green", "03")

with tecnicas[3]:
    st.markdown(
        f'<div class="cl-pill-row">{badge("Relacionada com o exemplo", "green")}'
        f'{badge("Explicada teoricamente", "violet")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='cl-lead'>Decompor expressões complexas ou utilizar cláusulas de guarda para "
        "tornar o fluxo mais simples e linear.</p>",
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        code_block(
            """def pode_faturar(cliente, total):
    if cliente is not None:
        if total > 0:
            if cliente['ativo']:
                return True
    return False""",
            filename="antes.py",
            label="ANTES",
        )
    with c2:
        code_block(
            """def pode_faturar(cliente, total):
    if cliente is None:
        return False
    if total <= 0:
        return False
    return cliente['ativo']""",
            filename="depois.py",
            label="DEPOIS",
        )
    card("No exemplo da loja virtual", "As regras de desconto passam de if/elif para um dicionário com valor por omissão. É uma forma de simplificar e tornar o condicional extensível.", "accent", "04")

st.markdown("<br>", unsafe_allow_html=True)
section_title("Técnica demonstrada vs técnicas explicadas", "O rigor exige distinguir o que foi realmente aplicado.")
tabela(
    ["Técnica", "Estado no laboratório", "Onde observar"],
    [
        ["Extrair Método", "Aplicada ao exemplo da loja virtual", "pedido_refatorado.py · três funções extraídas"],
        ["Tabela de regras (dicionário)", "Melhoria adicional identificada", "aplicar_desconto_cliente"],
        ["Eliminar duplicação", "Explicada teoricamente", "Separador Eliminar Duplicação"],
        ["Renomear elementos", "Explicada teoricamente", "Separador Renomear Elementos"],
        ["Simplificar condicionais", "Relacionada e explicada", "Separador Simplificar Condicionais"],
    ],
)

st.markdown("<br>", unsafe_allow_html=True)
section_title(
    "Boas práticas de refatoração",
    "Refatorar é uma actividade incremental — não uma reescrita total.",
    eyebrow="Boas práticas",
)
b1, b2 = st.columns(2, gap="medium")
with b1:
    card(
        "Regra do Escoteiro",
        "Deixar o código um pouco mais organizado do que o encontrámos. Pequenas melhorias contínuas evitam a acumulação de dívida técnica.",
        "green",
        "RE",
    )
with b2:
    card(
        "Refatoração incremental",
        "Aplicar uma transformação pequena, executar os testes, confirmar o comportamento e só depois avançar para a transformação seguinte.",
        "accent",
        "IN",
    )

st.markdown("<br>", unsafe_allow_html=True)
section_title("Ambientes de desenvolvimento integrados", "Ferramentas que automatizam transformações mecânicas com segurança.")
i1, i2, i3 = st.columns(3, gap="medium")
with i1:
    card("Visual Studio Code", "Suporte a renomear símbolos, extrair variáveis e métodos, navegar por referências e executar testes integrados.", "accent", "VS")
with i2:
    card("IntelliJ IDEA", "Refatorações assistidas para renomear, extrair métodos, mover elementos e reorganizar a estrutura do projecto.", "violet", "IJ")
with i3:
    card("Eclipse", "Ferramentas de refactoring para renomear, extrair métodos e organizar imports, com verificação de referências.", "green", "EC")

callout(
    "<strong>Antes e depois de cada transformação:</strong> executar a suíte de testes. "
    "A ferramenta ajuda a manter a estrutura consistente; os testes confirmam que o "
    "comportamento observado não mudou.",
    "violet",
)
