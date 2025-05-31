#!/bin/sh
set -a  # exporte toutes les variables chargées depuis .env
if [ -f /app/.env ]; then
  . /app/.env
fi
exec scrapy crawl linkedin_scraper
