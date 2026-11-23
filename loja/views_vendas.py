from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView

from .forms import VendaForm
from .models import Produto, Venda


class VendaLista(LoginRequiredMixin, ListView):
    model = Venda
    template_name = 'loja/venda_lista.html'
    context_object_name = 'vendas'

    def get_queryset(self):
        return Venda.objects.select_related('produto', 'vendedor')


class VendaCriar(LoginRequiredMixin, CreateView):
    model, form_class = Venda, VendaForm
    template_name = 'loja/form.html'
    success_url = reverse_lazy('venda_lista')
    extra_context = {'titulo': 'Nova venda', 'voltar': reverse_lazy('venda_lista')}

    @transaction.atomic
    def form_valid(self, form):
        produto = Produto.objects.select_for_update().get(pk=form.cleaned_data['produto'].pk)
        qtd = form.cleaned_data['quantidade']
        if produto.estoque < qtd:
            form.add_error('quantidade', f'Estoque insuficiente (disponível: {produto.estoque}).')
            return self.form_invalid(form)
        venda = form.save(commit=False)
        venda.vendedor = self.request.user
        venda.valor_total = produto.preco * qtd
        venda.save()
        produto.estoque -= qtd  # baixa automática no estoque
        produto.save(update_fields=['estoque'])
        messages.success(self.request, f'Venda registrada: {qtd}x {produto.nome}.')
        return redirect(self.success_url)


class VendaCancelar(LoginRequiredMixin, DeleteView):
    model = Venda
    template_name = 'loja/confirmar_exclusao.html'
    success_url = reverse_lazy('venda_lista')
    extra_context = {'voltar': reverse_lazy('venda_lista')}

    @transaction.atomic
    def form_valid(self, form):
        venda = self.object
        produto = Produto.objects.select_for_update().get(pk=venda.produto_id)
        produto.estoque += venda.quantidade  # devolve ao estoque
        produto.save(update_fields=['estoque'])
        messages.success(self.request, 'Venda cancelada e estoque devolvido.')
        return super().form_valid(form)
