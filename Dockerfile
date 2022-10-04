# Code Executor

FROM python:3.10.5-alpine3.16

ADD main.py .

RUN apk add --update --no-cache py3-numpy py3-pandas py3-apache-arrow

ENV PYTHONPATH=/usr/lib/python3.10/site-packages

ENTRYPOINT [ "python3", "./main.py"]

