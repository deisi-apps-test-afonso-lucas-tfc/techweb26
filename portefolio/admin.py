from django.contrib import admin
from .models import Membro, Evento, Clube

class MembroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo', 'ano', 'curso', 'is_active')
    search_fields = ('nome', 'cargo', 'curso')
    list_filter = ('cargo', 'is_active')

class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao')
    search_fields = ('titulo', 'descricao')
    list_filter = ('titulo', 'descricao')

class ClubeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao')
    search_fields = ('titulo', 'descricao')
    list_filter = ('titulo', 'descricao')

admin.site.register(Membro, MembroAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Clube, ClubeAdmin)