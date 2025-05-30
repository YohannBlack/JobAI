FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install scrapy

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["scrapy", "crawl", "linkedin_scraper"]


