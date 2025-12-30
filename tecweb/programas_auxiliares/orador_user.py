from tecweb.models import *

n = 23
for o in Orador.objects.all():
  if not o.user:
    if o.email:
      user = User.objects.create_user(username=o.email.split('@')[0]+'_'+str(n), email=o.email, first_name=o.nome, password='1234')
    else:
      user = User.objects.create_user(username=o.nome.replace(' ','_')+'_'+str(n), email='', first_name=o.nome, password='1234')
  
    o.user = user
    o.save()