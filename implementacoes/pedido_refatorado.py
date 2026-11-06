"""Implementação refatorada do processamento de pedidos (referência académica)."""


def _formatar(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def calcular_valor_base(itens):
    return sum(item['preco'] * item['quantidade'] for item in itens)


def aplicar_desconto_cliente(valor_base, tipo_cliente):
    taxas_desconto = {
        'VIP': 0.10,
        'PREMIUM': 0.15
    }
    desconto = taxas_desconto.get(tipo_cliente, 0.0)
    return valor_base * (1 - desconto)


def emitir_fatura_impressa(nome_cliente, tipo_cliente, valor_base, valor_total):
    taxa = 0.0
    if tipo_cliente == 'VIP':
        taxa = 0.10
    elif tipo_cliente == 'PREMIUM':
        taxa = 0.15
    print("----------- FACTURA -----------")
    print("")
    print(f"Cliente: {nome_cliente}")
    print(f"Tipo: {tipo_cliente}")
    print("")
    print(f"Valor base: {_formatar(valor_base)} Kz")
    print(f"Desconto: {int(taxa * 100)}%")
    print("")
    print(f"TOTAL A PAGAR: {_formatar(valor_total)} Kz")
    print("")
    print("-------------------------------")


def processar_pedido(pedido):
    valor_base = calcular_valor_base(pedido['itens'])
    total_com_desconto = aplicar_desconto_cliente(
        valor_base,
        pedido['tipo_cliente']
    )
    emitir_fatura_impressa(
        pedido['cliente'],
        pedido['tipo_cliente'],
        valor_base,
        total_com_desconto
    )
    return total_com_desconto
