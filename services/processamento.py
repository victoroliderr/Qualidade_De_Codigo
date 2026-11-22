"""Execução real das duas implementações e leitura dos resultados do pytest."""
from __future__ import annotations

import io
import json
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path

from implementacoes import pedido_original, pedido_refatorado
from implementacoes.pedido_refatorado import TAXAS_DESCONTO

RAIZ = Path(__file__).resolve().parent.parent
FICHEIRO_RESULTADOS = RAIZ / "data" / "resultados_testes.json"

MESES = (
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
)

# Exemplos demonstrativos em contexto angolano. Os valores são ilustrativos.
EXEMPLOS = {
    "COMUM": {
        "cliente": "Guilhermino João",
        "tipo_cliente": "COMUM",
        "itens": [{"preco": 50_000.0, "quantidade": 2}],
    },
    "VIP": {
        "cliente": "Maria dos Santos",
        "tipo_cliente": "VIP",
        "itens": [{"preco": 100_000.0, "quantidade": 1}],
    },
    "PREMIUM": {
        "cliente": "Empresa TIS Angola",
        "tipo_cliente": "PREMIUM",
        "itens": [{"preco": 200_000.0, "quantidade": 1}],
    },
}

TIPO_PREDEFINIDO = "VIP"


def _copiar_pedido(pedido: dict) -> dict:
    """Cria uma cópia independente para cada implementação."""
    return {
        "cliente": pedido["cliente"],
        "tipo_cliente": pedido["tipo_cliente"],
        "itens": [dict(item) for item in pedido["itens"]],
    }


def _executar_em_silencio(funcao, pedido: dict) -> tuple[float, str]:
    saida = io.StringIO()
    with redirect_stdout(saida):
        valor = funcao(pedido)
    return valor, saida.getvalue()


def executar_comparacao(pedido: dict) -> dict:
    """Executa as duas versões com os mesmos dados e compara os resultados."""
    valor_original, fatura_original = _executar_em_silencio(
        pedido_original.processar_pedido, _copiar_pedido(pedido)
    )
    valor_refatorado, fatura_refatorada = _executar_em_silencio(
        pedido_refatorado.processar_pedido, _copiar_pedido(pedido)
    )

    tipo_cliente = pedido["tipo_cliente"]
    return {
        "cliente": pedido["cliente"],
        "tipo_cliente": tipo_cliente,
        "valor_base": pedido_refatorado.calcular_valor_base(pedido["itens"]),
        "valor_original": valor_original,
        "valor_refatorado": valor_refatorado,
        "fatura_original": fatura_original,
        "fatura_refatorada": fatura_refatorada,
        "preservado": (
            valor_original == valor_refatorado
            and fatura_original == fatura_refatorada
        ),
    }


def exemplo_por_tipo(tipo: str | None) -> dict:
    """Devolve o exemplo pedido ou o exemplo predefinido (VIP)."""
    chave = (tipo or "").strip().upper()
    return EXEMPLOS.get(chave, EXEMPLOS[TIPO_PREDEFINIDO])


def resumo_exemplos() -> list[dict]:
    """Dados necessários para apresentar as três opções de cliente."""
    resumo = []
    for tipo, pedido in EXEMPLOS.items():
        valor_base = pedido_refatorado.calcular_valor_base(pedido["itens"])
        total = pedido_refatorado.aplicar_desconto_cliente(valor_base, tipo)
        resumo.append(
            {
                "tipo": tipo,
                "cliente": pedido["cliente"],
                "valor_base": valor_base,
                "total": total,
                "percentagem": int(
                    round(TAXAS_DESCONTO.get(tipo, 0.0) * 100)
                ),
            }
        )
    return resumo


def ler_resultados_testes() -> dict | None:
    """Lê o relatório gerado pela última execução real do pytest.

    O ficheiro é produzido localmente ou na CI através de
    ``CODELAB_RESULTS_PATH``. O servidor nunca executa pytest.
    """
    if not FICHEIRO_RESULTADOS.exists():
        return None

    try:
        dados = json.loads(FICHEIRO_RESULTADOS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    dados["data_legivel"] = _formatar_data(dados.get("gerado_em"))
    return dados


def _formatar_data(iso: str | None) -> str:
    if not iso:
        return "data não registada"

    try:
        data = datetime.fromisoformat(iso)
    except ValueError:
        return "data não registada"

    return (
        f"{data.day} de {MESES[data.month - 1]} de {data.year}, "
        f"às {data:%H:%M} (hora de Luanda)"
    )


__all__ = [
    "EXEMPLOS",
    "TIPO_PREDEFINIDO",
    "executar_comparacao",
    "exemplo_por_tipo",
    "ler_resultados_testes",
    "resumo_exemplos",
]
