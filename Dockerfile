FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar código
COPY . .

# Recolher ficheiros estáticos
RUN python manage.py collectstatic --noinput

# Tornar o entrypoint executável
RUN chmod +x /app/entrypoint.sh


# Expor porta
EXPOSE 3000


# Arranque controlado (verifica BD antes de iniciar)
CMD ["/app/entrypoint.sh"]