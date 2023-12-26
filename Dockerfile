# pull official base image
FROM python:3.10-slim

# set work directory
WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . .
