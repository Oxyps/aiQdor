    from django import forms

#------------ Para configurar os fields ------------#
from django.forms import ModelForm, DateInput, TextInput, CharField, TimeInput
# Para trocar o nome do campo
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
#---------------------------------------------------#

#------------ Validação ------------#
from django.utils import timezone
import datetime
from datetime import time
from consulta.models import Consulta
#-----------------------------------#

#-------------- Models --------------------#
from consulta.models import Consulta
from django.db.models.functions import (
     ExtractWeekDay
)
#------------------------------------------#


class ConsultaCreateForm(forms.ModelForm):

    class Meta:
        model = Consulta
        fields = (
            'dentistaCRO',
            'dataC',
            'horaC',
            'procedimentos'
        )
        labels = {
            'dentistaCRO': _('Selecione um Denitsta:'),
            'dataC': _('Data da Consulta:'),
            'horaC': _('Horário da Consulta:'),
            'procedimentos': _('Selecione os procedimentos:'),
        }
        widgets = {
            'dataC': DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",
                    "locale": "pt-br",
                }
            ),
            'horaC' : TimePickerInput(
                options = {
                    "locale": "pt-br",
                }
            ),
        }

    def set_user(self,request):
        self.user = request.user

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('dataC') 
        hora = cleaned_data.get('horaC')
        dentista = cleaned_data.get('dentistaCRO')
        user = self.user

        consulta = Consulta.objects.filter(dataC=data).filter(horaC=hora).filter(pacienteCPF=user)
        if consulta:
           raise forms.ValidationError(f'Já existe uma consulta marcada em {data}, as {hora} de {user}') 
        else:
            consulta1 = Consulta.objects.filter(dataC=data).filter(horaC=hora).filter(dentistaCRO=dentista.CRO)
            if consulta1:
                raise  forms.ValidationError(f'Já existe uma consulta marcada em {data}, as {hora} com {dentista}')
        
    def clean_dataC(self):
        dataC = self.cleaned_data.get('dataC')
        now = timezone.now().date()
        weekday = ( dataC.isoweekday() % 7 ) + 1

        if dataC < now:
            raise forms.ValidationError('Essa data já passou') 
        else:
            if weekday != 1 and weekday != 7:
                return dataC
            else:
                raise forms.ValidationError('Atendemos apenas de Segunda à Sexta')

    def clean_horaC(self):
        horaC = self.cleaned_data.get('horaC')
        lim_inf = time(8, 0)
        lim_sup = time(17, 0)

        if horaC >= lim_inf and horaC <= lim_sup:
            if (horaC == time(8, 0) or horaC == time(9, 0) or horaC == time(10, 0) or horaC == time(11, 0)
                or horaC == time(12, 0) or horaC == time(13, 0) or horaC == time(14, 0)
                or horaC == time(15, 0) or horaC == time(16, 0)or horaC == time(17, 0)): 
                    return horaC
            else:
                raise forms.ValidationError('As consultas começam as pontualmente as 00. Ex: 09:00hrs, 10:00hrs')  
        else:
            raise forms.ValidationError('Adendemos apenas das 08:00h as 17:00h')


class ConsultaEditForm(ConsultaCreateForm):

    class Meta:
        model = Consulta

        fields = (
            'dentistaCRO',
            'dataC',
            'horaC',
            'procedimentos'
        )
        labels = {
            'dentistaCRO': _('Selecione um Denitsta:'),
            'dataC': _('Data da Consulta:'),
            'horaC': _('Horário da Consulta:'),
            'procedimentos': _('Selecione os procedimentos:'),
        }
        widgets = {
            'dataC': DatePickerInput(
                 options={
                     "format": "DD/MM/YYYY",
                     "locale": "pt-br",
                 }
                
            ),

            'horaC' : TimePickerInput(
                options = {
                    "locale": "pt-br",
                }
            ),
        }

        def set_user(self,  request):
            self.user = request.user

        def clean(self):
            #cleaned_data = super().clean()
            id = self.cleaned_data.get('id')

            user = self.user

            consulta = Consulta.objects.filter(pk=id)
            c_user = user.consulta_set.filter(pk=id)

            if uc == consulta:
                pass
            else:
                raise forms.ValidationError('Erro')
                super()

            

