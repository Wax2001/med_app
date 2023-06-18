FROM python:3.10
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y gettext

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/