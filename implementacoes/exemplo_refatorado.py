def notificar_admin(usuario):
    print("Notificando admin:", usuario["nome"])


def processar_usuario(usuario):
    if usuario["admin"]:
        notificar_admin(usuario)
