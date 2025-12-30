import csv
from tecweb.models import *

with open('tecweb/certificados/lig.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    data = [row for row in reader]
n=1
for a in data:
    if Aluno.objects.filter(numero_aluno=a['Número']).exists():
        aluno = Aluno.objects.get(numero_aluno=a['Número'])
        aluno.nome_completo = a['Nome'] + ' ' + a['Apelido']
        aluno.save()
        print(aluno.nome_completo)
        n+=1
print(n)