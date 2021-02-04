FROM node:latest as build-stage
WORKDIR /app
COPY /vue-connect-ui/package*.json ./
RUN npm install
COPY vue-connect-ui/ .
RUN npm run build

FROM alpine:3.12.0 as production-stage

ARG IMAGE_VERSION=latest
ARG IMAGE_TAGS
ARG IMAGE_LABELS
ARG IMAGE_DIGEST

ENV VC_VERSION=$IMAGE_VERSION
ENV VC_LABELS=$IMAGE_LABELS
ENV VC_TAGS=$IMAGE_TAGS
ENV VC_DIGEST=$IMAGE_DIGEST

RUN apk add --update --no-cache nginx python3 supervisor
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools pipenv

RUN mkdir -p /dist/html \
    mkdir -p /dist/python \
    mkdir -p /var/log/supervisord \
    mkdir -p /var/run/supervisord

RUN addgroup -S gunicorn && adduser gunicorn -S gunicorn -G gunicorn

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache nginx python3 supervisor && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools pipenv

COPY /vue-connect-api/ /dist/python
RUN cd /dist/python && pipenv install --system --deploy --ignore-pipfile

COPY --from=build-stage /app/dist /dist/html

COPY rootfs /

# ngix
EXPOSE 8080

# gunicorn
EXPOSE 8081
ENTRYPOINT ["/docker-entrypoint.sh"]
