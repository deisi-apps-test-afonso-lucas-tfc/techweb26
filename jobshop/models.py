from django.db import models

# Create your models here.
from django.db import models

class Membro(models.Model):
    nome = models.CharField(max_length=100)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    foto = models.ImageField(upload_to='jobshop/fotos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Agenda(models.Model):
    foto = models.ImageField(upload_to='jobshop/fotos/', blank=True, null=True)
    data = models.DateField(null=True, blank=True)


class Parceiro(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    foto = models.ImageField(upload_to='jobshop/fotos/', blank=True, null=True)
    site = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nome