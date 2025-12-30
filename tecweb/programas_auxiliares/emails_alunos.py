from tecweb.models import *


with open("emails_alunos.txt", "w") as f:
    for a in Aluno.objects.all():
        f.write(f"{a.user.email};")
