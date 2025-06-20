from models import criar_usuario, buscar_usuario_por_email

# Criar o usuário
criar_usuario("Administrador", "admin@teste.com", "123456")

# Verificar se foi criado com sucesso
usuario = buscar_usuario_por_email("admin@teste.com")
if usuario:
    print("Usuário encontrado:", dict(usuario))
else:
    print("Usuário NÃO encontrado.")
