"""Formatação monetária central do CODELAB.

Todos os valores apresentados na interface e nas facturas usam o Kwanza
angolano, com ponto para os milhares e vírgula para as casas decimais.
"""
from __future__ import annotations


def formatar_kwanzas(valor: float | int) -> str:
    """Devolve um valor no formato ``100.000,00 Kz``."""
    inteiro, decimal = f"{valor:,.2f}".split(".")
    return f"{inteiro.replace(',', '.')},{decimal} Kz"
