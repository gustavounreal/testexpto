# Generated by Django 5.1.2 on 2024-11-02 01:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_nome_vendedor_cadastrovendas_vendedor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boleto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_boleto', models.IntegerField()),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_vencimento', models.DateField()),
                ('status_pagamento', models.CharField(choices=[('pendente', 'Pendente'), ('pago', 'Pago')], default='pendente', max_length=20)),
                ('data_pagamento', models.DateField(blank=True, null=True)),
                ('venda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boletos', to='users.cadastrovendas')),
            ],
        ),
    ]