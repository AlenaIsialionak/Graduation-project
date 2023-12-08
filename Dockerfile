#FROM python:3.11-bullseye
#
#ENV PYTHONUNBUFFERED 1
#
#WORKDIR /app
#
##ADD requirements.txt
#
#COPY requirements.txt /news_site/
#RUN pip install -r requirements.txt
#RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*
#
#COPY . /news_site/
#EXPOSE 8000:8000
#
#CMD python manage.py runserver 0.0.0.0:8000

FROM python:3.11-bullseye
ENV PYTHONUNBUFFERED 1

WORKDIR /app

EXPOSE 8000:8000
RUN mkdir "src"

COPY ./news_app ./src/news_app
COPY ./news_site ./src/news_site
COPY ./manage.py ./src/manage.py
COPY ./requirements.txt ./requirements.txt
COPY ./entrypoint.sh ./entrypoint.sh

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


RUN chmod +x ./entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]
CMD ["python", "src/manage.py", "runserver",  "0.0.0.0:8000"]

