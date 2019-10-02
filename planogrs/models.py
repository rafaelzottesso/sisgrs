from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from .validators import validate_CNPJ, validate_CPF

# Create your models here.


# class Estado(models.Model):
#     sigla = models.CharField(max_length=2)
#     nome = models.CharField(max_length=50)

#     def __str__(self):
#         return self.sigla + " - " + self.nome


# Unidades de medida
UNIDADES_CHOICES = [
    ('un', 'un'),
    ('g', 'g'),
    ('kg', 'kg'),
    ('ton', 'ton'),
    ('m', 'm'),
    ('m²', 'm²'),
    ('m³', 'm³'),
    ('l', 'l'),
    ('l/s', 'l/s'),
    ('kW', 'kW'),
    ('MW', 'MW')
]

PERIODO_CHOICES = [
    ('dia', 'Diário'),
    ('sem', 'Semanal'),
    ('qui', 'Quinzenal'),
    ('men', 'Mensal'),
    ('bim', 'Bimestral'),
    ('tri', 'Trimestral'),
    ('qua', 'Quadrimestral'),
    ('sem', 'Semestral'),
    ('anu', 'Anual')
]

CORES_BS4_CHOICES = [
    ('primary', 'primary'),
    ('secondary', 'secondary'),
    ('warning', 'warning'),
    ('danger', 'danger'),
    ('success', 'success'),
    ('light', 'light'),
    ('dark', 'dark'),
    ('info', 'info'),
]

SIMNAO_CHOICES = [
    ('s', 'Sim'),
    ('n', 'Não'),
]

# Define o diretório padrão para salvar os arquivos enviados


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.user.id, filename)


class Classe(models.Model):
    nome        = models.CharField(max_length=15)
    descricao   = models.CharField(max_length=250, verbose_name="Descrição")

    def __str__(self):
        return self.nome + " - " + self.descricao

    class Meta:
        ordering = ["nome"]


class Residuo(models.Model):
    codigo          = models.CharField(max_length=15, verbose_name="Código", unique=True)
    descricao       = models.CharField(max_length=500, verbose_name="Descrição")
    classificacao   = models.ForeignKey(Classe, on_delete=models.PROTECT, verbose_name="Classificação")

    def __str__(self):
        return "[{}] {}".format(self.codigo, self.descricao)

    class Meta:
        ordering            = ["codigo"]
        verbose_name        = "Resíduo"


class Setor(models.Model):
    user                        = models.ForeignKey(User, on_delete=models.PROTECT)
    nome                        = models.CharField(max_length=50)
    informacoes_complementares  = models.CharField(max_length=250, null=True, blank=True, verbose_name="Informações Complementares")  # NULL

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ["nome"]
        verbose_name_plural = "Setores"


class TipoResiduo(models.Model):
    nome                        = models.CharField(max_length=50)
    informacoes_complementares  = models.CharField(max_length=250, verbose_name="Informações Complementares")

    def __str__(self):
        return self.nome

    class Meta:
        ordering            = ["nome"]
        verbose_name        = "Tipo de Resíduos"
        verbose_name_plural = "Tipos de Resíduos"

class Armazenamento(models.Model):
    codigo      = models.CharField(max_length=15, verbose_name="Código", unique=True)
    descricao   = models.CharField(max_length=250, verbose_name="Descrição")

    def __str__(self):
        return "[{}] {}".format(self.codigo, self.descricao)

    class Meta:
        ordering = ["codigo"]


class DestinacaoFinal(models.Model):
    codigo      = models.CharField(max_length=15, verbose_name="Código", unique=True)
    descricao   = models.CharField(max_length=250, verbose_name="Descrição")

    def __str__(self):
        return "[{}] {}".format(self.codigo, self.descricao)

    class Meta:
        ordering            = ["codigo"]
        verbose_name        = "Destinação Final"
        verbose_name_plural = "Destinações Finais"

# Lado Empresa


class ResponsavelJuridico(models.Model):
    user        = models.ForeignKey(User, on_delete=models.PROTECT)
    nome        = models.CharField(max_length=200)
    rg          = models.CharField(max_length=20, verbose_name="RG")
    cpf         = models.CharField(max_length=14, verbose_name="CPF", validators=[validate_CPF])
    telefone    = models.CharField(max_length=16, null=True, blank=True)  # null
    email       = models.CharField(max_length=50, verbose_name="Email")
    cargo       = models.CharField(max_length=50, null=True, blank=True)  # null

    def __str__(self):
        return "{} {}".format(self.nome, self.cargo)

    class Meta:
        ordering            = ["nome"]
        verbose_name        = "Responsável Juridico"
        verbose_name_plural = "Responsáveis Juridicos"
        unique_together     = [["user", "cpf"]]

