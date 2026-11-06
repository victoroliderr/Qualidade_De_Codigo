def processar_usuario(usuario):
    if usuario["admin"]:
        print("Notificando admin:", usuario["nome"])
