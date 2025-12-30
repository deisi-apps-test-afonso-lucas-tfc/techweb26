ano_atual=2026
MAX_SESSOES = 7

from django.shortcuts import render, redirect, get_object_or_404
from .models import SessaoEvento, Aluno, Inscricao, Tipo, Entidade, Orador, User, Inquerito
from .forms import InqueritoForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout
from allauth.socialaccount.models import SocialAccount

from django.core.mail import send_mail


def listar_sessoes(request):

    # superuser = None
    aluno = None
    context = {}
    context['tipos'] = Tipo.objects.all()
    context['entidades'] = Entidade.objects.filter(sessoes__ano=ano_atual).order_by('nome')
    context['sessoes_disponiveis'] = SessaoEvento.objects.filter(ano=ano_atual).order_by('titulo')

    if request.user.is_authenticated:
        email = request.user.email
        # superuser = User.objects.filter(email=email, is_superuser=True).first()

        user = request.user
        aluno = 1 if Aluno.objects.filter(user=request.user).exists() else 0
        orador = Orador.objects.filter(email=email).first() if Orador.objects.filter(email=request.user.email).exists() else 0
        
        if aluno == 1:
            aluno = Aluno.objects.get(user=user)
            sessoes_inscrito = Inscricao.objects.filter(aluno=aluno, ano=ano_atual)
            num_sessoes = sessoes_inscrito.count()

            inscritas_ids = sessoes_inscrito.values_list('sessao_id', flat=True)
            sessoes_disponiveis = SessaoEvento.objects.filter(ano=ano_atual).exclude(id__in=inscritas_ids).order_by('titulo')
            max_sessoes = MAX_SESSOES

            context['sessoes_inscrito'] = sessoes_inscrito
            context['sessoes_disponiveis'] = sessoes_disponiveis
            context['num_sessoes'] = num_sessoes
            context['max_sessoes'] = max_sessoes
            
        if orador:
            context['orador'] = orador
            context['sessoes_orador'] = SessaoEvento.objects.filter(oradores=orador, ano=ano_atual)
            context['sessoes_disponiveis'] = SessaoEvento.objects.filter(ano=ano_atual).exclude(oradores=orador).order_by('titulo')

    from datetime import date
    hoje = date.today()
    mostrar_registo = date(2026, 3, 9) <= hoje <= date(2026, 3, 14)
 
    context['mostrar_registo'] =  mostrar_registo

    return render(request, 'tecweb/lista_sessoes.html', context)



def fotos_view(request):

    context = {}
    context['sessoes'] = SessaoEvento.objects.filter(ano=ano_atual).order_by('titulo')

    superuser=None
    if request.user.is_authenticated:
        email = request.user.email
        superuser = User.objects.filter(email=email, is_superuser=True).first()
   
    context['superuser'] = superuser

    return render(request, 'tecweb/fotos.html', context)


def oradores_view(request):
    
    oradores = Orador.objects.filter(sessoes__ano=ano_atual).distinct().order_by('nome')
    context = {}

    lista = []
    
    
    for orador in oradores:
        sessoes = (
            SessaoEvento.objects
            .filter(oradores=orador, ano=ano_atual)
            .distinct()
            .order_by('titulo') 
        )
    
        lista.append({
            'orador': orador,
            'sessoes': sessoes,
        })

    context['oradores'] = lista

    superuser=None
    if request.user.is_authenticated:
        email = request.user.email
        superuser = User.objects.filter(email=email, is_superuser=True).first()
   
    context['superuser'] = superuser

    return render(request, 'tecweb/oradores.html', context)


from django.db.models import Prefetch

def empresas_view(request):

    context = {}
    

    entidades = Entidade.objects.filter(sessoes__ano=ano_atual).distinct().order_by('nome')

    lista = []
    
    for entidade in entidades:
        sessoes = (
            SessaoEvento.objects
            .filter(entidades=entidade, ano=ano_atual)
            .distinct()
            .order_by('titulo') 
        )
    
        oradores = (
            Orador.objects
            .filter(sessoes__entidades=entidade, sessoes__ano=ano_atual)
            .distinct()
            .order_by('nome')
        )
    
        lista.append({
            'entidade': entidade,
            'sessoes': list(sessoes),
            'oradores': list(oradores)     
        })

    context['entidades'] = lista

    superuser=None
    if request.user.is_authenticated:
        email = request.user.email
        superuser = User.objects.filter(email=email, is_superuser=True).first()
   
    context['superuser'] = superuser

    return render(request, 'tecweb/empresas.html', context)