class Cnae(models.Model):
    # user = models.ForeignKey(User, on_delete=models.PROTECT) VAI SER CADSTRADO PELA PREFEITURA
    codigo      = models.CharField(max_length=50, verbose_name="Código", unique=True)
    descricao   = models.CharField(max_length=250, verbose_name="Descrição")

    def __str__(self):
        return "{} {}".format(self.codigo, self.descricao)

    class Meta:
        ordering        = ["codigo"]
        verbose_name    = "CNAE"


class PrestadorServico(models.Model):
    cnpj                = models.CharField(max_length=18, verbose_name="CNPJ", unique=True, validators=[validate_CNPJ])
    razao_social        = models.CharField(max_length=100, verbose_name="Razão Social")
    nome_fantasia       = models.CharField(max_length=100)
    cnae                = models.ForeignKey(Cnae, on_delete=models.PROTECT, verbose_name="CNAE", null=True)
    cep                 = models.CharField(max_length=10, verbose_name="CEP")
    endereco            = models.CharField(max_length=100, verbose_name="Endereço")
    bairro              = models.CharField(max_length=100)
    numero              = models.CharField(max_length=10, verbose_name="Número")
    complemento         = models.CharField(max_length=100, null=True, blank=True)  # NULL
    telefone_comercial  = models.CharField(max_length=16)
    telefone_celular    = models.CharField(max_length=16, null=True, blank=True)  # NULL
    email               = models.CharField(max_length=100, null=True, blank=True, verbose_name="Email")  # NULL

    def __str__(self):
        return "{} - {}".format(self.nome_fantasia, self.cnpj)

    class Meta:
        ordering            = ["razao_social"]
        verbose_name        = "Prestador de Serviços"
        verbose_name_plural = "Prestadores de Serviços"

# class MeusPrestadores(models.Model):
 #   user = models.ForeignKey(User, on_delete=models.PROTECT)
  #  prestador_servico = models.ForeignKey(PrestadorServico, on_delete=models.PROTECT)
#
 #   def __str__(self):
  #          return "{} {}".format(self.user, self.prestador_servico)


class Empresa(models.Model):
    user                            = models.OneToOneField(User, on_delete=models.PROTECT)

    cnpj                            = models.CharField(max_length=18, verbose_name="CNPJ", unique=True, validators=[validate_CNPJ])
    razao_social                    = models.CharField(max_length=100, verbose_name="Razão Social")
    nome_fantasia                   = models.CharField(max_length=100)
    cnae                            = models.ForeignKey(Cnae, on_delete=models.PROTECT, verbose_name="CNAE", null=True)
    atividade_especifica            = models.CharField(max_length=200, help_text="(Conforme Alvará)", null=True, blank=True, verbose_name="Atividade Específica")  # null
    inscricao_estadual              = models.CharField(max_length=50, null=True, blank=True, verbose_name="Inscrição Estadual")  # null
    cadastro_imobiliario            = models.CharField(max_length=50, verbose_name="Cadastro Imobiliário")
    cep                             = models.CharField(max_length=10, verbose_name="CEP")
    endereco                        = models.CharField(max_length=100, verbose_name="Endereço")
    bairro                          = models.CharField(max_length=100)
    numero                          = models.CharField(max_length=10, verbose_name="Número")
    complemento                     = models.CharField(max_length=100, null=True, blank=True)  # null
    telefone_comercial              = models.CharField(max_length=16)
    telefone_celular                = models.CharField(max_length=16)
    email                           = models.CharField(max_length=100, verbose_name="Email", help_text="Apenas para envio de notificações. Este não é o email para login ou recuperação de senha.")

    nome_tecnico                    = models.CharField(max_length=200, verbose_name="Nome")
    conselho_numero_tecnico         = models.CharField(max_length=50, verbose_name="Número conselho")
    rg_tecnico                      = models.CharField(max_length=20, verbose_name="RG")
    cpf_tecnico                     = models.CharField(max_length=14, verbose_name="CPF", validators=[validate_CPF])
    telefone_tecnico                = models.CharField(max_length=16, verbose_name="Telefone")
    email_tecnico                   = models.CharField(max_length=50, verbose_name="Email")
    art_num                         = models.CharField(max_length=50, verbose_name="Número ART")
    art_anexo                       = models.FileField(upload_to=user_directory_path, verbose_name="Anexo ART", null=True)

    licenca_iap                     = models.CharField(max_length=2, choices=SIMNAO_CHOICES, verbose_name="Possui licença no IAP?")
    num_lincenca                    = models.CharField(max_length=50, null=True, blank=True, verbose_name="Numero Licença")  # NULL
    num_protocolo                   = models.CharField(max_length=10, null=True, blank=True, verbose_name="Número de Protocolo")    # NULL
    data_validade                   = models.DateField(null=True, blank=True, verbose_name="Data de validade")   # NULL
    
    area_construida                 = models.CharField(max_length=250, verbose_name="Área Construída")
    descricao_empreendimento        = models.CharField(max_length=250, verbose_name="Descrição do Empreendimento")
    descricao_processo_produtivo    = models.CharField(max_length=250, null=True, blank=True, verbose_name="Descrição do Processo Produtivo")  # NULL
    metas_minimizacao               = models.CharField(max_length=250, null=True, blank=True, verbose_name="Metas de Minimização")  # NULL
    acoes_preventivas               = models.CharField(max_length=250, null=True, blank=True, verbose_name="Ações Preventivas")  # NULL
    # responsavel_juridico            = models.ForeignKey(ResponsavelJuridico, null=True, blank=True, on_delete=models.PROTECT, verbose_name="Resposável Jurídico")   # NULL

    def __str__(self):
        return "{} - {}".format(self.nome_fantasia, self.cnpj)

    class Meta:
        ordering = ["nome_fantasia"]


