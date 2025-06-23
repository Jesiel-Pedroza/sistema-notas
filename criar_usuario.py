from models import criar_usuario, buscar_usuario_por_email

# Criar o usuário Jesiel
criar_usuario("Jesiel", "jesiel@jespedsys.com.br", "admin123")

# Verificar se foi criado com sucesso
usuario = buscar_usuario_por_email("jesiel@jespedsys.com.br")
if usuario:
    print("Usuário encontrado:", dict(usuario))
else:
    print("Usuário NÃO encontrado.")
