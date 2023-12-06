FROM python:3.11-bullseye

ENV PYTHONUNBUFFERED 1

WORKDIR /news_site

COPY requirements.txt /news_site/
RUN pip install -r requirements.txt

COPY entrypoint.sh /news_site/entrypoint.sh
COPY . /news_site/

#CMD ["python", "manage.py", "migrate"]
ENTRYPOINT ["/news_site/entrypoint.sh"]


