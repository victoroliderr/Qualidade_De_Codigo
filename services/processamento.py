"""Serviços auxiliares do CODELAB."""
from __future__ import annotations

import io
from contextlib import redirect_stdout

from implementacoes import pedido_original, pedido_refatorado


def formatar_kwanzas(valor):
    return f"{valor:,.2f} Kz".replace(",", "X").replace(".", ",").replace("X", ".")


def executar_comparacao(pedido):
    def capturar(funcao):
        saida = io.StringIO()
        with redirect_stdout(saida):
            resultado = funcao(pedido)
        return resultado, saida.getvalue()

    v_o, f_o = capturar(pedido_original.processar_pedido)
    v_r, f_r = capturar(pedido_refatorado.processar_pedido)
    return {
        "valor_original": v_o,
        "valor_refatorado": v_r,
        "fatura_original": f_o,
        "fatura_refatorada": f_r,
        "preservado": v_o == v_r and f_o == f_r,
    }


EXEMPLOS = {
    "COMUM": {"cliente": "João Silva", "tipo_cliente": "COMUM", "itens": [{"preco": 50.0, "quantidade": 2}]},
    "VIP": {"cliente": "Maria Santos", "tipo_cliente": "VIP", "itens": [{"preco": 100.0, "quantidade": 1}]},
    "PREMIUM": {"cliente": "Empresa XYZ", "tipo_cliente": "PREMIUM", "itens": [{"preco": 200.0, "quantidade": 1}]},
}
