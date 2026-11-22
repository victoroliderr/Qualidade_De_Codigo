"""Configuração necessária para publicar a aplicação no Render."""
from __future__ import annotations

from pathlib import Path

import pytest

import main

RAIZ = Path(__file__).resolve().parent.parent


def test_blueprint_do_render_esta_configurado(record_property):
    record_property("descricao", "Blueprint do Render configura o arranque ASGI")
    conteudo = (RAIZ / "render.yaml").read_text(encoding="utf-8")

    assert "runtime: python" in conteudo
    assert "uvicorn main:app --host 0.0.0.0 --port $PORT" in conteudo
    assert "healthCheckPath: /" in conteudo
    assert "generateValue: true" in conteudo


def test_chave_de_sessao_local_e_estavel(monkeypatch, record_property):
    record_property("descricao", "Chave de sessão local é estável")
    for nome in ("SESSKEY", "RENDER", "VERCEL"):
        monkeypatch.delenv(nome, raising=False)

    assert main.chave_sessao() == main.CHAVE_LOCAL


def test_producao_exige_chave_de_sessao(monkeypatch, record_property):
    record_property("descricao", "Produção recusa arrancar sem SESSKEY")
    monkeypatch.delenv("SESSKEY", raising=False)
    monkeypatch.setenv("RENDER", "true")

    with pytest.raises(RuntimeError, match="SESSKEY"):
        main.chave_sessao()


def test_chave_configurada_e_utilizada_em_producao(monkeypatch, record_property):
    record_property("descricao", "Chave configurada é usada no Render")
    monkeypatch.setenv("RENDER", "true")
    monkeypatch.setenv("SESSKEY", "chave-de-teste")

    assert main.chave_sessao() == "chave-de-teste"
