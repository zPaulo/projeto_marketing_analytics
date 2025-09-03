#!/bin/bash

# Aguardar PostgreSQL estar pronto
echo "Aguardando PostgreSQL..."
while ! pg_isready -h postgres_database -p 5432 -U ${POSTGRES_USER} -d ${POSTGRES_DB}; do
  echo "PostgreSQL não está pronto, aguardando..."
  sleep 2
done

echo "PostgreSQL está pronto!"

# Executar migrações
echo "Executando migrações..."
uv run alembic upgrade head

# Configurar cron job (ex: a cada 1 hora)
echo "Configurando cron job..."
echo "0 * * * * /app/scripts/run_job.sh" | crontab -

# Iniciar cron
cron

# Manter o container rodando
tail -f /dev/null