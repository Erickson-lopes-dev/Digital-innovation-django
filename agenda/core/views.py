from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse


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

    # até 1 hora de atraso ele aparece
    data_atual = datetime.now() - timedelta(hours=1)
                                                              #__lt para menor
    evento = Evento.objects.filter(usuario=usuario, data_evento__gt=data_atual)
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)


# import redirect
# def index(request):
#     return redirect('/agenda/')


@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)

    return render(request, 'evento.html', dados)


@login_required(login_url='/login/')
def submit_evento(request):

    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        local = request.POST.get('local')
        usuario = request.user
        id_evento = request.POST.get('id_evento')

        # update or create
        if id_evento:
            # evento = Evento.objects.get(id=id_evento)
            # if evento.usuario == usuario:
            #     evento.titulo = titulo
            #     evento.data_evento = data_evento
            #     evento.descricao = descricao
            #     evento.local = local
            #     evento.save()

            Evento.objects.filter(id=id_evento).update(titulo=titulo,
                                                       data_evento=data_evento,
                                                       descricao=descricao,
                                                       local=local)

        else:
            Evento.objects.create(titulo=titulo,
                                  data_evento=data_evento,
                                  descricao=descricao,
                                  local=local,
                                  usuario=usuario)
    return redirect('/')


@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    # evitando que outro usuario delete o registro de outros
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()

    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')


@login_required(login_url='/login/')
def json_evento(request):
    usuario = request.user

    # até 1 hora de atraso ele aparece
    data_atual = datetime.now() - timedelta(hours=1)
    # __lt para menor
    evento = Evento.objects.filter(usuario=usuario, data_evento__gt=data_atual)
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)
