"""Conceitos essenciais, em formato compacto."""
from __future__ import annotations

from fasthtml.common import (
    Dd,
    Details,
    Div,
    Dl,
    Dt,
    H3,
    P,
    Section,
    Span,
    Summary,
)

from components.base import cabecalho_seccao

ATRIBUTOS = (
    (
        "Legibilidade",
        "O código diz o que faz sem exigir explicações.",
    ),
    (
        "Manutenibilidade",
        "Alterar uma regra exige tocar apenas no sítio certo.",
    ),
    (
        "Reutilização",
        "As funções podem ser usadas por outros fluxos.",
    ),
    (
        "Eficiência",
        "O valor base é calculado uma única vez.",
    ),
    (
        "Confiabilidade",
        "Os testes confirmam que o comportamento se mantém.",
    ),
)

DEFINICOES = (
    (
        "O que é refatoração?",
        "Melhorar a estrutura interna do código sem alterar o comportamento externo.",
    ),
    (
        "Qual técnica foi aplicada?",
        "Extrair Método — separar partes de uma função em funções independentes.",
    ),
    (
        "Qual era o problema?",
        "Uma única função acumulava cálculo, desconto e emissão da factura.",
    ),
    (
        "Qual foi a melhoria?",
        "Cada operação passou a ter uma função própria, com nome e responsabilidade claras.",
    ),
)

OUTROS_CONCEITOS = (
    (
        "Dívida técnica",
        "Custo futuro de atalhos e decisões que tornam o código mais difícil de manter.",
    ),
    (
        "Code smells",
        "Sinais no código que sugerem problemas estruturais, como funções longas e duplicação.",
    ),
    (
        "Ferramentas",
        "Pylint, Ruff, SonarQube e coverage detectam problemas; não substituem revisão.",
    ),
    (
        "Métricas",
        "Complexidade ciclomática, acoplamento e cobertura medem aspectos diferentes da qualidade.",
    ),
    (
        "Outras técnicas",
        "Extrair Classe, Mover Método, Renomear e Substituir Condicional por Polimorfismo.",
    ),
)


def seccao_conceitos() -> Section:
    return Section(
        cabecalho_seccao(
            "04",
            "Conceitos",
            "O essencial, em poucas linhas",
            (
                "Cinco atributos de qualidade e a técnica que sustenta a "
                "comparação. O relatório escrito contém o desenvolvimento completo."
            ),
        ),
        Div(
            *[
                Div(
                    Span(f"{indice:02d}", cls="atributo-numero"),
                    H3(nome, cls="atributo-nome"),
                    P(descricao, cls="atributo-texto"),
                    cls="atributo",
                )
                for indice, (nome, descricao) in enumerate(ATRIBUTOS, start=1)
            ],
            cls="atributos",
        ),
        Dl(
            *[
                Div(
                    Dt(pergunta, cls="definicao-termo"),
                    Dd(resposta, cls="definicao-texto"),
                    cls="definicao",
                )
                for pergunta, resposta in DEFINICOES
            ],
            cls="definicoes",
        ),
        Details(
            Summary("Outros conceitos do relatório", cls="outros-resumo"),
            Div(
                *[
                    Div(
                        H3(titulo, cls="outro-titulo"),
                        P(texto, cls="outro-texto"),
                        cls="outro",
                    )
                    for titulo, texto in OUTROS_CONCEITOS
                ],
                cls="outros-grid",
            ),
            cls="outros",
        ),
        id="conceitos",
        cls="section section-final",
    )
