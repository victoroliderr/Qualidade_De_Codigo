"""Elementos partilhados pelas secções da página."""
from __future__ import annotations

from fasthtml.common import Div, H2, P, Span


def cabecalho_seccao(numero: str, rotulo: str, titulo: str, descricao: str) -> Div:
    return Div(
        Div(
            Span(
                f"{numero} / {rotulo}",
                cls="section-eyebrow",
            ),
            H2(titulo, cls="section-title"),
            cls="section-heading",
        ),
        P(descricao, cls="section-note"),
        cls="section-head",
    )
