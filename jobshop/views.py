from django.shortcuts import render
from .models import Membro, Agenda, Parceiro

def index_view(request):
    agendas = Agenda.objects.all().order_by("data")
    parceiros = Parceiro.objects.all()
    return render(request, 'jobshop/index.html', {
            'agendas': agendas,
            'parceiros': parceiros,
        })

def team_view(request):
    membros = Membro.objects.all()
    return render(request, 'jobshop/team.html', {
            'membros': membros,
        })
