from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CategoriaForm, ProdutoForm
from .models import Categoria, Produto


class FormMixin:
    template_name = 'loja/form.html'
    msg = ''

    def form_valid(self, form):
        messages.success(self.request, self.msg)
        return super().form_valid(form)


# ---------- Produtos ----------
class ProdutoLista(ListView):
    model = Produto
    template_name = 'loja/produto_lista.html'
    context_object_name = 'produtos'

    def get_queryset(self):
        qs = Produto.objects.select_related('categoria')
        busca = self.request.GET.get('q', '').strip()
        return qs.filter(nome__icontains=busca) if busca else qs


class ProdutoCriar(FormMixin, CreateView):
    model, form_class = Produto, ProdutoForm
    success_url = reverse_lazy('produto_lista')
    msg = 'Produto cadastrado com sucesso.'
    extra_context = {'titulo': 'Novo produto', 'voltar': reverse_lazy('produto_lista')}


class ProdutoEditar(FormMixin, UpdateView):
    model, form_class = Produto, ProdutoForm
    success_url = reverse_lazy('produto_lista')
    msg = 'Produto atualizado com sucesso.'
    extra_context = {'titulo': 'Editar produto', 'voltar': reverse_lazy('produto_lista')}


class ProdutoExcluir(DeleteView):
    model = Produto
    template_name = 'loja/confirmar_exclusao.html'
    success_url = reverse_lazy('produto_lista')
    extra_context = {'voltar': reverse_lazy('produto_lista')}

    def form_valid(self, form):
        messages.success(self.request, 'Produto excluído.')
        return super().form_valid(form)


# ---------- Categorias ----------
class CategoriaLista(ListView):
    model = Categoria
    template_name = 'loja/categoria_lista.html'
    context_object_name = 'categorias'


class CategoriaCriar(FormMixin, CreateView):
    model, form_class = Categoria, CategoriaForm
    success_url = reverse_lazy('categoria_lista')
    msg = 'Categoria cadastrada com sucesso.'
    extra_context = {'titulo': 'Nova categoria', 'voltar': reverse_lazy('categoria_lista')}


class CategoriaEditar(FormMixin, UpdateView):
    model, form_class = Categoria, CategoriaForm
    success_url = reverse_lazy('categoria_lista')
    msg = 'Categoria atualizada com sucesso.'
    extra_context = {'titulo': 'Editar categoria', 'voltar': reverse_lazy('categoria_lista')}


class CategoriaExcluir(DeleteView):
    model = Categoria
    template_name = 'loja/confirmar_exclusao.html'
    success_url = reverse_lazy('categoria_lista')
    extra_context = {'voltar': reverse_lazy('categoria_lista')}

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, 'Não é possível excluir: existem produtos nesta categoria.')
            return redirect('categoria_lista')
        messages.success(self.request, 'Categoria excluída.')
        return response
