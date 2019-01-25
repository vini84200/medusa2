FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /medusaii
WORKDIR /medusaii
# Installing OS Dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
libsqlite3-dev
RUN pip install -U pip setuptools
COPY requirements.txt /medusaii/
COPY requirements-dev.txt /medusaii/
RUN pip install -r /medusaii/requirements.txt
COPY . /medusaii/
# Django service
EXPOSE 8000