def inscrever_sessao(request, sessao_id):
    if request.user.is_authenticated is False:
        return redirect('tecweb:login')

    sessao = get_object_or_404(SessaoEvento, id=sessao_id)

    user = request.user
    aluno = 1 if Aluno.objects.filter(user=request.user).exists() else 0
    if aluno == 1:
        aluno = Aluno.objects.get(user=user)
        if Inscricao.objects.filter(aluno=aluno, sessao=sessao).exists():
            messages.warning(request, "Voce ja esta inscrito nesta sessao.")
            return redirect('tecweb:calendario')

        sessao_atividades = Inscricao.objects.filter(aluno=aluno)

        for inscricao in sessao_atividades:
            horarios_inscricao = inscricao.sessao.horarios.filter(ano=ano_atual)

            for horario in horarios_inscricao:
                if horario.inicio < sessao.horarios.first().fim and horario.fim > sessao.horarios.first().inicio:
                    messages.warning(request, "Ja esta inscrito num evento com o mesmo horario.")
                    return redirect('tecweb:calendario')
    else:
        return redirect('tecweb:register')

    if sessao.vagas_disponiveis > 0:
        Inscricao.objects.create(aluno=aluno, sessao=sessao, ano=ano_atual)
        messages.success(request, f"Voce foi inscrito com sucesso na sessao: {sessao.titulo}")
        return redirect('tecweb:sessoes')
    else:
        messages.warning(request, "Nao ha vagas disponiveis para esta sessao.")
        return redirect('tecweb:calendario')

def desinscrever_sessao(request, sessao_id):
    if request.user.is_authenticated is False:
        return redirect('tecweb:login')

    sessao = get_object_or_404(SessaoEvento, id=sessao_id)

    user = request.user
    aluno = 1 if Aluno.objects.filter(user=request.user).exists() else 0
    if aluno == 1:
        aluno = Aluno.objects.get(user=user)
        inscricao = Inscricao.objects.filter(aluno=aluno, sessao=sessao).first()
    else:
        return redirect('tecweb:register')

    if inscricao:
        inscricao.delete()
        messages.success(request, f"Voce foi desinscrito da sessao: {sessao.titulo}")
    else:
        messages.warning(request, "Voce nao esta inscrito nesta sessao.")

    return redirect('tecweb:sessoes')

def perfil(request):
    if request.user.is_authenticated:
        email = request.user.email
        superuser = User.objects.filter(email=email, is_superuser=True).first()

        user = request.user
        aluno = 1 if Aluno.objects.filter(user=request.user).exists() else 0
        if aluno == 1:
            aluno = Aluno.objects.get(user=user)
            inscricoes = Inscricao.objects.filter(aluno=aluno, ano=ano_atual)
        else:
            return redirect('tecweb:register')

        social_account = SocialAccount.objects.filter(user=user).first()
        if social_account:
            profile_picture_url = social_account.extra_data.get("picture")

        num_sessoes = inscricoes.count()
        max_sessoes = MAX_SESSOES

        return render(request, 'tecweb/perfil.html', {
            'numero_aluno': aluno.numero_aluno,
            'inscricoes': inscricoes,
            'num_sessoes': num_sessoes,
            'max_sessoes': max_sessoes,
            'profile_picture_url': profile_picture_url,
            'tipos': Tipo.objects.all(),
            'entidades':Entidade.objects.filter(sessoes__ano=ano_atual).order_by('nome'),
        })

    return redirect('tecweb:login')

def perfil_sessoes(request):
    eventos = []

    aluno = None
    user = None
    if request.user.is_authenticated:
        user = request.user
        aluno = 1 if Aluno.objects.filter(user=request.user).exists() else 0
        if aluno == 1:
            aluno = Aluno.objects.get(user=user)
        else:
            return redirect('tecweb:register')

    sessoes = aluno.inscricoes.filter(ano=ano_atual).prefetch_related('horarios')

    for sessao in sessoes:
        for horario in sessao.horarios.all():
            eventos.append({
                'title': sessao.titulo_curto,
                'start': horario.inicio.isoformat(),
                'end': horario.fim.isoformat(),
                'url': reverse('tecweb:detalhe_sessao', args=[sessao.id]),
                'backgroundColor': sessao.tipo.backgroundColor,
                'borderColor': sessao.tipo.borderColor,
                'vagas_disponiveis': sessao.vagas_disponiveis,
                'alunos_inscritos': sessao.alunos_inscritos.count(),
            })

    return JsonResponse(eventos, safe=False)

