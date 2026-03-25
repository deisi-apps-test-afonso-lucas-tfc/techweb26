FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 1. Criar um utilizador para a app (boas práticas de segurança)
RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

# 2. Instalar dependências (como root ainda)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 3. COPIAR O CÓDIGO JÁ COM O DONO CERTO
# O segredo está no --chown
COPY --chown=appuser:appuser . .

# 4. Ajustar permissões do entrypoint
RUN chmod +x /app/entrypoint.sh

# 5. Mudar para o utilizador da app
# A partir daqui, nada corre como root
USER appuser

EXPOSE 3000

CMD ["/app/entrypoint.sh"]