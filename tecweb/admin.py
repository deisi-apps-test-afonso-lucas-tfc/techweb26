from django.contrib import admin
from .models import SessaoEvento
from .models import Horario
from .models import Aluno
from .models import Inscricao
from .models import Orador
from .models import Tipo
from .models import Entidade, Inquerito, Fotografia, Ficheiro
from django import forms
from django.utils.html import format_html

class HorarioInline(admin.TabularInline):
    model = Horario
    extra = 1

class FotografiaInline(admin.TabularInline):
    model = Fotografia
    extra = 1  
    fields = ('foto', 'autor', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.foto:
            return format_html('<img src="{}" width="100" style="border-radius: 5px;" />', obj.foto.url)
        return "Sem imagem"

    preview.short_description = "Pré-visualização"

class FicheiroInline(admin.TabularInline):
    model = Ficheiro
    extra = 1
    fields = ('nome', 'ficheiro')
    

class SessaoEventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ano')
    ordering = ('-ano', 'titulo')
    search_fields = ('titulo',)
    filter_horizontal = ('oradores', 'entidades')  
    inlines = [HorarioInline, FotografiaInline, FicheiroInline]
    save_as = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            orador = request.user.orador
            return qs.filter(oradores=orador)
        except Orador.DoesNotExist:
            return qs.none()  # Users sem orador não veem nada

    
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('inicio', 'fim')
    ordering = ('inicio','fim')
    search_fields = ('inicio','fim')

class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'numero_aluno', 'curso')
    ordering = ('nome_completo', 'numero_aluno',)
    search_fields = ('numero_aluno', 'nome_completo', 'user__first_name', 'user__last_name')

class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('aluno__nome_completo','sessao','data_inscricao')
    ordering = ('aluno','sessao','data_inscricao')
    search_fields = ('sessao__id','aluno__numero_aluno', 'aluno__nome_completo','aluno__user__first_name', 'aluno__user__last_name')

class OradorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'entidade', 'linkedin', 'orcid', 'short_cv', 'foto')
    ordering = ('nome',)
    search_fields = ('nome', 'cienciaid')
    list_editable = ('email',)
    list_display_links = ('nome',)  # required so category isn't the link

    def short_cv(self, obj):
        return obj.cv[:20] + "..." if obj.cv and len(obj.cv) > 20 else obj.cv

    short_cv.short_description = "CV"


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Se o user pertence ao grupo 'orador', mostra apenas o Orador associado
        if request.user.groups.filter(name='orador').exists():
            return qs.filter(user=request.user)
        return qs  # Admins e outros grupos veem todos

    # Garante que o orador só pode alterar o seu próprio registro
    def has_change_permission(self, request, obj=None):
        if obj is not None and request.user.groups.filter(name='orador').exists():
            return obj.user == request.user
        return super().has_change_permission(request, obj)

    # Garante que o orador não pode deletar outros registros
    def has_delete_permission(self, request, obj=None):
        if obj is not None and request.user.groups.filter(name='orador').exists():
            return obj.user == request.user
        return super().has_delete_permission(request, obj)



class ColorPickerWidget(forms.TextInput):
    input_type = "color"

class TipoForm(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = "__all__"
        widgets = {
            "backgroundColor": ColorPickerWidget(),
            "borderColor": ColorPickerWidget(),
        }

@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    form = TipoForm
    list_display = ("nome", "color_preview", "backgroundColor", "borderColor")
    list_editable = ("backgroundColor", "borderColor")
    list_display_links = ("nome",)

    def color_preview(self, obj):
        return format_html(
            '<div style="width:30px; height:20px; background:{}; border: 3px solid {}; border-radius:4px;"></div>',
            obj.backgroundColor, obj.borderColor
        )

    color_preview.short_description = "Preview"


class EntidadeAdmin(admin.ModelAdmin):
    list_display = ("nome", "link_preview")
    search_fields = ("nome", "link")

    def link_preview(self, obj):
        if obj.link:
            return format_html(f'<a href="{obj.link}" target="_blank">{obj.link}</a>')
        return "-"

    link_preview.short_description = "Website"


admin.site.register(Entidade, EntidadeAdmin)

admin.site.register(SessaoEvento, SessaoEventoAdmin)
admin.site.register(Horario, HorarioAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Inscricao, InscricaoAdmin)
admin.site.register(Orador, OradorAdmin)



class InqueritoAdmin(admin.ModelAdmin):
    list_display = (
        'inscricao', 
        'interesse', 
        'qualidade', 
        'relevancia', 
        'formador', 
        'conteudos', 
        'satisfacao',
        'pontos_positivos',
        'sugestoes_melhoria',
    )
    search_fields = (
        'inscricao__aluno__numero_aluno',
        'inscricao__aluno__nome_completo',
        'inscricao__sessao__titulo'
    )
    ordering = ('inscricao__aluno__numero_aluno',)

admin.site.register(Inquerito, InqueritoAdmin)