def detalhe_sessao(request, id):
    sessao = get_object_or_404(SessaoEvento, id=id)
    user = None
    aluno = None
    superuser=None
    inscricao_id=None
    orador_autenticado = False
    email = ""
    
    if request.user.is_authenticated:
        email = request.user.email
        superuser = User.objects.filter(email=email, is_superuser=True).first()

        user = request.user
        aluno = 1 if Aluno.objects.filter(user=request.user).exists() else 0
        if aluno == 1:
            aluno = Aluno.objects.get(user=user)
            inscricao = Inscricao.objects.filter(aluno=aluno, sessao=sessao).first()
            inscricao_id = inscricao.id if inscricao else None
        else:
            pass # return redirect('tecweb:register')
       
    n_inqueritos = Inquerito.objects.filter(inscricao__sessao=sessao).count()
    orador_autenticado = sessao.oradores.filter(email=email).exists()
    
    
    feedbacks_numericos = {
    "Interesse da temática abordada": '-' if not n_inqueritos else round(sum(i.interesse for i in Inquerito.objects.filter(inscricao__sessao=sessao)) / n_inqueritos, 1),
    "Qualidade dos conteúdos apresentados": '-' if not n_inqueritos else round(sum(i.qualidade for i in Inquerito.objects.filter(inscricao__sessao=sessao)) / n_inqueritos, 1),
    "Relevância para o curso que frequenta": '-' if not n_inqueritos else round(sum(i.relevancia for i in Inquerito.objects.filter(inscricao__sessao=sessao)) / n_inqueritos, 1),
    "Qualidade Técnica do Formador/Orador": '-' if not n_inqueritos else round(sum(i.formador for i in Inquerito.objects.filter(inscricao__sessao=sessao)) / n_inqueritos, 1),
    "Qualidade da apresentação de conteúdos/exposição das ideias do formador/orador": '-' if not n_inqueritos else round(sum(i.conteudos for i in Inquerito.objects.filter(inscricao__sessao=sessao)) / n_inqueritos, 1),
    "Satisfação geral sobre a sessão": '-' if not n_inqueritos else round(sum(i.satisfacao for i in Inquerito.objects.filter(inscricao__sessao=sessao)) / n_inqueritos, 1),
}

    
    feedbacks_respostas = {
        "Quais os pontos mais positivos da sessão a que assistiu?": [i.pontos_positivos for i in Inquerito.objects.filter(inscricao__sessao=sessao)],
        "Sugestões de melhoria para a sessão a que acabou de assistir.": [i.sugestoes_melhoria for i in Inquerito.objects.filter(inscricao__sessao=sessao)],
    } 
    
    
    context = {
        'sessao': sessao, 
        'orador_autenticado': orador_autenticado,
        'aluno': aluno, 
        'inscricao_id':inscricao_id, 
        'entidades':Entidade.objects.filter(sessoes__ano=ano_atual).order_by('nome'), 
        'superuser': superuser,
        'inscritos': Inscricao.objects.filter(sessao=sessao).count(),
        'inqueritos': n_inqueritos,
        'feedbacks_numericos': feedbacks_numericos,     
        'feedbacks_respostas': feedbacks_respostas,
    }

    return render(request, 'tecweb/detalhe_sessao.html', context)


def calendario_sessoes(request):
    eventos = []
    sessoes = SessaoEvento.objects.filter(ano=ano_atual).prefetch_related('horarios')

    aluno = None
    user = None
    if request.user.is_authenticated:
        user = request.user
        aluno = 1 if Aluno.objects.filter(user=request.user).exists() else 0
        if aluno == 1:
            aluno = Aluno.objects.get(user=user)

    for sessao in sessoes:
        inscrito = 0
        if aluno:
            inscrito = 1 if aluno and aluno.inscricoes.filter(id=sessao.id).exists() else 0

        for horario in sessao.horarios.all():
            eventos.append({
                'title': sessao.titulo_curto,
                'start': horario.inicio.isoformat(),
                'end': horario.fim.isoformat(),
                'url': reverse('tecweb:detalhe_sessao', args=[sessao.id]),
                'backgroundColor': sessao.tipo.backgroundColor,
                'inscrito': inscrito,
                'borderColor': sessao.tipo.borderColor,
                'classNames': ['naoInscrito'] if not inscrito else '',
                'vagas_totais': sessao.vagas_totais,
                'alunos_inscritos': sessao.alunos_inscritos.count(),
                'sala': sessao.sala if sessao.sala else ''
            })

    return JsonResponse(eventos, safe=False)


