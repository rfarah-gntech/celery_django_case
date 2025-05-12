#!/bin/bash

# Sai imediatamente se um comando falhar
set -e

echo "🗄️ Aguardando o banco de dados estar disponível..."
while ! nc -z db 5432; do
  sleep 1
done
echo "✅ Banco de dados disponível."

echo "🗃️ Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "🚀 Iniciando o servidor Django..."
exec python manage.py runserver 0.0.0.0:8000
