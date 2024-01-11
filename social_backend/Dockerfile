# pull official base image
FROM python:3.9.6-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Make working directory
RUN mkdir /social_backend
WORKDIR /social_backend

COPY requirements.txt /social_backend/


# RUN apt-get update && apt-get install -y postgresql-client

RUN /usr/local/bin/python -m pip install --upgrade pip 

RUN pip install -r requirements.txt


COPY . /social_backend/

# Expose django port
EXPOSE 8000
