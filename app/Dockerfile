FROM python:3.12-slim as bot
ENV TZ="Europe/Moscow"
RUN date

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . /app


CMD ["python3", "app/main.py"]
