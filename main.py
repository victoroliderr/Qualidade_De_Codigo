"""CODELAB — ponto de entrada ASGI para execução local e Vercel.

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

# Chave estável para cookies assinados. Em produção, define SESSKEY no Vercel.
# O valor de recurso local evita gerar uma chave diferente em cada arranque.
SESSKEY = os.getenv("SESSKEY")
if not SESSKEY:
    if os.getenv("VERCEL"):
        raise RuntimeError(
            "Define a variável de ambiente SESSKEY antes de publicar no Vercel."
        )
    SESSKEY = "codelab-desenvolvimento-local"

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
