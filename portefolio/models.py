from django.db import models

class Membro(models.Model):
    CARGO_CHOICES = [
        ('Presidente', 'presidente'),
        ('Vice-Presidente', 'vice-presidente'),
        ('Secretário', 'secretário'),
        ('Tesoureiro', 'tesoureiro'),
        ('Colaborador', 'colaborador'),
        ('Voluntário', 'voluntário'),
        ('Developper', 'developper'),
        ('Equipa de Comunicação', 'comunicacao'),
        ('Organização de Eventos', 'eventos'),
        ('Team Manager - Comunicação', 'tm_comunicacao'),
        ('Team Manager - Eventos', 'tm_eventos'),
    ]

    ANO_CHOICES = [
        ('1º', '1º'),
        ('2º', '2º'),
        ('3º', '3º'),
    ]

    CURSO_CHOICES = [
        ('Licenciatura Engenharia Informática', 'LEI'),
        ('Licenciatura Informática de Gestão', 'LIG'),
        ('Licenciatura Engenhraria Informática, Redes e Telecomunicações', 'LEIRT'),
        ('Licenciatura Computação e Matemática Aplicada', 'LCMA'),
        ('Licenciatura Ciência de Dados', 'LCiD'),
    ]


    cargo = models.CharField(max_length=200, choices=CARGO_CHOICES)
    nome = models.CharField(max_length=100)
    ano = models.CharField(max_length=2, choices=ANO_CHOICES)
    curso = models.CharField(max_length=100, choices=CURSO_CHOICES)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    foto = models.ImageField(upload_to='portefolio/fotos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    foto = models.ImageField(upload_to='portefolio/fotos/', blank=True, null=True)
    data = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.titulo

class Clube(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    foto = models.ImageField(upload_to='portefolio/fotos/', blank=True, null=True)

    def __str__(self):
        return self.titulo