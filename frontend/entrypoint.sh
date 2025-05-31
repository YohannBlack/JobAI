#!/bin/sh
set -a  # exporte toutes les variables chargées depuis .env
if [ -f /app/.env ]; then
  . /app/.env
fi
exec streamlit run /app/live_jobs.py --server.port=8501 --server.address=0.0.0.0

