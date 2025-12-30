from tecweb.models import *

n = 23
for o in Orador.objects.all():
  o.user.username = o.nome.lower().replace(' ','_').replace('.','_')
  o.user.save()