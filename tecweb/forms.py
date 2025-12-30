from django import forms
from .models import Inquerito


ESCALA_QUALITATIVA = [
    (1, "Muito Negativa"),
    (2, "Algo Negativa"),
    (3, "Nem Negativa, nem Positiva"),
    (4, "Algo Positiva"),
    (5, "Muito Positiva"),
]

class InqueritoForm(forms.ModelForm):
    class Meta:
        model = Inquerito
        fields = [
            "consentimento",
            "interesse",
            "qualidade",
            "relevancia",
            "formador",
            "conteudos",
            "satisfacao",
            "pontos_positivos",
            "sugestoes_melhoria",
        ]
        widgets = {
            "consentimento": forms.CheckboxInput(),
            "interesse": forms.RadioSelect(choices=ESCALA_QUALITATIVA),
            "qualidade": forms.RadioSelect(choices=ESCALA_QUALITATIVA),
            "relevancia": forms.RadioSelect(choices=ESCALA_QUALITATIVA),
            "formador": forms.RadioSelect(choices=ESCALA_QUALITATIVA),
            "conteudos": forms.RadioSelect(choices=ESCALA_QUALITATIVA),
            "satisfacao": forms.RadioSelect(choices=ESCALA_QUALITATIVA),
            "pontos_positivos": forms.Textarea(attrs={"rows": 3, "placeholder": "Exemplo: O formador explicou de forma clara."}),
            "sugestoes_melhoria": forms.Textarea(attrs={"rows": 3, "placeholder": "Exemplo: Podia haver mais exemplos práticos."}),
        }



from django import forms
from .models import Horario, SessaoEvento, Orador

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = kwargs.pop('request', None)
        if request and request.user.groups.filter(name='orador').exists():
            try:
                orador = Orador.objects.get(user=request.user)
                self.fields['sessao'].queryset = SessaoEvento.objects.filter(oradores=orador)
            except Orador.DoesNotExist:
                self.fields['sessao'].queryset = SessaoEvento.objects.none()