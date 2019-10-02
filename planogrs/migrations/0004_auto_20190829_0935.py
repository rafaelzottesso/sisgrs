# Generated by Django 2.1.7 on 2019-08-29 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planogrs', '0003_auto_20190815_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestadorservico',
            name='cnae',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='planogrs.Cnae', verbose_name='CNAE'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='email',
            field=models.CharField(help_text='Apenas para envio de notificações. Este não é o email para login ou recuperação de senha.', max_length=100, verbose_name='Email'),
        ),
    ]
