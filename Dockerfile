FROM python:3.11-slim-buster

# Install Java.
RUN apt-get update && apt-get install -q -y \
    curl \
    zip \
    openjdk-11-jdk \
    apt-transport-https \
    gnupg2 \
    ca-certificates

RUN apt-get update && \
    apt-get install -y xvfb gnupg wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
    wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /chromedriver

# make the chromedriver executable and move it to default selenium path.
RUN chmod +x /chromedriver/chromedriver
RUN mv /chromedriver/chromedriver /usr/bin/chromedriver


RUN curl -SsL https://downloads.gauge.org/stable | sh

# hadolint ignore=DL3013,SC1091,DL3059
RUN pip install --no-cache-dir --upgrade pip setuptools


WORKDIR /app/

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

# Install gauge plugins
RUN gauge install python && \
    gauge install screenshot

ENV PATH=$HOME/.gauge:$PATH
