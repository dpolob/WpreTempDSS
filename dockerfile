# dockerfile for WpreRainDSS
#
FROM python:3.6.10-slim-buster

COPY . /WpreTempDSS

RUN apt-get update
#RUN apt-get install -y git
#RUN apt-get install -y vim

WORKDIR /WpreTempDSS

RUN pip3 install -r requeriments.txt
CMD python3 main.py
