"""Implementação original do processamento de pedidos (referência académica)."""


def _formatar(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def processar_pedido(pedido):
    total = 0
    for item in pedido['itens']:
        total += item['preco'] * item['quantidade']

    if pedido['tipo_cliente'] == 'VIP':
        total = total * 0.90
    elif pedido['tipo_cliente'] == 'PREMIUM':
        total = total * 0.85

    valor_base = sum(item['preco'] * item['quantidade'] for item in pedido['itens'])
    taxa = 0.0
    if pedido['tipo_cliente'] == 'VIP':
        taxa = 0.10
    elif pedido['tipo_cliente'] == 'PREMIUM':
        taxa = 0.15

    print("----------- FACTURA -----------")
    print("")
    print(f"Cliente: {pedido['cliente']}")
    print(f"Tipo: {pedido['tipo_cliente']}")
    print("")
    print(f"Valor base: {_formatar(valor_base)} Kz")
    print(f"Desconto: {int(taxa * 100)}%")
    print("")
    print(f"TOTAL A PAGAR: {_formatar(total)} Kz")
    print("")
    print("-------------------------------")

    return total
