FROM python:alpine

RUN mkdir /code

WORKDIR /code

COPY scaling/requirements.txt /code/

# install the requirements
RUN pip install  --upgrade pip
RUN pip install -r requirements.txt

# copy the source code in the /code folder of the container
COPY scaling/ /code
EXPOSE 80

ENTRYPOINT ["python","/code/app.py" ]

#CMD ["--help"]
