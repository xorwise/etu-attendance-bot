FROM python:3.12-slim as bot
ENV TZ="Europe/Moscow"
RUN date

RUN apt-get update
RUN apt-get install --yes --quiet --no-install-recommends \
        unzip \
        gettext \
        fonts-liberation \
        libasound2 \
        libatk-bridge2.0-0 \
        libatk1.0-0 \
        libatspi2.0-0 \
        libcairo2 \
        libcups2 \
        libdbus-1-3 \
        libdrm2 \
        libgbm1 \
        libgdk-pixbuf2.0-0 \
        libglib2.0-0 \
        libgtk-3-0 \
        libnspr4 \
        libnss3 \
        libpango-1.0-0 \
        libx11-6 \
        libxcb1 \
        libxcomposite1 \
        libxdamage1 \
        libxext6 \
        libxfixes3 \
        libxkbcommon0 \
        libxrandr2 \
        libxshmfence1 \
        wget \
        xdg-utils \
        xvfb \
        && rm -rf /var/lib/apt/lists/*

RUN wget -O /tmp/chrome-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.105/linux64/chrome-linux64.zip
RUN unzip /tmp/chrome-linux64.zip -d /bin
RUN wget -O /tmp/chromedriver-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.105/linux64/chromedriver-linux64.zip
RUN unzip /tmp/chromedriver-linux64.zip -d /bin
RUN rm /tmp/chrome-linux64.zip
RUN rm /tmp/chromedriver-linux64.zip
WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . /app


CMD ["python3", "app/main.py"]
