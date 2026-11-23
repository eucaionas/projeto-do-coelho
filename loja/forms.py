from django import forms
from .models import Categoria, Produto, Venda


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'estoque', 'categoria']

    def clean_preco(self):
        preco = self.cleaned_data['preco']
        if preco <= 0:
            raise forms.ValidationError('O preço deve ser maior que zero.')
        return preco


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['produto', 'quantidade']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produto'].queryset = Produto.objects.filter(estoque__gt=0)  # só produtos com estoque

    def clean_quantidade(self):
        qtd = self.cleaned_data['quantidade']
        if qtd < 1:
            raise forms.ValidationError('A quantidade deve ser pelo menos 1.')
        return qtd
