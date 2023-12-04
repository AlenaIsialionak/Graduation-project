FROM python:3.11.4-alpine

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

ADD requirements.txt /news_site/
WORKDIR /news_site

COPY requirements.txt .


RUN pip install -r requirements.txt

COPY . .

CMD ["python", "./manage.py", "runserver",  "0.0.0.0:8000"]