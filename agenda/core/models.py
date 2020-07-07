from django.db import models
# usuario logado
from django.contrib.auth.models import User


# makemigrations core
class Evento(models.Model):
    titulo = models.CharField(max_length=100, verbose_name='Título')
    descricao = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(verbose_name='Data do Evento')
    data_criacao = models.DateTimeField(auto_now=True, verbose_name='DAta da Criação')
    local = models.CharField(max_length=100, blank=True, null=True)
    # se o usuario for excluido os dados dele são deletados
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'evento'

    def __str__(self):
        return self.titulo

    def get_data_evento(self):
        return self.data_evento.strftime('%d/%m/%Y %H:%M')

# migrate
