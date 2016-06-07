FROM python:3.4-alpine

RUN mkdir /pyFinder
WORKDIR /pyFinder
ADD  requirements.txt /pyFinder/
RUN pip install  --upgrade pip
RUN pip install -r requirements.txt
ADD . /pyFinder/
ENTRYPOINT python ../pyFinder/src/pyDescriptor/mainDescriptor.py