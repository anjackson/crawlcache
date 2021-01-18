FROM python:3.7-buster

WORKDIR /crawlcache

COPY requirements.txt .

RUN \
  pip install -r requirements.txt

COPY crawlcache.py .

CMD mitmdump --flow-detail 3 -v --ssl-insecure --mode upstream:http://warcprox:8000/ -s crawlcache.py

