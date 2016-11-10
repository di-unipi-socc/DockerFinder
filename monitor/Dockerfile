FROM python:3.5-alpine

RUN mkdir /code

WORKDIR /code

COPY scaling/requirements.txt /code/

# install the requirements
RUN pip install  --upgrade pip
RUN pip install -r requirements.txt

# copy the source code in the /code folder of the container
COPY scaling/ /code

ENTRYPOINT ["python","/code/scaleScanner.py" ]

#CMD ["--help"]
