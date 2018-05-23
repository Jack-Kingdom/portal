FROM python:3-alpine
MAINTAINER Jack King

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD python start.py