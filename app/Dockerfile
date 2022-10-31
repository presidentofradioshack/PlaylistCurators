# syntax=docker/dockerfile:1

FROM python:3.8-slim

RUN useradd -r -s /bin/bash ethan

WORKDIR /app

RUN chown -R ethan:ethan /app
USER ethan

ENV FLASK_ENV=production
ENV FLASK_APP=app

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION

ENV AWS_ACCESS_KEY_ID ${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY ${AWS_SECRET_ACCESS_KEY}
ENV AWS_DEFAULT_REGION ${AWS_DEFAULT_REGION}

ADD ./requirements.txt ./requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt --user

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers=5"]