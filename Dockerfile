FROM python:3.11-slim

# Impedir que o Python gere ficheiros .pyc e garantir logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Instalar dependências como root (necessário para permissões de sistema)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 2. O PASSO CRUCIAL: Copiar o código definindo o utilizador 1000 como dono
# Isto evita o erro "Permission denied: '/app/debug.log'"
COPY --chown=1000:1000 . .

# 3. Garantir que o entrypoint tem permissão de execução
RUN chmod +x /app/entrypoint.sh

# 4. Forçar o container a correr com o utilizador 1000 (Segurança K8s)
USER 1000

# Porta 8000 (ajustada para coincidir com o teu Workflow do GitHub)
EXPOSE 8000

CMD ["/app/entrypoint.sh"]