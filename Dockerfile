FROM python:3.14.0a4-alpine3.21
LABEL maintainer="xuzmonomi.com"

ENV PYTHONBUFFERED=1

COPY ./requirements.txt /tmp/requirments.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirments.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \ 
        app-user   

ENV PATH="/py/bin:$PATH"

USER app-user