from django.contrib import admin

from dentista.models import Dentista

from consulta.models import Consulta, Procedimento

# Register your models here.

admin.site.register(Consulta)

admin.site.register(Dentista)

admin.site.register(Procedimento)