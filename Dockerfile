# pull official base image
FROM python:3.11-alpine

# set work directory
# WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY . /code/

# install dependencies
RUN pip install --upgrade pip

COPY requirements.txt /code/

RUN pip install -r requirements.txt
