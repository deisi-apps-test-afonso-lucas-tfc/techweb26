# Utilizadores

* orador: OradorTecweb DEISI2025
* gestor: gestor DEISI2025

# comentei no menu fotografias! ativar no final

# nao esquecer de sempre remover do git o db.sqlite3

# Instruções

1. Criar DB ou obter cópia em:

https://drive.google.com/file/d/1YvqIKyMOTuPlMgosxf6-H0jJOUOwL-1a/view?usp=sharing

2. 

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

3. To Do: integrar presenças na app. 

- Gerar QrCode para cada sessao. 
- criar botao q ativa modal com QRCode
- com telefone, aluno é encaminhado a pagina para se autenticar com conta Google
- no dashboard aparece nome e foto dos autenticados
- eventualmente associar um numero que vai mudando (como Martim)



# django-empty

Este repositório serve como um template base para projetos Django, permitindo iniciar rapidamente um novo projeto com uma estrutura pré-configurada.

## Propósito

O `django-empty` foi criado para ser um ponto de partida para projetos Django. Pode clonar este repositório e importar o seu projeto Django existente, aproveitando a configuração inicial já preparada.

## Conteúdo

- **.github/workflows**: Contém os ficheiros de configuração para o pipeline CI/CD, que automatiza o build, push e deploy da imagem Docker.
- **.gitignore**: Define os ficheiros e pastas a serem ignorados pelo Git, como ficheiros temporários e ambientes virtuais.
- **Dockerfile**: Ficheiro de configuração para construir a imagem Docker da aplicação Django. Atenção que `project` deve corresponder ao nome da pasta onde está `settings.py`.
- **docker-compose.yml**: Configuração para orquestrar serviços com Docker Compose, útil para desenvolvimento local.
- **requirements.txt**: Lista as dependências Python necessárias para o projeto.

## Media/Static Files

Em settings.py:
```
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), 
]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles') 
```
