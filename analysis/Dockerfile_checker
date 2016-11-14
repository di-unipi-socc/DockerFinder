#scanner image
FROM python:alpine

RUN mkdir /code

WORKDIR /code

COPY  pyFinder/requirements.txt /code/
RUN pip install  --upgrade pip
RUN pip install -r requirements.txt

COPY pyFinder/ /code

ENTRYPOINT ["python","/code/entryChecker.py"]
CMD ["--help"]
