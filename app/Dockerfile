FROM python:3.12-alpine

WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN export PATH=$PATH:/app
RUN pip install -r requirements.txt
COPY . .
