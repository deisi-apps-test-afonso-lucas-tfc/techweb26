#!/bin/sh
set -e

DB_PATH="/data/db.sqlite3"
INITIAL_DB="/initial_db.sqlite3"

echo "🚀 Starting Django container..."

# Garantir pasta /data
mkdir -p /data

# Se não existir BD no volume, copiar a inicial
if [ ! -f "$DB_PATH" ]; then
  echo "📦 No production database found."
  echo "➡️  Initializing database from template..."
  cp "$INITIAL_DB" "$DB_PATH"
else
  echo "✅ Production database found. Keeping existing data."
fi


# Garantir permissões
chmod 664 "$DB_PATH"

# Verificar pasta media
if [ -d "/app/media" ] && [ "$(ls -A /app/media)" ]; then
  echo "✅ Media folder found. Keeping existing media files."
else
  echo "⚠️  Media folder missing or empty!"
fi

# Aplicar migrações (seguro mesmo com dados)
echo "🛠 Applying migrations..."
python manage.py migrate --noinput

# Collect static files to mounted volume
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Ativar cron job para envio de backup de BD
# echo "Registering cron jobs..."
# python manage.py crontab add || true

# Iniciar o cron em background
# service cron start &


# Iniciar servidor
echo "🌐 Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:3000 project.wsgi:application