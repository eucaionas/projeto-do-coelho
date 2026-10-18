from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.ProdutoLista.as_view(), name='produto_lista'),
    path('produtos/novo/', v.ProdutoCriar.as_view(), name='produto_criar'),
    path('produtos/<int:pk>/editar/', v.ProdutoEditar.as_view(), name='produto_editar'),
    path('produtos/<int:pk>/excluir/', v.ProdutoExcluir.as_view(), name='produto_excluir'),
    path('categorias/', v.CategoriaLista.as_view(), name='categoria_lista'),
    path('categorias/nova/', v.CategoriaCriar.as_view(), name='categoria_criar'),
    path('categorias/<int:pk>/editar/', v.CategoriaEditar.as_view(), name='categoria_editar'),
    path('categorias/<int:pk>/excluir/', v.CategoriaExcluir.as_view(), name='categoria_excluir'),
]
