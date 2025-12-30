from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import Group


class Tipo(models.Model):
    nome = models.CharField(max_length=200)
    backgroundColor = models.CharField(max_length=200)
    borderColor = models.CharField(max_length=200, default='', blank=True, null=True)

    def __str__(self):
        return f"{self.nome}"


class Entidade(models.Model):
    nome =  models.CharField(max_length=255, default='', null=True, blank=True)
    link = models.URLField(max_length=200, default='', null=True, blank=True)
    logotipo = models.ImageField(upload_to='tecweb/logos', null = True, blank = True)

    def __str__(self):
        return f"{self.nome}"


class Orador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    nome = models.CharField(max_length=200)
    linkedin = models.CharField(max_length=300, blank=True, null=True)
    orcid = models.CharField(max_length=300, default=None, blank=True, null=True)
    cv = models.TextField(null=True, blank=True)
    foto = models.ImageField(upload_to="tecweb/fotos", null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True, default=None)
    entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE, default=None, null=True, blank=True)
    token = models.CharField(max_length=64, blank=True, null=True)
    
    class Meta:
        ordering = ['nome']  # Definindo a ordenacao alfabetica por nome

    def __str__(self):
        return f"{self.nome}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # grava primeiro o Orador
        # Adiciona o User ao grupo 'orador'
        group, _ = Group.objects.get_or_create(name='orador')
        if not self.user.groups.filter(name='orador').exists():
            self.user.groups.add(group)
            self.user.is_staff = True  # para aceder a admin
            self.user.save()


from django.utils.timezone import now

class SessaoEvento(models.Model):
    ano = models.IntegerField()
    titulo = models.CharField(max_length=255, default='', null=True, blank=True)
    titulo_curto = models.CharField(max_length=255, default='', null=True, blank=True)
    entidades = models.ManyToManyField(Entidade, related_name="sessoes")
    foto_capa = models.ImageField(upload_to='tecweb/fotos', null = True, blank = True)
    sala = models.CharField(max_length=255, default='', null=True, blank=True)
    morada = models.TextField(default='', null=True, blank=True)
    oradores = models.ManyToManyField(Orador, related_name="sessoes", blank=True)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, null=True, blank=True, default=None)
    objetivo = models.TextField(default='', null=True, blank=True)
    prerequisitos = models.TextField(default='', blank=True)
    topicos = models.TextField(default='', null=True, blank=True)
    metodologia = models.TextField(default='', null=True, blank=True)
    resultados_esperados = models.TextField(default='', null=True, blank=True)
    duracao = models.TextField(default='', null=True, blank=True)
    ferramentas = models.TextField(default='', null=True, blank=True)
    recursos_necessarios = models.TextField(default='', null=True, blank=True)
    vagas_totais = models.IntegerField(default=20)  # Total de vagas da sessão
    inscricao_alargada = models.BooleanField()

    def oradores_ordenados(self):
        return self.oradores.order_by("nome")
    
    @property
    def terminou(self):
        return not self.horarios.filter(fim__gt=now()).exists()   
    
    def __str__(self):
        return self.titulo

    @property
    def vagas_disponiveis(self):
        inscritos_count = Inscricao.objects.filter(sessao=self).count()
        return self.vagas_totais - inscritos_count

    @property
    def inscritos(self):
        return Inscricao.objects.filter(sessao=self).count()


class Fotografia(models.Model):
    autor = models.CharField(max_length=255, default='', null=True, blank=True)
    foto = models.FileField(upload_to="tecweb/fotos/sessoes", null=True, blank=True)
    sessao = models.ForeignKey(SessaoEvento, on_delete=models.CASCADE, related_name='fotografias', null = True, blank=True)


    def __str__(self):
        return f"Foto {self.id} de {self.sessao}" 


class Ficheiro(models.Model):
    nome = models.CharField(max_length=255, default='', null=True, blank=True)
    ficheiro = models.FileField(upload_to="tecweb/ficheiros", null=True, blank=True)
    sessao = models.ForeignKey(SessaoEvento, on_delete=models.CASCADE, related_name='ficheiros', null = True, blank=True)

    def __str__(self):
        return self.nome if self.nome else self.ficheiro.name.split("/")[-1]


