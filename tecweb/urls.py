from django.urls import path
from . import views

app_name = "tecweb"

urlpatterns = [
    path('sessoes/', views.listar_sessoes, name='sessoes'),
    path('fotos/', views.fotos_view, name='fotos'),
    path('oradores/', views.oradores_view, name='oradores'),
    path('entidades/', views.empresas_view, name='empresas'),
    path('detalhe/<int:id>/', views.detalhe_sessao, name='detalhe_sessao'),
    path('calendario/', views.calendario, name='calendario'),
    path('calendario/sessoes/', views.calendario_sessoes, name='calendario_sessoes'),
    path('', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('registar/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('inscrever/<int:sessao_id>', views.inscrever_sessao, name='inscrever_sessao'),
    path('desinscrever_sessao/<int:sessao_id>/', views.desinscrever_sessao, name='desinscrever_sessao'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/sessoes/', views.perfil_sessoes, name='perfil_sessoes'),
    path('autenticar/', views.autenticar, name='autenticar'),

    path('login-orador/', views.login_orador, name='login-orador'),
    path('autentica-orador/', views.autentica_orador, name='autentica-orador'),

    path('ver/alunos-por-sessao/', views.alunos_por_sessao, name='alunos_por_sessao'),
    path('exportar-inscritos/<int:sessao_id>/', views.exportar_inscritos, name='exportar_inscritos'),
    path('exportar-inscritos-horas/', views.exportar_inscritos_horas, name='exportar_inscritos_horas'),
    path('ver/inscritos/<int:sessao_id>/', views.sessao_inscritos, name='sessao_inscritos'),
    path('sessoes/orador/', views.sessoes_orador, name='sessoes_orador'),
    path("inquerito/<int:inscricao_id>/", views.inquerito_view, name="inquerito"),
    # path('feedback-numerico/', views.feedback_numerico_view, name='feedback_numerico'),
]
