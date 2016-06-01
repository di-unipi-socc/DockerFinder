FROM python:3.4-alpine

RUN mkdir /code
WORKDIR /code
ADD  requirements.txt /code/
RUN pip install  --upgrade pip
RUN pip install -r requirements.txt
ADD . /code/