from tecweb.models import *
import os
from django.core.files import File 

print('nomes')

script_directory = os.path.dirname(os.path.abspath(__file__))
print(script_directory)
pdf_directory = os.path.join(script_directory,'pdfs')

for pdf in os.listdir(pdf_directory):
    pdf_path = os.path.join(pdf_directory, pdf)
    if os.path.isfile(pdf_path):
        try:
            info = pdf.split('_')
            aluno_id = int(info[-3])
            sessao_id = int(info[-2])
                
            aluno = Aluno.objects.get(id=aluno_id)
            sessao = SessaoEvento.objects.get(id=sessao_id)

            i = Inscricao.objects.get(aluno=aluno, sessao=sessao)

            with open(pdf_path, 'rb') as f:
                i.certificado.save(pdf, File(f), save=True)

        except:
            print("certifique-se q estao assinados os certtificados: error with file", pdf)