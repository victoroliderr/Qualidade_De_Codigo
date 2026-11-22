"""Secção de demonstração e painel de resultados."""
from __future__ import annotations

from fasthtml.common import (
    Button,
    Div,
    Fieldset,
    Form,
    Input,
    Label,
    Legend,
    P,
    Pre,
    Section,
    Span,
)

from components.base import cabecalho_seccao
from services.moeda import formatar_kwanzas
from services.processamento import resumo_exemplos


def _opcao_cliente(item: dict, selecionado: bool) -> Div:
    identificador = f"tipo-{item['tipo'].lower()}"
    return Div(
        Input(
            type="radio",
            name="tipo",
            value=item["tipo"],
            id=identificador,
            checked=selecionado,
        ),
        Label(
            Span(
                Span(item["tipo"], cls="tipo-nome"),
                Span(f"{item['percentagem']}%", cls="tipo-percentagem"),
                cls="tipo-topo",
            ),
            Span(item["cliente"], cls="tipo-cliente"),
            Span(
                f"Base {formatar_kwanzas(item['valor_base'])}",
                cls="tipo-base",
            ),
            Span(formatar_kwanzas(item["total"]), cls="tipo-valor"),
            **{"for": identificador},
        ),
        cls="tipo",
    )


def painel_resultados(resultado: dict | None) -> Div:
    if resultado is None:
        return Div(
            P(
                "Selecciona um tipo de cliente e executa a comparação.",
                cls="resultado-vazio",
            ),
            cls="resultado-conteudo",
        )

    if resultado["preservado"]:
        estado = Div(
            Span(cls="status-dot"),
            Span("Comportamento preservado", cls="status-title"),
            Span("Mesmo valor e mesma factura nas duas versões.", cls="status-note"),
            cls="status-bar ok",
        )
    else:
        estado = Div(
            Span(cls="status-dot"),
            Span("Diferença detectada", cls="status-title"),
            Span("As duas versões não produziram o mesmo resultado.", cls="status-note"),
            cls="status-bar erro",
        )

    return Div(
        Div(
            Span("Resultado da execução", cls="resultado-etiqueta"),
            Span(
                f"{resultado['cliente']} · {resultado['tipo_cliente']}",
                cls="resultado-contexto",
            ),
            cls="resultado-topo",
        ),
        Div(
            _coluna_resultado(
                "Antes",
                "Código original",
                "processar_pedido() · uma função",
                resultado["valor_original"],
                resultado["fatura_original"],
            ),
            _coluna_resultado(
                "Depois",
                "Código refatorado",
                "processar_pedido() · quatro funções",
                resultado["valor_refatorado"],
                resultado["fatura_refatorada"],
            ),
            cls="resultado-grelha",
        ),
        estado,
        cls="resultado-conteudo",
    )


def _coluna_resultado(
    etiqueta: str,
    titulo: str,
    detalhe: str,
    valor: float,
    fatura: str,
) -> Div:
    return Div(
        Span(etiqueta, cls="resultado-etiqueta"),
        P(titulo, cls="resultado-titulo"),
        P(formatar_kwanzas(valor), cls="resultado-valor"),
        P(detalhe, cls="resultado-detalhe"),
        Pre(fatura, cls="invoice"),
        cls="resultado-coluna",
    )


def seccao_demonstracao(tipo: str, resultado: dict) -> Section:
    opcoes = [
        _opcao_cliente(item, item["tipo"] == tipo)
        for item in resumo_exemplos()
    ]

    return Section(
        cabecalho_seccao(
            "01",
            "Demonstração",
            "Processamento de encomendas",
            (
                "Escolhe o tipo de cliente. As duas versões recebem exactamente "
                "os mesmos dados e são executadas agora."
            ),
        ),
        Form(
            Fieldset(
                Legend("Tipo de cliente", cls="visually-hidden"),
                Div(*opcoes, cls="tipo-grelha"),
                cls="tipo-fieldset",
            ),
            Div(
                Button(
                    Span("Comparar as duas versões", cls="btn-idle"),
                    Span("A comparar…", cls="btn-loading"),
                    type="submit",
                    id="botao-comparar",
                    cls="btn-primary",
                ),
                P(
                    "Valores ilustrativos em Kwanzas. Nenhum resultado é simulado.",
                    cls="demo-nota",
                ),
                cls="demo-acoes",
            ),
            action="/comparar#resultado",
            method="post",
            hx_post="/comparar",
            hx_target="#resultado",
            hx_swap="innerHTML show:#resultado:top",
            hx_indicator="#botao-comparar",
            hx_disabled_elt="#botao-comparar",
            **{"aria-label": "Comparar as duas versões"},
        ),
        Div(
            painel_resultados(resultado),
            id="resultado",
            cls="resultado",
            **{"aria-live": "polite"},
        ),
        id="demonstracao",
        cls="section",
    )
