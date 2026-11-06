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
    code_block,
    table as tabela,
)

carregar_css()

hero(
    "Galeria interactiva · 5 categorias",
    "Code Smells",
    "Um code smell é um sinal de que a estrutura interna pode estar a dificultar a compreensão e a evolução do código — mesmo quando os testes passam.",
    ["Long Method", "Duplicated Code", "Complex Conditional", "Large Class", "Long Parameter List"],
)

st.markdown(
    f'<div class="cl-pill-row">{badge("Identificados na loja virtual", "green")}'
    f'{badge("Exemplos teóricos de aprendizagem", "violet")}</div>',
    unsafe_allow_html=True,
)

callout(
    "<strong>Distinção importante:</strong> no exemplo da loja virtual foram identificados "
    "método longo com responsabilidade múltipla, condicionais pouco extensíveis e valores "
    "directamente incorporados no código. Duplicação de código, classes grandes e listas de "
    "parâmetros longas são apresentadas aqui como exemplos teóricos — não como problemas "
    "encontrados nesse exemplo.",
    "violet",
)

section_title("Explorar a galeria", "Cada separador apresenta definição, exemplo, problema e técnica de correção.")

separadores = st.tabs(
    [
        "Métodos Longos",
        "Duplicação de Código",
        "Condicionais Complexas",
        "Classes Grandes",
        "Parâmetros Longos",
    ]
)

with separadores[0]:
    st.markdown(
        f'<div class="cl-pill-row">{badge("Identificado no exemplo da loja virtual", "green")}</div>',
        unsafe_allow_html=True,
    )
    section_title("Long Method", "Funções que acumulam responsabilidades excessivas.")
    st.markdown(
        "<p class='cl-lead'>A função faz demasiadas coisas ao mesmo tempo. Quando um método cresce, "
        "o leitor precisa de manter vários níveis de detalhe na memória e os testes tornam-se mais "
        "difíceis de isolar.</p>",
        unsafe_allow_html=True,
    )
    code_block(
        """def processar_pedido(pedido):
    total = 0
    for item in pedido['itens']:
        total += item['preco'] * item['quantidade']

    if pedido['tipo_cliente'] == 'VIP':
        total = total * 0.90
    elif pedido['tipo_cliente'] == 'PREMIUM':
        total = total * 0.85

    print("----- FATURA -----")
    print(f"Cliente: {pedido['cliente']}")
    print(f"Total a pagar: R$ {total:.2f}")
    print("------------------")
    return total""",
        filename="exemplo_loja_virtual.py",
        label="NO EXEMPLO",
    )
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        card("Problema causado", "Cálculo, aplicação de desconto e emissão de fatura ficam acoplados. Alterar a fatura obriga a mexer no cálculo.", "red", "P")
    with c2:
        card("Técnica de refatoração", "Extrair Método: dividir o corpo em calcular_valor_base, aplicar_desconto_cliente e emitir_fatura_impressa.", "green", "T")

with separadores[1]:
    st.markdown(
        f'<div class="cl-pill-row">{badge("Exemplo teórico", "violet")}</div>',
        unsafe_allow_html=True,
    )
    section_title("Duplicated Code", "Blocos de instruções repetidos em diferentes locais.")
    st.markdown(
        "<p class='cl-lead'>A mesma regra aparece copiada em vários pontos. Uma correcção futura "
        "tem de ser replicada em todos eles; se um local for esquecido, as cópias divergem.</p>",
        unsafe_allow_html=True,
    )
    code_block(
        """def processar_encomenda_normal(pedido):
    if pedido["expresso"]:
        pedido["total"] += TAXA_EXPRESSO

def processar_encomenda_oferta(pedido):
    if pedido["expresso"]:
        pedido["total"] += TAXA_EXPRESSO""",
        filename="duplicacao_teorica.py",
        label="EXEMPLO TEÓRICO",
    )
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        card("Problema causado", "Manutenção em múltiplos locais e risco de comportamento inconsistente entre cópias.", "red", "P")
    with c2:
        card("Técnica de refatoração", "Substitute Algorithm / Pull Up Method: centralizar a lógica repetida numa única função reutilizável.", "green", "T")

