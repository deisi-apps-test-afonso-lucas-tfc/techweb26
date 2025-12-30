FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar código
COPY . .


# Base de dados inicial (template)
# ⚠️ Só é usada se não existir BD no volume
COPY initial_data/db.sqlite3 /initial_db.sqlite3

# Pasta onde o volume será montado
RUN mkdir -p /data

# Recolher ficheiros estáticos
RUN python manage.py collectstatic --noinput

# Tornar o entrypoint executável
RUN chmod +x /app/entrypoint.sh


# Expor porta
EXPOSE 3000


# Arranque controlado (verifica BD antes de iniciar)
CMD ["/app/entrypoint.sh"]