class TipoSituacao(models.Model):
    nome                    = models.CharField(max_length=50, unique=True)
    cor                     = models.CharField(max_length=10, choices=CORES_BS4_CHOICES, default='primary')
    pode_alterar_cadastros  = models.CharField(
        max_length=2, choices=SIMNAO_CHOICES, verbose_name="Permitir alteração nos cadastros?",
        help_text="Se sim, irá permitir que a Empresa possa alterar os dados cadastrados no sistema.",
        default='n')

    def __str__(self):
        return self.nome


class Situacao(models.Model):
    user                        = models.ForeignKey(User, on_delete=models.PROTECT)
    movimentado_por = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="movimentado_por")
    data_movimentacao           = models.DateTimeField(auto_now_add=True, verbose_name="Data de movimentação")
    tipo_situacao               = models.ForeignKey(TipoSituacao, on_delete=models.PROTECT, verbose_name="Status da Situação")
    informacoes_complementares  = models.CharField(max_length=250, verbose_name="Informações Complementares",
        help_text="Este é o espaço que você tem para justificar a submissão do plano para essa Situação. Tamanho: 0/250.")

    def __str__(self):
        return self.user.empresa.cnpj + ' - ' +self.tipo_situacao.nome

    class Meta:
        ordering            = ["data_movimentacao"]
        verbose_name        = "Situação"
        verbose_name_plural = "Situações"


class ResiduosSetor(models.Model):
    user                            = models.ForeignKey(User, on_delete=models.PROTECT)
    tipo_residuo                    = models.ForeignKey(TipoResiduo, on_delete=models.PROTECT, verbose_name="Tipo de Resíduo")
    setor                           = models.ForeignKey(Setor, on_delete=models.PROTECT)
    residuo                         = models.ForeignKey(Residuo, on_delete=models.PROTECT, verbose_name="Resíduo", help_text="Busque pelo código ou parte da descrição do resíduo.")
    especificar_residuo             = models.CharField(max_length=250, verbose_name="Específicar Resíduo")
    estado_fisico                   = models.CharField(max_length=10, verbose_name="Estado Físico")  # ********
    armazenamento                   = models.ForeignKey(Armazenamento, on_delete=models.PROTECT)
    especificar_armazenamento       = models.CharField(max_length=250)
    destinacao_final                = models.ForeignKey(DestinacaoFinal, on_delete=models.PROTECT, verbose_name="Destinação Final")
    especificar_destinacao_final    = models.CharField(max_length=250, verbose_name="Especificar Destinação Final")
    volume                          = models.FloatField(max_length=20, default=0)
    unidade_medida                  = models.CharField(max_length=4, choices=UNIDADES_CHOICES, verbose_name="Unidade de medida")
    periodicidade_coleta            = models.CharField(max_length=4, choices=PERIODO_CHOICES, verbose_name="Peridicidade de coleta")
    prestador_servico               = models.ForeignKey(PrestadorServico, on_delete=models.PROTECT, verbose_name="Prestadores de Serviços", help_text="Busque por Razão Social, Nome Fantasia ou CNPJ.")  # Pode selecionar mais de uma
    informacoes_complementares      = models.CharField(max_length=250, null=True, blank=True, verbose_name="Informações Complementares")  # NULL

    def __str__(self):
        return "{} ({}) - {}".format(self.especificar_residuo, self.setor, self.residuo.descricao)

    class Meta:
        ordering            = ["setor"]
        verbose_name        = "Resíduo por Setor"
        verbose_name_plural = "Resíduos por Setor"
        # return "{} - {} - {} - {}".format(self.tipo_residuo.nome, self.setor.nome, self.residuo.codigo, self.prestador_servico.nome_fantasia)


# /Andamento inicial/ Enviou > /Pendente/ > Prefeitura > /Analise/ > (Falta alguma coisa?) > /Em adequação/ > Empresa (altera) >
#
