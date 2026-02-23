from tecweb.models import *
from datetime import timedelta

def indicadores(ano):
    vagas = []

    for s in SessaoEvento.objects.filter(ano=ano):
        d = timedelta()

        for h in s.horarios.all():
            d += h.fim-h.inicio

        
        
        vagas.append({
            'vagas': s.vagas_totais,
            'vagas_disponiveis': s.vagas_disponiveis,
            'duracao': int(d.total_seconds()/60/60),
        })

    #    print(eval(d.total_seconds()/60/60),'horas:',s.titulo)

    # print(vagas)

    info = {}
    
    horas_disponiveis = sum(i['duracao'] * i['vagas_disponiveis'] for i in vagas)
    info['horas_disponiveis'] = horas_disponiveis
    #print(f"Ainda existem {horas_disponiveis/h_aluno} vagas para alunos que facam {h_aluno} horas")

    horas_ocupadas = sum(i['duracao'] * (i['vagas'] - i['vagas_disponiveis']) for i in vagas)
    info['horas_ocupadas'] = horas_ocupadas

    #print(f"Existem {horas_ocupadas} horas ocupadas por alunos inscritos")

    horas_de_sessoes = sum(i['duracao'] for i in vagas)
    info['horas_de_sessoes'] = horas_de_sessoes
  #  print(f"Existem {horas_de_sessoes} horas de sessoes")

    tipos = {t.nome:0 for t in Tipo.objects.all()}
    
    for s in SessaoEvento.objects.filter(ano=ano):
        tipos[s.tipo.nome] += 1
    
    info['tipos'] = tipos

    num_sessoes = SessaoEvento.objects.filter(ano=ano).count()
    info['n_sessoes'] = num_sessoes
#    print(f"Existem {num_sessoes} sessoes:", tipos)

    oradores = Orador.objects.filter(sessoes__ano=ano).distinct().count()
    info['n_oradores'] = oradores
#    print(f"Existem {oradores} oradores")

    entidades = Entidade.objects.filter(sessoes__ano=ano).distinct().count()
    info['n_entidades'] = entidades
#    print(f"Existem {entidades} entidades")

    n_alunos = Aluno.objects.filter(inscricoes__ano=ano).distinct().count()
    info['n_alunos'] = n_alunos

    info['horas_por_aluno'] = 0 if n_alunos == 0 else round(horas_ocupadas / n_alunos)	
   
    return info
