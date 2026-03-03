#!/bin/sh
set -e

DB_PATH="/data/db.sqlite3"
BACKUP_JSON="/app/initial_data/backup.json"

echo "🚀 Starting Django container..."

# Garantir pasta /data
mkdir -p /data

# Aplicar migrações (cria tabelas se BD não existir)
echo "🛠 Applying migrations..."
python manage.py migrate --noinput

# Se a BD acabou de ser criada, carregar dados do backup.json
if [ ! -f "$DB_PATH.initialized" ]; then
  if [ -f "$BACKUP_JSON" ]; then
    echo "📦 Loading initial data from backup.json..."
    python manage.py loaddata "$BACKUP_JSON"
    touch "$DB_PATH.initialized"
    echo "✅ Initial data loaded successfully."
  else
    echo "⚠️  No backup.json found at $BACKUP_JSON. Skipping data load."
  fi
else
  echo "✅ Database already initialized. Skipping data load."
fi

# Garantir permissões
chmod 664 "$DB_PATH"

# Verificar pasta media
if [ -d "/app/media" ] && [ "$(ls -A /app/media)" ]; then
  echo "✅ Media folder found. Keeping existing media files."
else
  echo "⚠️  Media folder missing or empty!"
fi

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