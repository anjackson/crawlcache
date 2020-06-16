FROM python:3.7-slim

WORKDIR /crawlcache

COPY requirements.txt .

RUN \
  pip install -r requirements.txt

COPY crawlcache.py .

CMD mitmdump -s crawlcache.py