with separadores[2]:
    st.markdown(
        f'<div class="cl-pill-row">{badge("Identificado no exemplo da loja virtual", "green")}</div>',
        unsafe_allow_html=True,
    )
    section_title("Complex Conditional", "Estruturas condicionais profundas ou difíceis de acompanhar.")
    st.markdown(
        "<p class='cl-lead'>Condicionais encadeadas escondem regras de negócio e obrigam a alterar "
        "o mesmo bloco sempre que surge um novo caso. A lógica fica extensível apenas por edição "
        "do código existente.</p>",
        unsafe_allow_html=True,
    )
    code_block(
        """if pedido['tipo_cliente'] == 'VIP':
    total = total * 0.90
elif pedido['tipo_cliente'] == 'PREMIUM':
    total = total * 0.85
# Um novo tipo obriga a acrescentar outro elif.""",
        filename="condicional_loja_virtual.py",
        label="NO EXEMPLO",
    )
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        card("Problema causado", "Cada novo tipo de cliente exige uma alteração no condicional e aumenta o risco de esquecer um caso.", "red", "P")
    with c2:
        card("Técnica de refatoração", "Decompose Conditional / tabela de regras: usar um dicionário de taxas e uma consulta com valor por omissão.", "green", "T")

with separadores[3]:
    st.markdown(
        f'<div class="cl-pill-row">{badge("Exemplo teórico", "violet")}</div>',
        unsafe_allow_html=True,
    )
    section_title("Large Class", "Classes que tentam assumir demasiadas responsabilidades.")
    st.markdown(
        "<p class='cl-lead'>Uma classe acumula operações de domínios diferentes. Torna-se difícil "
        "de testar, de reutilizar parcialmente e de compreender sem percorrer centenas de linhas.</p>",
        unsafe_allow_html=True,
    )
    code_block(
        """class GestorLoja:
    def calcular_total(self, pedido): ...
    def aplicar_desconto(self, pedido): ...
    def emitir_fatura(self, pedido): ...
    def gerir_stock(self, produto): ...
    def enviar_email(self, cliente): ...
    def gerar_relatorio(self): ...""",
        filename="large_class_teorica.py",
        label="EXEMPLO TEÓRICO",
    )
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        card("Problema causado", "Baixa coesão: a classe muda por muitos motivos e concentra dependências que deviam estar separadas.", "red", "P")
    with c2:
        card("Técnica de refatoração", "Extrair classes com responsabilidades coesas (por exemplo, Fatura, Stock e Relatório).", "green", "T")

with separadores[4]:
    st.markdown(
        f'<div class="cl-pill-row">{badge("Exemplo teórico", "violet")}</div>',
        unsafe_allow_html=True,
    )
    section_title("Long Parameter List", "Funções que recebem demasiados argumentos.")
    st.markdown(
        "<p class='cl-lead'>Muitos parâmetros aumentam o acoplamento e tornam as chamadas difíceis "
        "de ler. É fácil trocar a ordem dos argumentos ou passar valores incoerentes.</p>",
        unsafe_allow_html=True,
    )
    code_block(
        """def criar_fatura(nome, morada, nif, email, telefone,
                  produto, preco, quantidade, desconto,
                  data_emissao, moeda, observacoes):
    ...""",
        filename="long_parameters_teorica.py",
        label="EXEMPLO TEÓRICO",
    )
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        card("Problema causado", "Chamadas longas, maior probabilidade de erro posicional e acoplamento a dados que não são responsabilidade da função.", "red", "P")
    with c2:
        card("Técnica de refatoração", "Introduzir um objecto de parâmetros (por exemplo, um dicionário ou dataclass Pedido) e agrupar dados relacionados.", "green", "T")

st.markdown("<br>", unsafe_allow_html=True)
section_title("Mapa rápido", "Sinais, consequências e técnicas associadas.")
tabela(
    ["Code smell", "Sinal típico", "Técnica de refatoração"],
    [
        ["Long Method", "Função com muitos blocos e responsabilidades", "Extrair Método"],
        ["Duplicated Code", "Blocos iguais em locais diferentes", "Substitute Algorithm / Pull Up Method"],
        ["Complex Conditional", "if/elif profundos ou expressões densas", "Decompose Conditional / guard clauses / tabela de regras"],
        ["Large Class", "Classe com muitos métodos e dependências", "Extrair classe"],
        ["Long Parameter List", "Assinatura com muitos argumentos", "Objecto de parâmetros"],
    ],
)
