from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tipo(models.Model):
    descricao = models.CharField(max_length=30, verbose_name="Descrição")

    def __str__(self):
        return "{}".format(self.descricao)

    class Meta:
        ordering = ['descricao']


class Chamado(models.Model):
    aberto_por   = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Aberto por", related_name='aberto')
    aberto_em    = models.DateTimeField(auto_now_add=True, verbose_name="Aberto em")
    tipo         = models.ForeignKey(Tipo, on_delete=models.PROTECT)
    assunto      = models.CharField(max_length=100)
    descricao    = models.CharField(max_length=500, verbose_name="Descrição")
    fechado_em   = models.DateTimeField(null=True, blank=True, verbose_name="Fechado em")
    fechado_por  = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Fechado por", related_name='fechado')

    def __str__(self):
        return "[{}] {} ({})".format(self.aberto_por, self.descricao, self.fechado_em)

    class Meta:
        ordering = ['-aberto_em', 'aberto_por']


class Mensagem(models.Model):
    chamado   = models.ForeignKey(Chamado, on_delete=models.PROTECT, max_length=15)
    user      = models.ForeignKey(User, on_delete=models.PROTECT, max_length=250, verbose_name="Usuario")
    mensagem  = models.CharField(max_length=500)
    data      = models.DateTimeField(auto_now_add=True)   

    def __str__(self):
        return "[{}] {}".format(self.chamado.id, self.mensagem)

    class Meta:
        ordering = ["data"]
        verbose_name_plural = "Mensagens"
