#--------- Django ------------#
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
#-----------------------------#

#---------- Models -----------#
from consulta.models import Consulta, Procedimento
from django.db.models import Sum
#-----------------------------#

#------------ Paginação -----------------#
from django.core.paginator import Paginator
#----------------------------------------#

#------------ Form ---------------#
from .forms import ConsultaCreateForm, ConsultaEditForm
#---------------------------------#


@login_required
def user_consulta(request):

    user = request.user

    usuario_consulta_lista = Consulta.objects.filter(pacienteCPF=user).order_by('dataC')
    #procedimentos = usuario_consulta_lista.procedimentos.all()

    paginator = Paginator(usuario_consulta_lista, 2)

    page = request.GET.get('page')

    usuario_consulta = paginator.get_page(page)
    #procedimentos = usuario_consulta.procedimentos.all()

    context = {
        'usuario_consulta': usuario_consulta,
        #'proc': procedimentos,
    }

    return render(request, 'consulta/user_consulta.html', context)

class AgendarConsultaView(View):

    form_class = ConsultaCreateForm
    template_name = 'consulta/agendar_consulta.html'
    redirect_name = 'user-consulta'


    def get(self, request):
        form = self.form_class()

        context = {'form': form }

        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        #user = request.user

        form.set_user(request)

        if form.is_valid():
            consulta = form.save(commit=False)
            
            user = request.user
            
            consulta.pacienteCPF = user

            form.save()

            proc = consulta.procedimentos.aggregate(Sum('preco'))
            
            consulta.precoC = proc['preco__sum'] 

            # next    

            form.save()    

            return redirect(self.redirect_name)

        context = {'form': form }

        return render(request, self.template_name, context)    


class EditarConsultaView(View):

    form_class = ConsultaEditForm
    template_name = 'consulta/editar_consulta.html'
    redirect_name = 'user-consulta'

    
    def get(self, request, id):
        con = get_object_or_404(Consulta, pk=id) 

        form = self.form_class(instance=con)

        context = {
            'form': form
        }

        return render(request, self.template_name, context)

   
    def post(self, request, id):
        con = get_object_or_404(Consulta, pk=id)

        form = self.form_class(request.POST, instance=con)

        form.set_user(request)

        if form.is_valid():
            consulta = form.save(commit=False)
            
            user = request.user
            
            consulta.pacienteCPF = user

            form.save()

            proc = consulta.procedimentos.aggregate(Sum('preco'))
            
            consulta.precoC = proc['preco__sum'] 

            form.save()

            return redirect(self.redirect_name)
        

        context = {
            'form': form
        }

        return render(request, self.template_name, context)


class DesmarcarConsultaView(View):

    redirect_name = 'user-consulta'

    def get(self, request, id):
        consulta = get_object_or_404(Consulta, pk=id)
        consulta.delete()
        
        return redirect(self.redirect_name)
    
    def post(self, request):
        pass
