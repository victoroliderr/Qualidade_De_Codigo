"""Comparação visual dos ficheiros reais das duas implementações."""
from __future__ import annotations

import html
import re
from pathlib import Path

from fasthtml.common import (
    Div,
    Li,
    NotStr,
    Ol,
    P,
    Section,
    Span,
)
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token

from components.base import cabecalho_seccao

RAIZ = Path(__file__).resolve().parent.parent

FUNCOES_REFATORADAS = (
    "calcular_valor_base",
    "aplicar_desconto_cliente",
    "emitir_fatura_impressa",
    "processar_pedido",
)

_DEFINICAO = re.compile(r"^\s*def\s+([A-Za-z_]\w*)\s*\(")


def _classe_token(token) -> str:
    """Mapeia tokens do Pygments para as classes usadas no CSS."""
    if token in Token.Keyword:
        return "tok-k"
    if token in Token.Name.Builtin:
        return "tok-nb"
    if token in Token.Name.Function:
        return "tok-nf"
    if token in Token.Name.Class:
        return "tok-nc"
    if token in Token.Name.Namespace:
        return "tok-nn"
    if token in Token.Name.Decorator:
        return "tok-nd"
    if token in Token.Name:
        return "tok-n"
    if token in Token.Literal.String:
        return "tok-s"
    if token in Token.Literal.Number:
        return "tok-m"
    if token in Token.Comment:
        return "tok-c"
    if token in Token.Operator:
        return "tok-o"
    if token in Token.Punctuation:
        return "tok-p"
    return ""


def _linhas_destacadas(codigo: str) -> list[str]:
    """Converte código Python em linhas HTML independentes."""
    linhas: list[list[tuple[str, str]]] = [[]]

    for token, valor in lex(codigo, PythonLexer()):
        partes = valor.split("\n")
        for indice, parte in enumerate(partes):
            if indice > 0:
                linhas.append([])
            if parte:
                linhas[-1].append((_classe_token(token), parte))

    if linhas and not linhas[-1]:
        linhas.pop()

    resultado = []
    for tokens in linhas:
        fragmentos = []
        for classe, texto in tokens:
            seguro = html.escape(texto)
            if classe:
                fragmentos.append(f'<span class="{classe}">{seguro}</span>')
            else:
                fragmentos.append(seguro)
        resultado.append("".join(fragmentos))
    return resultado


def _intervalos_funcoes(codigo: str, funcoes: set[str]) -> list[tuple[int, int]]:
    """Devolve os intervalos (início, fim) das funções a destacar."""
    linhas = codigo.rstrip("\n").split("\n")
    definicoes = []

    for indice, linha in enumerate(linhas):
        encontrada = _DEFINICAO.match(linha)
        if encontrada:
            definicoes.append(
                (indice, encontrada.group(1), linha[: len(linha) - len(linha.lstrip())])
            )

    intervalos = []
    for ordem, (inicio, nome, indentacao) in enumerate(definicoes):
        if nome not in funcoes:
            continue
        fim = len(linhas) - 1
        for seguinte, _, indentacao_seguinte in definicoes[ordem + 1 :]:
            if len(indentacao_seguinte) <= len(indentacao):
                fim = seguinte - 1
                break
        while fim > inicio and not linhas[fim].strip():
            fim -= 1
        intervalos.append((inicio, fim))
    return intervalos


def _corpo_codigo(codigo: str, funcoes: set[str]) -> Div:
    linhas = _linhas_destacadas(codigo)
    brutas = codigo.rstrip("\n").split("\n")
    intervalos = _intervalos_funcoes(codigo, funcoes)
    elementos = []

    for numero, linha in enumerate(linhas, start=1):
        indice = numero - 1
        bruta = brutas[indice] if indice < len(brutas) else ""
        encontrada = _DEFINICAO.match(bruta)
        foco = encontrada is not None and encontrada.group(1) in funcoes
        bloco = any(inicio <= indice <= fim for inicio, fim in intervalos)
        classes = "code-line"
        if bloco:
            classes += " is-block"
        if foco:
            classes += " is-focus"
        elementos.append(
            Div(
                Span(f"{numero:>2}", cls="ln"),
                Span(
                    NotStr(linha) if linha else NotStr("&#8203;"),
                    cls="lc",
                ),
                cls=classes,
            )
        )

    return Div(*elementos, cls="code-body")


def _painel_codigo(
    etiqueta: str,
    ficheiro: str,
    contagem: str,
    codigo: str,
    funcoes: set[str],
) -> Div:
    return Div(
        Div(
            Div(
                Span(etiqueta, cls="code-etiqueta"),
                Span(ficheiro, cls="code-ficheiro"),
                cls="code-identidade",
            ),
            Span(contagem, cls="code-contagem"),
            cls="code-topo",
        ),
        Div(_corpo_codigo(codigo, funcoes), cls="code-scroll"),
        cls="code-panel",
    )


def _ler_ficheiro(nome: str) -> str:
    return (RAIZ / "implementacoes" / nome).read_text(encoding="utf-8")


def seccao_comparacao() -> Section:
    codigo_original = _ler_ficheiro("pedido_original.py")
    codigo_refatorado = _ler_ficheiro("pedido_refatorado.py")

    return Section(
        cabecalho_seccao(
            "02",
            "Comparação",
            "O que mudou no código?",
            (
                "Os ficheiros apresentados são os que executam a demonstração. "
                "As linhas sublinhadas marcam as funções em destaque."
            ),
        ),
        Div(
            _painel_codigo(
                "Antes",
                "pedido_original.py",
                "1 função",
                codigo_original,
                {"processar_pedido"},
            ),
            _painel_codigo(
                "Depois",
                "pedido_refatorado.py",
                "4 funções",
                codigo_refatorado,
                set(FUNCOES_REFATORADAS),
            ),
            cls="code-grid",
        ),
        Div(
            Div(
                Span("Funções extraídas", cls="mini-etiqueta"),
                Ol(
                    *[
                        Li(
                            Span(f"{indice:02d}", cls="fn-numero"),
                            Span(f"{nome}()", cls="fn-nome"),
                            cls="fn-item",
                        )
                        for indice, nome in enumerate(FUNCOES_REFATORADAS, start=1)
                    ],
                    cls="fn-lista",
                ),
                cls="fn-bloco",
            ),
            P(
                "Antes, uma única função executava várias responsabilidades. "
                "Depois, cada operação passou a ter uma função própria.",
                cls="code-explicacao",
            ),
            cls="code-notas",
        ),
        id="comparacao",
        cls="section",
    )
