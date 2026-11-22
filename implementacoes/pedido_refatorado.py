"""Implementação refatorada do processamento de pedidos (referência académica).

A técnica aplicada é **Extrair Método**: cada responsabilidade passou a ter uma
função própria, com um nome que descreve aquilo que faz. A função
``processar_pedido`` limita-se a coordenar essas operações.
"""
from services.moeda import formatar_kwanzas

TAXAS_DESCONTO = {
    "VIP": 0.10,
    "PREMIUM": 0.15,
}


def calcular_valor_base(itens):
    """Soma o preço × quantidade de todos os itens da encomenda."""
    return sum(item["preco"] * item["quantidade"] for item in itens)


def aplicar_desconto_cliente(valor_base, tipo_cliente):
    """Aplica a taxa de desconto associada ao tipo de cliente."""
    taxa = TAXAS_DESCONTO.get(tipo_cliente, 0.0)
    return valor_base * (1 - taxa)


def emitir_fatura_impressa(
    nome_cliente,
    tipo_cliente,
    valor_base,
    valor_total,
    taxa_desconto,
):
    """Imprime a factura com o valor base, o desconto e o total a pagar."""
    print("----------- FACTURA -----------")
    print("")
    print(f"Cliente: {nome_cliente}")
    print(f"Tipo: {tipo_cliente}")
    print("")
    print(f"Valor base: {formatar_kwanzas(valor_base)}")
    print(f"Desconto: {int(round(taxa_desconto * 100))}%")
    print("")
    print(f"TOTAL A PAGAR: {formatar_kwanzas(valor_total)}")
    print("")
    print("-------------------------------")


def processar_pedido(pedido):
    """Coordena o cálculo, o desconto e a emissão da factura."""
    tipo_cliente = pedido["tipo_cliente"]
    valor_base = calcular_valor_base(pedido["itens"])
    valor_total = aplicar_desconto_cliente(valor_base, tipo_cliente)

    emitir_fatura_impressa(
        pedido["cliente"],
        tipo_cliente,
        valor_base,
        valor_total,
        TAXAS_DESCONTO.get(tipo_cliente, 0.0),
    )

    return valor_total