class Horario(models.Model):
    inicio = models.DateTimeField(default=None, null= True, blank=True)
    fim = models.DateTimeField(default=None, null= True, blank=True)
    sessao = models.ForeignKey(SessaoEvento, on_delete=models.CASCADE, related_name='horarios', null = True, blank=True)

    class Meta:
        ordering = ['inicio']

    def __str__(self):
        if self.fim :
            return self.inicio.strftime("%Y-%m-%d %H:%M") + ' - ' + self.fim.strftime("%Y-%m-%d %H:%M")
        else:
            return self.inicio.strftime("%Y-%m-%d %H:%M")


class Aluno(models.Model):
    ANOS_CURRICULARES = [
        (1, "1º Ano"),
        (2, "2º Ano"),
        (3, "3º Ano"),
    ]

    CURSOS = [
        ("LEI", "LEI"),
        ("LIG", "LIG"),
        ("LEIRT", "LEIRT"),
        ("LCD", "LCD"),
        ("LCMA", "LCMA"),
        ("MEISI", "MEISI"),
        ("DI", "DI"),
        ("Outro", "Outro"),
#         ("LEIA", "LEIA (IPLUSO)"),
#         ("LGC", "LGC (IPLUSO)"),
#         ("LGET", "LGET (IPLUSO)"),
#         ("LASI", "LASI (IPLUSO)"),
#         ("CTeSP-GSI", "CTeSP em Gestão de Sistemas de Informação"),
#         ("CTeSP-GNCE", "CTeSP em Gestão de Negócios e Comércio Eletrónico"),
#         ("CTeSP-DSIoT", "CTeSP em Desenvolvimento De Sistemas Para Internet Das Coisas"),
#         ("CTeSP-AICD", "CTeSP em Aplicações Informáticas para Ciências de Dados"),
     ]

    numero_aluno = models.CharField(max_length=9, unique=True)
    nome_completo = models.CharField(max_length=50, null=True, blank=True, default='') 
    telemovel = models.CharField(max_length=15, null=True, blank=True, default=None)
    curso = models.CharField(max_length=20, choices=CURSOS, null=True, blank=True, default=None)
    ano_curricular = models.IntegerField(choices=ANOS_CURRICULARES, null=True, blank=True, default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True, blank=True, default=None)
    inscricoes = models.ManyToManyField(SessaoEvento, related_name='alunos_inscritos', through='Inscricao', through_fields=('aluno', 'sessao'))

    def __str__(self):
        return f"{self.nome_completo} ({self.numero_aluno}, {self.get_curso_display()}, {self.ano_curricular}º)"


    
class Inscricao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, null= True, blank=True, default=None)
    sessao = models.ForeignKey(SessaoEvento, on_delete=models.CASCADE)
    ano = models.IntegerField()
    data_inscricao = models.DateTimeField(auto_now_add=True)
    certificado = models.FileField(upload_to="tecweb/certificados", default=None, null=True, blank=True)

    class Meta:
        unique_together = ('aluno', 'sessao')

    def __str__(self):
        if self.aluno:
            return f'{self.aluno.nome_completo} inscrito na sessão "{self.sessao.titulo}"'
        else:
            return f'inscrito na sessão "{self.sessao.titulo}"'


class Inquerito(models.Model):
    inscricao= models.OneToOneField(Inscricao, on_delete=models.CASCADE, null=True, blank=True, related_name="inquerito")
    consentimento = models.BooleanField(default=True, verbose_name="Consinto que as minhas respostas sejam utilizadas, de forma anonima, para gerar insights para a melhoria das sessões futuras da Tecweb")
    interesse = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Interesse da temática abordada")
    qualidade = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Qualidade dos conteúdos apresentados")
    relevancia = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Relevância para o curso que frequenta")
    formador = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Qualidade Técnica do Formador/Orador")
    conteudos = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Qualidade da apresentação de conteúdos/exposição das ideias do formador/orador")
    satisfacao = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Classifique na seguinte escala a sua satisfação geral sobre a sessão a que assistiu.")
    pontos_positivos = models.TextField(verbose_name="Quais os pontos mais positivos da sessão a que assistiu?")
    sugestoes_melhoria = models.TextField(verbose_name="Sugestões de melhoria para a sessão a que acabou de assistir.")
        
    def __str__(self):
        return f"Inquerito de {self.inscricao.aluno} da sessao '{self.inscricao.sessao.titulo}'"
    
    
