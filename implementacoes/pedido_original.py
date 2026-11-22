"""Implementação original do processamento de pedidos (referência académica).

Esta versão concentra numa única função o cálculo do valor base, a aplicação
do desconto e a emissão da factura. É esse acumular de responsabilidades que o
laboratório coloca em evidência.
"""
from services.moeda import formatar_kwanzas


def processar_pedido(pedido):
    total = 0
    for item in pedido["itens"]:
        total += item["preco"] * item["quantidade"]

    if pedido["tipo_cliente"] == "VIP":
        total = total * 0.90
    elif pedido["tipo_cliente"] == "PREMIUM":
        total = total * 0.85

    valor_base = sum(item["preco"] * item["quantidade"] for item in pedido["itens"])

    taxa = 0.0
    if pedido["tipo_cliente"] == "VIP":
        taxa = 0.10
    elif pedido["tipo_cliente"] == "PREMIUM":
        taxa = 0.15

    print("----------- FACTURA -----------")
    print("")
    print(f"Cliente: {pedido['cliente']}")
    print(f"Tipo: {pedido['tipo_cliente']}")
    print("")
    print(f"Valor base: {formatar_kwanzas(valor_base)}")
    print(f"Desconto: {int(round(taxa * 100))}%")
    print("")
    print(f"TOTAL A PAGAR: {formatar_kwanzas(total)}")
    print("")
    print("-------------------------------")

    return total