def calendario(request):
    num_sessoes = 0
    aluno = None
    user = None
    superuser=None
    if request.user.is_authenticated:
        email = request.user.email
        superuser = User.objects.filter(email=email, is_superuser=True).first()
        
        if superuser:
            return render(request, 'tecweb/calendario.html', {'num_sessoes':num_sessoes, 'tipos': Tipo.objects.all(), 'entidades':Entidade.objects.filter(sessoes__ano=ano_atual).order_by('nome'), 'superuser': superuser,})
        
        user = request.user
        aluno = 1 if Aluno.objects.filter(user=request.user).exists() else 0
        if aluno == 1:
            aluno = Aluno.objects.get(user=user)
            num_sessoes = Inscricao.objects.filter(aluno=aluno).count()
        
        elif not Orador.objects.filter(email=request.user.email).exists():
            return redirect('tecweb:register')
            
    return render(request, 'tecweb/calendario.html', {'num_sessoes':num_sessoes, 'tipos': Tipo.objects.all(), 'entidades':Entidade.objects.filter(sessoes__ano=ano_atual).order_by('nome'), 'superuser': superuser,})


def about(request):
    superuser=None
    if request.user.is_authenticated:
        email = request.user.email
        superuser = User.objects.filter(email=email, is_superuser=True).first()
        
    from .indicadores import indicadores
    context = indicadores(ano_atual)
    context['entidades'] = Entidade.objects.filter(sessoes__ano=ano_atual).order_by('nome')
    context['superuser'] = superuser
    
    return render(request, "tecweb/about.html", context)

def login_view(request):
    if 'numero_aluno' in request.session or request.user.is_authenticated:
        return redirect('tecweb:sessoes')
    return render(request, 'tecweb/login.html', {'entidades':Entidade.objects.filter(sessoes__ano=ano_atual).order_by('nome')})

def register_view(request):
    if request.user.is_authenticated:
        orador = 1 if Orador.objects.filter(email=request.user.email).exists() else 0
        
        ## Novos utilizadores com SuperUser n�o precisam de registo porque n�o s�o alunos
        superuser = User.objects.filter(email=request.user.email, is_superuser=True).first()

        if superuser:
            return redirect('tecweb:sessoes')
        ##

        if orador == 1:
            return redirect('tecweb:sessoes')

        aluno = 1 if Aluno.objects.filter(user=request.user).exists() else 0
        if aluno == 1:
            return redirect('tecweb:sessoes')
    else:
        return redirect('tecweb:login')

    if request.method == "POST":
        numero_aluno = request.POST.get('numero_aluno')
        nome_completo = request.POST.get('nome_completo')
        telemovel = request.POST.get('telemovel')
        curso = request.POST.get('curso')
        ano_curricular = request.POST.get('ano')

        if not numero_aluno.startswith('a'):
            return render(request, 'tecweb/register.html', {
                'erro': 'Numero de aluno tem de comecar com "a".'
            })

        if len(numero_aluno) != 9:
            return render(request, 'tecweb/register.html', {
                'erro': 'Numero de aluno invalido.'
            })

        numero = int(numero_aluno[1:])
        if not (21000000 <= numero <= 22799999):
            return render(request, 'tecweb/register.html', {
                'erro': 'Numero de aluno invalido.'
            })

        if Aluno.objects.filter(numero_aluno=numero_aluno).exists():
            return render(request, 'tecweb/register.html', {
                'erro': 'Este numero de aluno ja esta registado.'
            })

        aluno = Aluno.objects.create(
            numero_aluno=numero_aluno,
            nome_completo=nome_completo,
            telemovel=telemovel,
            curso=curso,
            ano_curricular=ano_curricular,
            user=request.user
        )

        return redirect('tecweb:sessoes')

    return render(request, 'tecweb/register.html')

