from django.contrib import admin
from .models import Classe, Residuo, Setor, TipoResiduo, Armazenamento, DestinacaoFinal, ResponsavelJuridico, Cnae, PrestadorServico, Empresa, TipoSituacao, Situacao, ResiduosSetor

# Register your models here.
admin.site.register(Classe)
admin.site.register(Residuo)
admin.site.register(Setor)
admin.site.register(TipoResiduo)
admin.site.register(Armazenamento)
admin.site.register(DestinacaoFinal)
admin.site.register(ResponsavelJuridico)
admin.site.register(Cnae)
admin.site.register(PrestadorServico)
admin.site.register(Empresa)
admin.site.register(TipoSituacao)
admin.site.register(Situacao)
admin.site.register(ResiduosSetor)