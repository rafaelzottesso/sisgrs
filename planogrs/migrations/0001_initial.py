# Generated by Django 2.1.7 on 2019-08-15 17:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import planogrs.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Armazenamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=15, unique=True, verbose_name='Código')),
                ('descricao', models.CharField(max_length=250, verbose_name='Descrição')),
            ],
            options={
                'ordering': ['codigo'],
            },
        ),
        migrations.CreateModel(
            name='Classe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=15)),
                ('descricao', models.CharField(max_length=250, verbose_name='Descrição')),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Cnae',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=50, unique=True, verbose_name='Código')),
                ('descricao', models.CharField(max_length=50, verbose_name='Descrição')),
            ],
            options={
                'ordering': ['codigo'],
                'verbose_name': 'CNAE',
            },
        ),
        migrations.CreateModel(
            name='DestinacaoFinal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=15, unique=True, verbose_name='Código')),
                ('descricao', models.CharField(max_length=250, verbose_name='Descrição')),
            ],
            options={
                'verbose_name_plural': 'Destinações Finais',
                'ordering': ['codigo'],
                'verbose_name': 'Destinação Final',
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnpj', models.CharField(max_length=18, unique=True, verbose_name='CNPJ')),
                ('razao_social', models.CharField(max_length=75, verbose_name='Razão Social')),
                ('nome_fantasia', models.CharField(max_length=75)),
                ('atividade_especifica', models.CharField(blank=True, help_text='(Conforme Alvará)', max_length=200, null=True, verbose_name='Atividade Específica')),
                ('inscricao_estadual', models.CharField(blank=True, max_length=50, null=True, verbose_name='Inscrição Estadual')),
                ('cadastro_imobiliario', models.CharField(max_length=50, verbose_name='Cadastro Imobiliário')),
                ('cep', models.CharField(max_length=10, verbose_name='CEP')),
                ('endereco', models.CharField(max_length=100, verbose_name='Endereço')),
                ('bairro', models.CharField(max_length=100)),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
                ('complemento', models.CharField(blank=True, max_length=100, null=True)),
                ('telefone_comercial', models.CharField(max_length=16)),
                ('telefone_celular', models.CharField(max_length=16)),
                ('email', models.CharField(max_length=100, verbose_name='Email')),
                ('nome_tecnico', models.CharField(max_length=200, verbose_name='Nome')),
                ('conselho_numero_tecnico', models.CharField(max_length=50, verbose_name='Número conselho')),
                ('rg_tecnico', models.CharField(max_length=20, verbose_name='RG')),
                ('cpf_tecnico', models.CharField(max_length=14, verbose_name='CPF')),
                ('telefone_tecnico', models.CharField(max_length=16, verbose_name='Telefone')),
                ('email_tecnico', models.CharField(max_length=50, verbose_name='Email')),
                ('art_num', models.CharField(max_length=50, verbose_name='Número ART')),
                ('art_anexo', models.FileField(null=True, upload_to=planogrs.models.user_directory_path, verbose_name='Anexo ART')),
                ('licenca_iap', models.CharField(choices=[('s', 'Sim'), ('n', 'Não')], max_length=2, verbose_name='Possui licença no IAP?')),
                ('num_lincenca', models.CharField(blank=True, max_length=50, null=True, verbose_name='Numero Licença')),
                ('num_protocolo', models.CharField(blank=True, max_length=10, null=True, verbose_name='Número de Protocolo')),
                ('data_validade', models.DateField(blank=True, null=True, verbose_name='Data de validade')),
                ('area_construida', models.CharField(max_length=250, verbose_name='Área Construída')),
                ('descricao_empreendimento', models.CharField(max_length=250, verbose_name='Descrição do Empreendimento')),
                ('descricao_processo_produtivo', models.CharField(blank=True, max_length=250, null=True, verbose_name='Descrição do Processo Produtivo')),
                ('metas_minimizacao', models.CharField(blank=True, max_length=250, null=True, verbose_name='Metas de Minimização')),
                ('acoes_preventivas', models.CharField(blank=True, max_length=250, null=True, verbose_name='Ações Preventivas')),
                ('cnae', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='planogrs.Cnae', verbose_name='CNAE')),
            ],
            options={
                'ordering': ['nome_fantasia'],
            },
        ),
        migrations.CreateModel(
            name='PrestadorServico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnpj', models.CharField(max_length=18, unique=True, verbose_name='CNPJ')),
                ('razao_social', models.CharField(max_length=50, verbose_name='Razão Social')),
                ('nome_fantasia', models.CharField(max_length=50)),
                ('cep', models.CharField(max_length=10, verbose_name='CEP')),
                ('endereco', models.CharField(max_length=100, verbose_name='Endereço')),
                ('bairro', models.CharField(max_length=100)),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
                ('complemento', models.CharField(blank=True, max_length=100, null=True)),
                ('telefone_comercial', models.CharField(max_length=16)),
                ('telefone_celular', models.CharField(blank=True, max_length=16, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True, verbose_name='Email')),
            ],
            options={
                'verbose_name_plural': 'Prestadores de Serviços',
                'ordering': ['razao_social'],
                'verbose_name': 'Prestador de Serviços',
            },
        ),
        migrations.CreateModel(
            name='Residuo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=15, unique=True, verbose_name='Código')),
                ('descricao', models.CharField(max_length=250, verbose_name='Descrição')),
                ('classificacao', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='planogrs.Classe', verbose_name='Classificação')),
            ],
            options={
                'ordering': ['codigo'],
                'verbose_name': 'Resíduo',
            },
        ),
        migrations.CreateModel(
            name='ResiduosSetor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('especificar_residuo', models.CharField(max_length=250, verbose_name='Específicar Resíduo')),
                ('estado_fisico', models.CharField(max_length=10, verbose_name='Estado Físico')),
                ('especificar_armazenamento', models.CharField(max_length=250)),
                ('especificar_destinacao_final', models.CharField(max_length=250, verbose_name='Especificar Destinação Final')),
                ('volume', models.FloatField(default=0, max_length=20)),
                ('unidade_medida', models.CharField(choices=[('un', 'un'), ('g', 'g'), ('kg', 'kg'), ('ton', 'ton'), ('m', 'm'), ('m²', 'm²'), ('m³', 'm³'), ('l', 'l'), ('l/s', 'l/s'), ('kW', 'kW'), ('MW', 'MW')], max_length=4, verbose_name='Unidade de medida')),
                ('periodicidade_coleta', models.CharField(choices=[('dia', 'Diário'), ('sem', 'Semanal'), ('qui', 'Quinzenal'), ('men', 'Mensal'), ('bim', 'Bimestral'), ('tri', 'Trimestral'), ('qua', 'Quadrimestral'), ('sem', 'Semestral'), ('anu', 'Anual')], max_length=4, verbose_name='Peridicidade de coleta')),
                ('informacoes_complementares', models.CharField(blank=True, max_length=250, null=True, verbose_name='Informações Complementares')),
                ('armazenamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='planogrs.Armazenamento')),
                ('destinacao_final', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='planogrs.DestinacaoFinal', verbose_name='Destinação Final')),
                ('prestador_servico', models.ForeignKey(help_text='Busque por Razão Social, Nome Fantasia ou CNPJ.', on_delete=django.db.models.deletion.PROTECT, to='planogrs.PrestadorServico', verbose_name='Prestadores de Serviços')),
                ('residuo', models.ForeignKey(help_text='Busque pelo código ou parte da descrição do resíduo.', on_delete=django.db.models.deletion.PROTECT, to='planogrs.Residuo', verbose_name='Resíduo')),
            ],
            options={
                'verbose_name_plural': 'Resíduos por Setor',
                'ordering': ['setor'],
                'verbose_name': 'Resíduo por Setor',
            },
        ),
        migrations.CreateModel(
            name='ResponsavelJuridico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('rg', models.CharField(max_length=20, verbose_name='RG')),
                ('cpf', models.CharField(max_length=14, verbose_name='CPF')),
                ('telefone', models.CharField(blank=True, max_length=16, null=True)),
                ('email', models.CharField(max_length=50, verbose_name='Email')),
                ('cargo', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Responsáveis Juridicos',
                'ordering': ['nome'],
                'verbose_name': 'Responsável Juridico',
            },
        ),
        migrations.CreateModel(
            name='Setor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('informacoes_complementares', models.CharField(blank=True, max_length=250, null=True, verbose_name='Informações Complementares')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Setores',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Situacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_movimentacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de movimentação')),
                ('informacoes_complementares', models.CharField(help_text='Este é o espaço que você tem para justificar a submissão do plano para essa Situação. Tamanho: 0/250.', max_length=250, verbose_name='Informações Complementares')),
                ('movimentado_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='movimentado_por', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Situações',
                'ordering': ['data_movimentacao'],
                'verbose_name': 'Situação',
            },
        ),
        migrations.CreateModel(
            name='TipoResiduo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('informacoes_complementares', models.CharField(max_length=250, verbose_name='Informações Complementares')),
            ],
            options={
                'verbose_name_plural': 'Tipos de Resíduos',
                'ordering': ['nome'],
                'verbose_name': 'Tipo de Resíduos',
            },
        ),
        migrations.CreateModel(
            name='TipoSituacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, unique=True)),
                ('cor', models.CharField(choices=[('primary', 'primary'), ('secondary', 'secondary'), ('warning', 'warning'), ('danger', 'danger'), ('success', 'success'), ('light', 'light'), ('dark', 'dark'), ('info', 'info')], default='primary', max_length=10)),
                ('pode_alterar_cadastros', models.CharField(choices=[('s', 'Sim'), ('n', 'Não')], default='n', help_text='Se sim, irá permitir que a Empresa possa alterar os dados cadastrados no sistema.', max_length=2, verbose_name='Permitir alteração nos cadastros?')),
            ],
        ),
        migrations.AddField(
            model_name='situacao',
            name='tipo_situacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='planogrs.TipoSituacao', verbose_name='Status da Situação'),
        ),
        migrations.AddField(
            model_name='situacao',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='residuossetor',
            name='setor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='planogrs.Setor'),
        ),
        migrations.AddField(
            model_name='residuossetor',
            name='tipo_residuo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='planogrs.TipoResiduo', verbose_name='Tipo de Resíduo'),
        ),
        migrations.AddField(
            model_name='residuossetor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='empresa',
            name='responsavel_juridico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='planogrs.ResponsavelJuridico', verbose_name='Resposável Jurídico'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='responsaveljuridico',
            unique_together={('user', 'cpf')},
        ),
    ]
