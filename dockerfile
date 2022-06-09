FROM python:3.10-alpine

WORKDIR /src

COPY ./src/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./src .

# we could use CMD for running a command on start up but for this we will not