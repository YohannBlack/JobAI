FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install scrapy

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Aentrypoint pour charger l'env et lancer Scrapy
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
