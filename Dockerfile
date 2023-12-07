FROM python:3.11-bullseye

ENV PYTHONUNBUFFERED 1

WORKDIR /news_site

COPY requirements.txt /news_site/
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

COPY . /news_site/

CMD python manage.py runserver 0.0.0.0:8000


