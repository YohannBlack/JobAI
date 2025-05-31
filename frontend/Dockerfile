FROM python:3.12-slim

WORKDIR /app

# Installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app


COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exposer le port 8501
EXPOSE 8501

CMD ["streamlit", "run", "live_jobs.py", "--server.port=8501", "--server.address=0.0.0.0"]