"""Resumo honesto da última execução real do pytest."""
from __future__ import annotations

from fasthtml.common import Code, Div, Li, P, Section, Span, Ul

from components.base import cabecalho_seccao


def _nome_legivel(resultado: dict) -> str:
    if resultado.get("descricao"):
        return resultado["descricao"]
    return resultado.get("nome", "teste").removeprefix("test_").replace("_", " ")


def _estado(resultado: dict) -> tuple[str, str]:
    if resultado.get("estado") == "passed":
        return "aprovado", "Aprovado"
    if resultado.get("estado") == "failed":
        return "falhado", "Falhado"
    return "pendente", "Pendente"


def _lista_testes(dados: dict) -> Ul:
    itens = []
    for resultado in dados.get("resultados", []):
        classe, rotulo = _estado(resultado)
        itens.append(
            Li(
                Span(cls=f"test-dot {classe}"),
                Span(_nome_legivel(resultado), cls="test-nome"),
                Span(rotulo, cls=f"test-estado {classe}"),
                cls="test-item",
            )
        )
    return Ul(*itens, cls="test-lista")


def seccao_validacao(dados: dict | None) -> Section:
    if dados:
        aprovados = dados.get("aprovados", 0)
        total = dados.get("total", 0)
        falhados = dados.get("falhados", 0)
        data_legivel = dados.get("data_legivel", "data não registada")

        if falhados == 0 and total > 0:
            resumo = "Todos os testes passaram."
            classe = "ok"
        elif falhados == 1:
            resumo = "Um teste falhou."
            classe = "erro"
        else:
            resumo = f"{falhados} testes falharam."
            classe = "erro"

        resumo_html = Div(
            Div(
                Span(str(aprovados), cls="test-numero"),
                Span(f" / {total}", cls="test-total"),
                cls="test-contagem",
            ),
            P(
                f"{aprovados} aprovados · {falhados} falhados",
                cls="test-contagem-resumo",
            ),
            P(resumo, cls=f"test-resumo {classe}"),
            P(f"Execução de {data_legivel}.", cls="test-data"),
            P(
                "A suíte completa corre no terminal ou na CI com ",
                Code("pytest -q"),
                ".",
                cls="test-comando",
            ),
            cls="test-bloco",
        )
        lista = _lista_testes(dados)
    else:
        resumo_html = Div(
            Div(Span("—", cls="test-numero"), cls="test-contagem"),
            P("Sem resultados registados.", cls="test-resumo"),
            P(
                "Executa ",
                Code("CODELAB_RESULTS_PATH=data/resultados_testes.json pytest -q"),
                " para gerar o relatório real.",
                cls="test-comando",
            ),
            cls="test-bloco",
        )
        lista = Ul(
            Li(
                Span(cls="test-dot pendente"),
                Span("Nenhum resultado disponível", cls="test-nome"),
                Span("Pendente", cls="test-estado pendente"),
                cls="test-item",
            ),
            cls="test-lista",
        )

    return Section(
        cabecalho_seccao(
            "03",
            "Validação",
            "Testes automatizados",
            (
                "Resumo da última execução real do pytest. O servidor não corre "
                "testes: apenas apresenta o relatório gerado localmente ou na CI."
            ),
        ),
        Div(resumo_html, lista, cls="test-grid"),
        id="validacao",
        cls="section",
    )