def logout_view(request):
    request.session.flush()

    if request.user.is_authenticated:
        logout(request)

    return redirect('tecweb:login')

def autenticar(request):
    if request.user.is_authenticated:

        email = request.user.email
        orador = Orador.objects.filter(email=email).exists()

        if orador:
            return redirect('tecweb:sessoes')

        aluno = 1 if Aluno.objects.filter(user=request.user).exists() else 0
        if aluno == 1:
            return redirect('tecweb:sessoes')
        else:
            return redirect('tecweb:register')
    return redirect('tecweb:login')

def alunos_por_sessao(request):
    superuser=None
    if request.user.is_authenticated:
        email = request.user.email
        superuser = User.objects.filter(email=email, is_superuser=True).first()

        if not superuser:
            return redirect('tecweb:register')

    sessoes = SessaoEvento.objects.filter(ano=ano_atual)
    sessoes_com_inscritos = [
        {
            'sessao': sessao,
            'inscritos': Inscricao.objects.filter(sessao=sessao).select_related('aluno__user')
        }
        for sessao in sessoes
    ]

    return render(request, 'tecweb/alunos_por_sessao.html', {'sessoes_com_inscritos': sessoes_com_inscritos, 'superuser': superuser,})

def sessao_inscritos(request, sessao_id):
    superuser=None
    if request.user.is_authenticated:
        email = request.user.email
        orador = Orador.objects.filter(email=email).first()

        superuser = User.objects.filter(email=email, is_superuser=True).first()

        if not superuser and not orador:
            return redirect('tecweb:register')

    sessao = get_object_or_404(SessaoEvento, id=sessao_id)
    inscritos = Inscricao.objects.filter(sessao=sessao).select_related('aluno__user')

    return render(request, 'tecweb/sessao_inscritos.html', {'inscritos': inscritos, 'sessao': sessao, 'superuser': superuser,})



def exportar_inscritos(request, sessao_id):
    if request.user.is_authenticated:
        email = request.user.email
        orador = Orador.objects.filter(email=email).first()

        superuser = User.objects.filter(email=email, is_superuser=True).first()

        if not superuser and not orador:
            return redirect('tecweb:register')

    sessao = SessaoEvento.objects.get(id=sessao_id)
    inscritos = Inscricao.objects.filter(sessao=sessao).select_related('aluno__user')

    data = [
        {
            "Nome": inscricao.aluno.user.get_full_name(),
            "Numero de Aluno": inscricao.aluno.numero_aluno,
            "Curso": inscricao.aluno.get_curso_display(),
            "Ano Curricular": inscricao.aluno.get_ano_curricular_display(),
            "Email": inscricao.aluno.user.email,
        }
        for inscricao in inscritos
    ]

    content = "Nome;Numero;Curso;Ano;Email\n"
    content += "\n".join(
        [f'"{d["Nome"]}";{d["Numero de Aluno"]};{d["Curso"]};{d["Ano Curricular"][0]};{d["Email"]}' for d in data]
    )

    response = HttpResponse(content, content_type="text/csv; charset=utf-8")
    response['Content-Disposition'] = f'attachment; filename="inscritos_{sessao.titulo_curto}.csv"'

    response.charset = 'utf-8'
    return response



def exportar_inscritos_horas(request):
    if not request.user.is_authenticated:
        return redirect('tecweb:register')
    
    email = request.user.email
    superuser = User.objects.filter(email=email, is_superuser=True).first()

    if not superuser:
        return redirect('tecweb:register')

    dados = []
    for aluno in Aluno.objects.filter(inscricoes__ano=ano_atual).distinct().order_by('nome_completo'):
        sessoes = []
        duracao = 0
        for sessao in aluno.inscricoes.filter(ano=ano_atual):
            sessoes.append(sessao.titulo_curto)
            
            for horario in sessao.horarios.all():
                if horario.fim and horario.inicio:
                    duracao += (horario.fim - horario.inicio).total_seconds() / 3600   
                    

        dados.append({
                "Nome": aluno.user.get_full_name(),
                "Numero de Aluno": aluno.numero_aluno,
                "Curso": aluno.get_curso_display(),
                "Ano Curricular": aluno.get_ano_curricular_display(),
                "Email": aluno.user.email,
                "Horas inscritas": duracao,
                "Id Sessões": ','.join(sessoes),
        })

    content = "Nome;Numero;Curso;Ano;Email;Horas;Sessoes\n"
    content += "\n".join(
        [f'"{d["Nome"]}";{d["Numero de Aluno"]};{d["Curso"]};{d["Ano Curricular"][0]};{d["Email"]};{d["Horas inscritas"]};{d["Id Sessões"]}' for d in dados]
    )

    response = HttpResponse(content, content_type="text/csv; charset=utf-8")
    response['Content-Disposition'] = f'attachment; filename="inscritos_TecWeb.csv"'

    response.charset = 'utf-8'
    return response

