FROM python:alpine
LABEL version="1.0.3" maintainer="rskntroot@gmail.com"

RUN pip install --upgrade pip myst-parser pydata-sphinx-theme
RUN apk add --no-cache py3-sphinx make

WORKDIR /opt/sphinx

