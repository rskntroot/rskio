FROM python:alpine
RUN pip install --upgrade pip
LABEL version="1.0.3" maintainer="rskntroot@gmail.com"

RUN apk add --no-cache \
  make \
  py3-sphinx
RUN pip install myst-parser pydata-sphinx-theme

WORKDIR /opt/sphinx

