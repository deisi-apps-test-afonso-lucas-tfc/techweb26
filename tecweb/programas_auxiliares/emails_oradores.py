from tecweb.models import *


with open("emails_oradores.txt", "w") as f:
    for a in Orador.objects.all():
        if a.email:        
            f.write(f"{a.email};")
