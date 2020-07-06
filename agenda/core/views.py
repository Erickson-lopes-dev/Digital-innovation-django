from django.shortcuts import render, redirect
from core.models import Evento


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
