from django.shortcuts import render
from django.core.paginator import Paginator

from dentista.models import Dentista

def listaDentista(request):
    dentistas_lista = Dentista.objects.all().order_by('nome')


    paginator = Paginator(dentistas_lista, 3)

    page = request.GET.get('page')

    dentistas = paginator.get_page(page)

    contexto = {
        'dentistas': dentistas
    }

    return render(request, 'dentista/listaDentista.html', contexto)