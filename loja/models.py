from django.conf import settings
from django.db import models


class Categoria(models.Model):
    nome = models.CharField('Nome', max_length=60, unique=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField('Nome', max_length=100)
    preco = models.DecimalField('Preço (R$)', max_digits=8, decimal_places=2)
    estoque = models.PositiveIntegerField('Estoque', default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='produtos')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Venda(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='vendas')
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='vendas')
    quantidade = models.PositiveIntegerField('Quantidade')
    valor_total = models.DecimalField('Total (R$)', max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.quantidade}x {self.produto} ({self.criado_em:%d/%m/%Y})'
