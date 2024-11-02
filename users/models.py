from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from dateutil.relativedelta import relativedelta

class DadosUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14)
    endereco = models.CharField(max_length=255)
    cep = models.CharField(max_length=9)
    email = models.EmailField()
    banco = models.CharField(max_length=50)
    agencia = models.CharField(max_length=10)
    conta = models.CharField(max_length=20)
    pix = models.CharField(max_length=255)
    whatsapp = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.nome_completo


class CadastroVendas(models.Model):
    nome_completo = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    vendedor = models.ForeignKey(DadosUsuario, on_delete=models.CASCADE)
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_boletos = models.IntegerField()
    valor_por_boleto = models.DecimalField(max_digits=10, decimal_places=2)
    descricao_venda = models.TextField()
    forma_pagamento = models.CharField(max_length=10)
    chave_pix = models.CharField(max_length=100, blank=True, null=True)
    data_vencimento = models.DateField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Venda de {self.nome_completo} - {self.valor_venda}"
    

class Boleto(models.Model):
    venda = models.ForeignKey(CadastroVendas, on_delete=models.CASCADE, related_name="boletos")
    numero_boleto = models.IntegerField()  # Número sequencial do boleto na venda
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    status_pagamento = models.CharField(max_length=20, choices=[('pendente', 'Pendente'), ('pago', 'Pago')], default='pendente')
    data_pagamento = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Boleto {self.numero_boleto} da venda {self.venda.id} - {self.status_pagamento}"    


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=CadastroVendas)
def criar_boletos(sender, instance, created, **kwargs):
    if created:
        valor_por_boleto = instance.valor_venda / instance.quantidade_boletos
        data_vencimento = instance.data_vencimento
        if isinstance(data_vencimento, str):
            data_vencimento = datetime.strptime(data_vencimento, '%Y-%m-%d').date()
        for i in range(instance.quantidade_boletos):
            Boleto.objects.create(
                venda=instance,
                numero_boleto=i + 1,
                valor=valor_por_boleto,
                data_vencimento=data_vencimento + relativedelta(months=i)  # Incrementa 1 mês para cada boleto
            )