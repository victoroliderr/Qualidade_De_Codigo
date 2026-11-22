"""Testes de integração da página única e das rotas FastHTML.

Estes testes validam o que a defesa apresenta: a página em pt-AO, os ficheiros
estáticos, a comparação com e sem HTMX e a ausência de moeda brasileira.
"""
from __future__ import annotations

import pytest
from starlette.testclient import TestClient

import main


@pytest.fixture()
def cliente():
    return TestClient(main.app)


def test_pagina_inicial_em_portugues_de_angola(cliente, record_property):
    record_property("descricao", "Página inicial em português de Angola")
    resposta = cliente.get("/")

    assert resposta.status_code == 200
    html = resposta.text
    assert 'lang="pt-AO"' in html
    assert "CODELAB" in html
    assert "O mesmo resultado." in html
    assert "90.000,00 Kz" in html
    assert "Comportamento preservado" in html
    assert "aprovados" in html
    assert "falhados" in html


def test_ficheiros_estaticos_servidos(cliente, record_property):
    record_property("descricao", "Ficheiros estáticos servidos")
    css = cliente.get("/styles.css")
    htmx = cliente.get("/htmx.min.js")

    assert css.status_code == 200
    assert css.headers["content-type"].startswith("text/css")
    assert "--accent" in css.text

    assert htmx.status_code == 200
    assert "javascript" in htmx.headers["content-type"]
    assert len(htmx.text) > 10_000


def test_comparacao_sem_javascript_devolve_pagina_completa(cliente, record_property):
    record_property(
        "descricao", "Comparação sem JavaScript devolve a página completa"
    )
    resposta = cliente.post("/comparar", data={"tipo": "PREMIUM"})

    assert resposta.status_code == 200
    assert "<html" in resposta.text.lower()
    assert "170.000,00 Kz" in resposta.text
    assert "Empresa TIS Angola" in resposta.text


def test_comparacao_com_htmx_devolve_apenas_o_painel(cliente, record_property):
    record_property(
        "descricao", "Comparação com HTMX devolve apenas o painel"
    )
    resposta = cliente.post(
        "/comparar",
        data={"tipo": "COMUM"},
        headers={"HX-Request": "true"},
    )

    assert resposta.status_code == 200
    assert "<html" not in resposta.text.lower()
    assert "100.000,00 Kz" in resposta.text
    assert "Guilhermino João" in resposta.text


def test_sem_moeda_brasileira_na_pagina(cliente, record_property):
    record_property("descricao", "Ausência de moeda brasileira na página")
    html = cliente.get("/").text

    for termo in ("R$", "BRL", "USD", "Reais", "Dólares"):
        assert termo not in html


def test_membros_do_grupo_substituem_tecnologias_no_cabecalho(cliente, record_property):
    record_property("descricao", "Membros do grupo apresentados no início da página")
    html = cliente.get("/").text

    for nome in ("Victor Pedro", "Manuel Mendes", "Luís Pedro", "Miguel Bengui"):
        assert nome in html

    assert "Python · FastHTML · pytest" not in html
    assert "Laboratório académico" not in html


def test_menu_mobile_interativo(cliente, record_property):
    record_property("descricao", "Menu mobile com botão acessível")
    html = cliente.get("/").text

    assert 'id="menu-mobile"' in html
    assert 'aria-controls="menu-navegacao"' in html
    assert 'aria-expanded="false"' in html
    assert 'id="menu-navegacao"' in html
    assert "DOMContentLoaded" in html


def test_favicon_do_codelab_servido(cliente, record_property):
    record_property("descricao", "Favicon do CODELAB servido nos dois formatos")
    ico = cliente.get("/favicon.ico")
    svg = cliente.get("/favicon.svg")

    assert ico.status_code == 200
    assert len(ico.content) > 100
    assert svg.status_code == 200
    assert "<svg" in svg.text
