FROM python:3.7-alpine

COPY app.py /
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN mkdir /app

ENV AWS_REGION=us-east-1
ENV AWS_ACCESS_KEY_ID=
ENV AWS_SECRET_ACCESS_KEY=

ENV TEST=replaceme

WORKDIR /

ENTRYPOINT eval $(python /app.py) && env
