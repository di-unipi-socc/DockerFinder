# crawler image based on python
FROM python:alpine

RUN mkdir /code

WORKDIR /code

COPY pyFinder/requirements.txt /code/

# install the requirements
RUN pip install  --upgrade pip
RUN pip install -r requirements.txt

# copy the source code in the /code folder of the container
COPY pyFinder/ /code

ENTRYPOINT ["python","/code/entryCrawler.py" ]
CMD ["--help"]
