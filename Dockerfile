FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN python -m venv /opt/venv

RUN apt-get update && apt-get install -y default-libmysqlclient-dev libssl-dev && apt install -y default-mysql-client
RUN apt-get update && apt-get install -y pkg-config


RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/
EXPOSE 8000
