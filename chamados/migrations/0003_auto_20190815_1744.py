# Generated by Django 2.1.7 on 2019-08-15 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chamados', '0002_auto_20190815_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamado',
            name='fechado_em',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Fechado em'),
        ),
    ]
