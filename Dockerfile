FROM alpine:edge

RUN apk update && apk add --no-cache \
    python3 \
    bash \
    py3-lxml && \
    python3 -m ensurepip

ADD ./tests/requirements.txt /tmp/requirements.txt

RUN pip3 install -qr /tmp/requirements.txt 

ADD . /src/
WORKDIR /src
