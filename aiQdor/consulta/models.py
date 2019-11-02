from django.db import models

from dentista.models import Dentista

from user.models import Paciente, PacienteManager

# ------------------------------------------------------------------------- #
                # Classes da Consulta
# ------------------------------------------------------------------------- #

class Procedimento(models.Model):
    nome = models.CharField(max_length=40)
    descricao = models.CharField(max_length=40)
    preco = models.FloatField() 

    def __str__(self):
        return f'{self.nome} : R$ {self.preco}'

class Consulta(models.Model):
    # Hora e Data da consulta
    dataC = models.DateField()
    horaC = models.TimeField()

    # FK's
    dentistaCRO = models.ForeignKey(Dentista, on_delete=models.PROTECT)
    pacienteCPF = models.ForeignKey(Paciente, on_delete=models.PROTECT)


    precoC = models.FloatField(null=True)

    procedimentos = models.ManyToManyField(Procedimento)

    # Choices -> pagamento
    pagamentos = [
        ('pago', 'Confirmado'),
        ('não pago', 'Não Pago'),
        ('á ser pago', 'Em andamento')
    ]
    statusPagamento = models.CharField(max_length=15, choices=pagamentos, default='á ser pago')

    # Choices -> status da consulta
    consultas = [
        ('realizada', 'Realizada'),
        ('á ser realizada', 'Á ser realizada'),
        ('cancelada', 'Cancelada'),
    ]
    statusConsulta = models.CharField(max_length=15, choices=consultas, default='á ser realizada') 

    def __str__(self):
        return f'Consulta de {self.pacienteCPF}, com {self.dentistaCRO}'
