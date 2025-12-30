from django.shortcuts import render
from .models import Membro, Evento, Clube

def index_view(request):
    return render(request, 'portefolio/index.html')

def about_view(request):
    return render(request, 'portefolio/about.html')

def team_view(request):
    membros = Membro.objects.all()
    return render(request, 'portefolio/team.html', {
            'membros': membros,
        })

def eventos_view(request):
    eventos = Evento.objects.all().order_by("-data")
    return render(request, 'portefolio/lista_eventos.html', {
            'eventos': eventos,
        })

def clubes_view(request):
    clubes = Clube.objects.all()
    return render(request, 'portefolio/lista_clubes.html', {
            'clubes': clubes,
        })