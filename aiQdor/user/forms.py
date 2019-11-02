#------------ Definição de Formulario ------------#
from django import forms 
#-------------------------------------------------#

#------------ Para Usar os Models ------------#
from user.models import Paciente
#---------------------------------------------#

#------------ Para Validação ------------#
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .validator import validar_cpf, validar_celular
from django.utils import timezone
#----------------------------------------#

#------------ Para configurar os fields ------------#
from django.forms import ModelForm, DateInput, TextInput, CharField
# Para trocar o nome do campo
from django.utils.translation import gettext_lazy as _
from bootstrap_datepicker_plus import DatePickerInput
#---------------------------------------------------#

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput)
    class Meta:
        model = Paciente
        #fields = "__all__"
        fields = ('nome', 'CPF', 'email', 'dataNascimento', 'endereco', 'celular')
        
        widgets = {
            'nome':TextInput(attrs={
                'placeholder': 'Nome completo'
            }),

            'CPF': TextInput(attrs={
                'placeholder': 'Utilize somente números',
                'data-mask': '000.000.000-00',
            }),

            'dataNascimento': DatePickerInput(options={
                    "format": "DD/MM/YYYY",
                    "locale": "pt-br",
            }),

            'celular': TextInput(attrs= {
                'placeholder': 'Utilize somente números',
                'data-mask': '+99 (99) 9 9999-9999',
            }),

            'endereco': TextInput(attrs = {
                'palceholder': 'Seu endereço'
            })
        }
        

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não são iguais")
        return password2
    
    def clean_CPF(self):
        cpf = self.cleaned_data.get('CPF')
        users = Paciente.objects.filter(CPF=cpf)
        if validar_cpf(cpf):
            if users:
                raise forms.ValidationError("Esse CPF ja está cadastrado no sistema")
            else:    
                return cpf
        else:
            raise forms.ValidationError("CPF Invalido")    

    def clean_dataNascimento(self):
        ano_atual = timezone.now().year
        data = self.cleaned_data.get('dataNascimento')
        if data.year < ano_atual:
            return data
        else:
            raise forms.ValidationError("Essa pessoa ainda nem nasceu")       
    
    def clean_celular(self):
        cel = self.cleaned_data.get('celular')
        if validar_celular(cel):
            return cel  
        else:
            raise forms.ValidationError("Esse número é invalido")        

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Paciente
        #filed = '__all__' 
        fields = ('nome', 'CPF','email', 'dataNascimento', 'endereco', 'celular', 'password' )
        
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class PacienteEditPerfil(forms.ModelForm):
    
    class Meta:
        model = Paciente
        fields = ('nome','email', 'CPF', 'celular', 'endereco', 'dataNascimento')
        widgets = {

            'dataNascimento': DatePickerInput(
                 options={
                     "format": "DD/MM/YYYY",
                     "locale": "pt-br",
                 }
            ),
        }

    def set_user(self, request):
        self.user = request.user    

    def clean_CPF(self):
        cpf = self.cleaned_data.get('CPF')
        users = Paciente.objects.filter(CPF=cpf)
        us = self.user
        
        if validar_cpf(cpf):
            if users:
                if users[0].email == us.email:
                    return cpf
                else:    
                    raise forms.ValidationError("Esse CPF ja está cadastrado no sistema")
            else:    
                return cpf
        else:
            raise forms.ValidationError("CPF Invalido")    

    def clean_dataNascimento(self):
        now = timezone.now().year
        data = self.cleaned_data.get('dataNascimento')
        data_ano = data.year
        if data_ano < now:
            return data
        else:
            raise forms.ValidationError("Essa pessoa ainda nem nasceu")

    def clean_celular(self):
        cel = self.cleaned_data.get('celular')
        if validar_celular(cel):
            return cel  
        else:
            raise forms.ValidationError("Esse número de celular é invalido!")