# pull official base image
FROM python:3.11-slim-buster

# set environment variables
ENV POETRY_VERSION=1.5.1 \
    USER=smartfact \
    DIR=/usr/src/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=$DIR \
    PATH=/root/.poetry/bin:${PATH}

# set working directory
WORKDIR $DIR

# install system dependencies
RUN apt-get update \
    && apt-get -y install netcat g++ gcc libffi-dev make \
    && pip install --upgrade pip \
    && pip install "poetry==$POETRY_VERSION" \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ADD poetry.lock ./pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root \
    && poetry show

# add app
COPY . .

# add start.sh
COPY start.sh .
RUN chmod +x /usr/src/app/start.sh

# add and run as non-root user
RUN adduser --disabled-password $USER
USER $USER
