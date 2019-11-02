from django.shortcuts import render, redirect
from django.contrib import messages
from user.forms import UserCreationForm, PacienteEditPerfil
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            nome = form.cleaned_data.get('nome')
            email = form.cleaned_data.get('email')
            senha = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=senha)
            login(request, user)
            messages.success(request, f'Conta criada para {nome}!')
            return redirect('core-home')
        else:
            messages.error(request, f'Algo de errado não está certo!')
    else:
        form = UserCreationForm()

    context = {'form': form }
    return render(request, 'user/register.html', context)

@login_required
def perfil(request):
    return render(request, 'user/perfil.html')

@login_required
def perfil_edit(request):
    paciente_edit_form = PacienteEditPerfil(instance=request.user)

    if request.method == 'POST':
        paciente_edit_form = PacienteEditPerfil(request.POST, instance=request.user)

        paciente_edit_form.set_user(request)

        if paciente_edit_form.is_valid():
            paciente_edit_form.save()
            
            return redirect('perfil')
    else:
        paciente_edit_form = PacienteEditPerfil(instance=request.user)

    context = {
        'form': paciente_edit_form
    }
    return render(request, 'user/editar_perfil.html', context)
