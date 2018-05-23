FROM python:3-alpine
MAINTAINER Jack King

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8888
VOLUME database.sqlite

CMD ['python', './start.py']