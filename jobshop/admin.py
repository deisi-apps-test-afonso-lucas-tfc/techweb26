from django.contrib import admin
from .models import Membro, Agenda, Parceiro

class MembroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'is_active')
    search_fields = ('nome', 'is_active')
    list_filter = ('nome', 'is_active')

class AgendaAdmin(admin.ModelAdmin):
    list_display = ('data', 'foto')
    search_fields = ('data', 'foto')
    list_filter = ('data', 'foto')

class ParceiroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome', 'descricao')
    list_filter = ('nome', 'descricao')

admin.site.register(Membro, MembroAdmin)
admin.site.register(Agenda, AgendaAdmin)
admin.site.register(Parceiro, ParceiroAdmin)