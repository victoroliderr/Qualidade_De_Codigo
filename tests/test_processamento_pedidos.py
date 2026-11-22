"""Suíte pytest do processamento de pedidos da loja virtual.

Os casos oficiais do relatório usam valores em Kwanzas e a localização
portuguesa de Angola. Os restantes testes verificam equivalência de
comportamento, pedidos com vários produtos e a formatação monetária.
"""
from __future__ import annotations

import io
from contextlib import redirect_stdout

import pytest

from implementacoes import pedido_original, pedido_refatorado
from services.moeda import formatar_kwanzas


def capturar(funcao, pedido):
    """Executa uma implementação e devolve (valor, fatura, excepção)."""
    saida = io.StringIO()
    with redirect_stdout(saida):
        try:
            resultado = funcao(pedido)
        except Exception as erro:  # pragma: no cover - registado para o relatório
            return None, saida.getvalue(), erro
    return resultado, saida.getvalue(), None


def executar_nas_duas(pedido):
    """Executa as duas implementações com cópias independentes dos dados."""
    pedido_original_copia = {
        "cliente": pedido["cliente"],
        "tipo_cliente": pedido["tipo_cliente"],
        "itens": [dict(item) for item in pedido["itens"]],
    }
    pedido_refatorado_copia = {
        "cliente": pedido["cliente"],
        "tipo_cliente": pedido["tipo_cliente"],
        "itens": [dict(item) for item in pedido["itens"]],
    }
    valor_original, fatura_original, erro_original = capturar(
        pedido_original.processar_pedido, pedido_original_copia
    )
    valor_refatorado, fatura_refatorada, erro_refatorado = capturar(
        pedido_refatorado.processar_pedido, pedido_refatorado_copia
    )
    return {
        "valor_original": valor_original,
        "valor_refatorado": valor_refatorado,
        "fatura_original": fatura_original,
        "fatura_refatorada": fatura_refatorada,
        "erro_original": erro_original,
        "erro_refatorado": erro_refatorado,
    }


def verificar_caso(pedido, esperado, record_property, descricao):
    resultado = executar_nas_duas(pedido)
    obtido_original = resultado["valor_original"]
    obtido_refatorado = resultado["valor_refatorado"]

    record_property("descricao", descricao)
    record_property("esperado", formatar_kwanzas(esperado))
    record_property(
        "obtido",
        f"Original {formatar_kwanzas(obtido_original)} · "
        f"Refatorado {formatar_kwanzas(obtido_refatorado)}",
    )

    assert resultado["erro_original"] is None, resultado["erro_original"]
    assert resultado["erro_refatorado"] is None, resultado["erro_refatorado"]
    assert resultado["fatura_original"] == resultado["fatura_refatorada"]
    assert obtido_original == pytest.approx(esperado)
    assert obtido_refatorado == pytest.approx(esperado)


# --- Casos do relatório académico -------------------------------------------


def test_cliente_comum(record_property):
    """Cliente COMUM (0%) deve pagar 100.000,00 Kz."""
    pedido = {
        "cliente": "João Silva",
        "tipo_cliente": "COMUM",
        "itens": [{"preco": 50_000.0, "quantidade": 2}],
    }
    verificar_caso(pedido, 100_000.0, record_property, "Cliente COMUM — sem desconto")


def test_cliente_vip(record_property):
    """Cliente VIP (10%) deve pagar 90.000,00 Kz."""
    pedido = {
        "cliente": "Maria Santos",
        "tipo_cliente": "VIP",
        "itens": [{"preco": 100_000.0, "quantidade": 1}],
    }
    verificar_caso(pedido, 90_000.0, record_property, "Cliente VIP — desconto de 10%")

    resultado = executar_nas_duas(pedido)
    assert "TOTAL A PAGAR: 90.000,00 Kz" in resultado["fatura_original"]
    assert "Desconto: 10%" in resultado["fatura_refatorada"]


def test_cliente_premium(record_property):
    """Cliente PREMIUM (15%) deve pagar 170.000,00 Kz."""
    pedido = {
        "cliente": "Empresa Kwanza",
        "tipo_cliente": "PREMIUM",
        "itens": [{"preco": 200_000.0, "quantidade": 1}],
    }
    verificar_caso(
        pedido, 170_000.0, record_property, "Cliente PREMIUM — desconto de 15%"
    )


# --- Testes complementares --------------------------------------------------


def test_equivalencia_entre_implementacoes(record_property):
    """Original e refatorado devem devolver o mesmo valor e a mesma fatura."""
    pedido = {
        "cliente": "Ana Costa",
        "tipo_cliente": "VIP",
        "itens": [
            {"preco": 75_000.0, "quantidade": 3},
            {"preco": 12_500.0, "quantidade": 2},
        ],
    }
    resultado = executar_nas_duas(pedido)

    record_property("descricao", "Equivalência de comportamento entre as duas versões")
    record_property(
        "esperado",
        "Mesmo valor devolvido e fatura idêntica nas duas implementações",
    )
    record_property(
        "obtido",
        f"Original {formatar_kwanzas(resultado['valor_original'])} · "
        f"Refatorado {formatar_kwanzas(resultado['valor_refatorado'])} · "
        f"faturas "
        f"{'iguais' if resultado['fatura_original'] == resultado['fatura_refatorada'] else 'diferentes'}",
    )

    assert resultado["erro_original"] is None, resultado["erro_original"]
    assert resultado["erro_refatorado"] is None, resultado["erro_refatorado"]
    assert resultado["valor_original"] == pytest.approx(225_000.0)
    assert resultado["valor_refatorado"] == pytest.approx(resultado["valor_original"])
    assert resultado["fatura_original"] == resultado["fatura_refatorada"]


def test_multiplos_produtos(record_property):
    """A soma de vários produtos e quantidades deve ser correcta."""
    pedido = {
        "cliente": "Carlos Lima",
        "tipo_cliente": "COMUM",
        "itens": [
            {"preco": 30_000.0, "quantidade": 2},
            {"preco": 20_000.0, "quantidade": 1},
            {"preco": 10_000.0, "quantidade": 5},
        ],
    }
    verificar_caso(
        pedido, 130_000.0, record_property, "Múltiplos produtos — soma correcta"
    )


def test_tipo_cliente_sem_desconto(record_property):
    """Um tipo fora da tabela de descontos não deve receber desconto."""
    pedido = {
        "cliente": "Visitante",
        "tipo_cliente": "ESPECIAL",
        "itens": [{"preco": 100_000.0, "quantidade": 1}],
    }
    verificar_caso(
        pedido,
        100_000.0,
        record_property,
        "Tipo de cliente desconhecido — sem desconto",
    )


def test_formatacao_kwanzas(record_property):
    """A formatação monetária deve usar ponto nos milhares e vírgula decimal."""
    record_property("descricao", "Formatação central de Kwanzas")
    record_property("esperado", "1.000,00 Kz · 50.000,00 Kz · 170.000,00 Kz")
    record_property(
        "obtido",
        f"{formatar_kwanzas(1_000)} · {formatar_kwanzas(50_000)} · "
        f"{formatar_kwanzas(170_000)}",
    )

    assert formatar_kwanzas(1_000) == "1.000,00 Kz"
    assert formatar_kwanzas(50_000) == "50.000,00 Kz"
    assert formatar_kwanzas(170_000) == "170.000,00 Kz"
