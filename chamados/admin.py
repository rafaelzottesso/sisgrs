from django.contrib import admin
from .models import Tipo, Chamado, Mensagem

# Register your models here.
admin.site.register(Tipo)
admin.site.register(Chamado)
admin.site.register(Mensagem)
