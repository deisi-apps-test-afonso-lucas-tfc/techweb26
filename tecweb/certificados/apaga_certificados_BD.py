from tecweb.models import *

for i in Inscricao.objects.all():
    if i.certificado:
        i.certificado.delete(save=False)
        i.certificado=None
        i.save()