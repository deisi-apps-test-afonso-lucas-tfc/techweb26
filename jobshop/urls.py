from django.urls import path
from . import views

app_name = "jobshop"

urlpatterns = [
    path('', views.index_view, name='index'),
    path('team/', views.team_view, name='team'),
]
