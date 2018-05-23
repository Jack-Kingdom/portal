FROM python:3-alpine
MAINTAINER Jack King

WORKDIR /usr/src/app

# install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy code to work folder
COPY . .

# set env
ENV LISTENING_ADDRESS='0.0.0.0'

# create user && switch
RUN groupadd -r portal && useradd --no-log-init -r -g portal portal
USER portal

# entry
CMD python start.py