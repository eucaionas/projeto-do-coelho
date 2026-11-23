# Projeto do Coelho (Doce Gestão) - AV2 Django

Sistema web em Django com autenticação, sessão, mensagens e vendas.

## Funcionalidades
- Login, cadastro de conta e logout (sistema de autenticação do Django)
- Sessão com expiração de 2 minutos de inatividade e contador de páginas vistas
- Mensagens de sucesso e erro em todas as telas
- CRUD de Categorias e Produtos (ForeignKey)
- Vendas com baixa automática de estoque e devolução ao cancelar
## Como executar (Windows / PowerShell)
```
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Acesse http://127.0.0.1:8000, clique em "Criar conta", entre e cadastre
uma categoria, depois produtos e vendas.