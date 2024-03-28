# syntax=docker/dockerfile:1
FROM python:3.12

RUN pip install --no-cache-dir --upgrade pip pipenv

RUN apt-get update && apt-get upgrade -y && apt-get install -y git libxmlsec1-dev

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV="development"

WORKDIR /app
COPY . .
RUN pipenv install --dev --system --clear --deploy

CMD ["make", "run-dev"]

EXPOSE 5000
