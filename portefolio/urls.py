from django.urls import path
from . import views

app_name = "portefolio"

urlpatterns = [
    path('', views.index_view, name='index'),
    path('about/', views.about_view, name='about'),
    path('team/', views.team_view, name='team'),
    path('activity/', views.eventos_view, name='eventos'),
    path('groups/', views.clubes_view, name='clubes'),
]
