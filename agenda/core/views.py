from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_user(request):
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
             messages.error(request, "Usuario ou senha não incorretos")

    return redirect('/')


# só acessa se tiver login e redireciona se não for possível
@login_required(login_url='/login')
def lista_eventos(request):
    # procurando por id
    # evento = Evento.objects.get(id=1)

    # retornando lista com todos os registros
    # evento = Evento.objects.all()
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario)
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)

# import redirect
# def index(request):
#     return redirect('/agenda/')


@login_required(login_url='/login/')
def evento(request):
    return render(request, 'evento.html')