from datetime import date

def sessoes_orador(request):
    if request.user.is_authenticated:
        email = request.user.email
        orador = Orador.objects.filter(email=email).first()

        if not orador:
            return redirect('tecweb:register')

        sessoes = SessaoEvento.objects.filter(oradores=orador, ano=ano_atual)

        hoje = date.today()

        mostrar_registo = date(2026, 3, 9) <= hoje <= date(2026, 3, 14)

        context = {
            'sessoes_disponiveis': sessoes,
            'orador': orador,
            'sessoes': SessaoEvento.objects.filter(ano=ano_atual).order_by('titulo'),
            'tipos': Tipo.objects.all(),
            'entidades': Entidade.objects.filter(sessoes__ano=ano_atual).order_by('nome'),
            'mostrar_registo': mostrar_registo,
        }

        return render(request, 'tecweb/lista_sessoes.html', context)
    else:
        return redirect('tecweb:login')


def inquerito_view(request, inscricao_id):
    try:
        inscricao = Inscricao.objects.get(id=inscricao_id)
    except Inscricao.DoesNotExist:
        return redirect('tecweb:sessoes')

    inquerito, created = Inquerito.objects.get_or_create(inscricao=inscricao)

    if request.method == "POST":
        form = InqueritoForm(request.POST, instance=inquerito)
        if form.is_valid():
            inquerito.save()
            return redirect('tecweb:sessoes')
    else:
        form = InqueritoForm(instance=inquerito)  

    return render(request, "tecweb/inquerito_form.html", {"form": form, "inscricao": inscricao})



import secrets

def generate_token():
    return secrets.token_urlsafe(32)

def login_orador(request):
    
    email = request.POST.get('email')

    if Orador.objects.filter(email=email).exists():
        
        orador = Orador.objects.get(email=email)
        orador.token = generate_token()
        orador.save()
          
        send_mail(
            subject='TecWeb: Autenticação', 
            message=f'Caro {orador.nome}, clique no link https://tecweb26.pw.deisi.ulusofona.pt/autentica-orador/?email={orador.email}&token={orador.token} para entrar na aplicação da TecWeb.</p><p>Este é um email automático, não responda.', 
            html_message=f'<p>Caro {orador.nome},</p><p>clique no <a href="https://tecweb26.pw.deisi.ulusofona.pt/autentica-orador/?email={orador.email}&token={orador.token}">link</a> para entrar na aplicação da TecWeb.</p><p>Este é um email automático, não responda.</p>',
            from_email='deisi.ulusofona@gmail.com',
            recipient_list=[email]
        )
        return render(
            request, 
            'tecweb/email-enviado.html', 
            {
                'entidades':Entidade.objects.filter(sessoes__ano=ano_atual).order_by('nome'), 
                'email': email,
            }
        )
        
    else:
        
        return render(
            request, 
            'tecweb/login.html', 
            {
                'entidades':Entidade.objects.filter(sessoes__ano=ano_atual).order_by('nome'), 
                'erro_orador': 'Email não encontrado na base de dados de Oradores.'
            }
        )


from django.contrib.auth import login

def autentica_orador(request):
    email = request.GET.get('email')
    token = request.GET.get('token')

    if not email or not token:
        return HttpResponse("Parâmetros inválidos.")

    try:
        orador = Orador.objects.get(email=email, token=token)
        
        user = orador.user  
        user.backend = 'django.contrib.auth.backends.ModelBackend'  # ou o backend correto
        login(request, user)
        
        request.session['orador_id'] = orador.id
        return redirect('tecweb:sessoes')
    
    except Orador.DoesNotExist:
        return render(
            request, 
            'tecweb/login.html', 
            {
                'entidades':Entidade.objects.filter(sessoes__ano=ano_atual).order_by('nome'), 
                'erro_orador': 'Email encontrado, mas problema com o link.'
            }
        )
    
    