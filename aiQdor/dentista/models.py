from django.db import models

# ------------------------------------------------------------------------- #
                    # Classes do Dentista
# ------------------------------------------------------------------------- #

class Dentista(models.Model):
    # PK
    CRO = models.CharField(max_length=40, primary_key=True)
    nome = models.CharField(max_length=40)
    especialidade = models.CharField(max_length=40)

    def __str__(self):
        return f'Dr. {self.nome}'