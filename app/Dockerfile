FROM python:3.8.2-slim-buster
LABEL maintainer="criss1913@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

# setting up debian environment with all the dependencies
RUN set -ex \
    && buildDeps=" \
    build-essential \
    libpq-dev \
    " \
    && deps=" \
    gdal-bin \
    gettext \
    postgresql-client-11 \
    " \
    && apt-get update && apt-get install -y $buildDeps $deps --no-install-recommends \
    && pip install --no-cache-dir -r /requirements.txt \
    && apt-get purge -y --auto-remove $buildDeps \
    && rm -rf /var/lib/apt/lists/*

#setting up django work directory
RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN addgroup --system user && adduser --system --no-create-home --group user
RUN chown -R user:user /app && chmod -R 755 /app
USER user

EXPOSE 8000