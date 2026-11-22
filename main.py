"""CODELAB — ponto de entrada ASGI para execução local e publicação no Render.

A aplicação é uma página única em FastHTML. A demonstração executa as duas
implementações reais em Python e devolve o resultado através de HTMX.
"""
from __future__ import annotations

import os

from fasthtml.common import fast_app, serve

from components.demonstracao import painel_resultados
from components.layout import pagina
from services.processamento import (
    TIPO_PREDEFINIDO,
    executar_comparacao,
    exemplo_por_tipo,
)

# O Render e o Vercel sinalizam o ambiente através de uma variável própria.
# Nesses ambientes a chave tem de vir das variáveis de ambiente da plataforma.
PLATAFORMAS_PRODUCAO = ("RENDER", "VERCEL")
CHAVE_LOCAL = "codelab-desenvolvimento-local"


def chave_sessao() -> str:
    """Devolve a chave estável dos cookies; recusa arrancar sem chave em produção."""
    chave = os.getenv("SESSKEY")
    if chave:
        return chave

    if any(os.getenv(nome) for nome in PLATAFORMAS_PRODUCAO):
        raise RuntimeError(
            "Define a variável de ambiente SESSKEY antes de publicar a aplicação."
        )

    # Em desenvolvimento, um valor fixo evita invalidar os cookies a cada arranque.
    return CHAVE_LOCAL


SESSKEY = chave_sessao()

app, rt = fast_app(
    pico=False,
    surreal=False,
    htmx=False,
    default_hdrs=False,
    static_path="public",
    secret_key=SESSKEY,
    title="CODELAB — Qualidade do Código e Refatoração",
    htmlkw={"lang": "pt-AO"},
)


@rt("/")
def get():
    return pagina(TIPO_PREDEFINIDO)


@rt("/comparar")
def post(tipo: str = TIPO_PREDEFINIDO, htmx=None):
    resultado = executar_comparacao(exemplo_por_tipo(tipo))

    if getattr(htmx, "request", None):
        return painel_resultados(resultado)

    # Fallback sem JavaScript: devolve a página completa com o resultado.
    return pagina(resultado["tipo_cliente"], resultado)


if __name__ == "__main__":
    serve()
