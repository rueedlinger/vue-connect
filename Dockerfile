FROM node:latest as build-stage
WORKDIR /app
COPY vue-connect-ui/package*.json ./
RUN npm install
COPY vue-connect-ui/ .
RUN npm run build

FROM alpine:3.12.0 as production-stage

ARG IMAGE_VERSION=dev
ARG IMAGE_TAGS=unknown
ARG IMAGE_BUILD_TIME=unknown
ARG IMAGE_GITHUB_SHA=unknown
ARG IMAGE_GITHUB_REPO=unknown

ENV TZ="UTC"
ENV LANG="C.UTF-8"

ENV VC_SQLITE_FILE_PATH="/dist/db/vue-connect.db"
ENV VC_CREATE_DB_IN_APP="false"
ENV VC_POLLING_INTERVAL_SEC="60"

ENV VC_VERSION=$IMAGE_VERSION
ENV VC_TAGS=$IMAGE_TAGS
ENV VC_IMAGE_BUILD_TIME=$IMAGE_BUILD_TIME
ENV VC_IMAGE_GITHUB_SHA=$IMAGE_GITHUB_SHA
ENV VC_IMAGE_GITHUB_REPO=$IMAGE_GITHUB_REPO

RUN mkdir -p /dist/html && \
    mkdir -p /dist/python && \
    mkdir -p /dist/db && \
    mkdir -p /dist/redis && \
    mkdir -p /var/log/supervisord && \
    mkdir -p /var/run/supervisord 


# used fixed UID and GID for gunicorn user
RUN addgroup gunicorn --gid 500 && \ 
    adduser gunicorn --uid 500 -S -G gunicorn && \
    chown -R gunicorn:gunicorn /dist/db


ENV PYTHONUNBUFFERED=1
RUN apk add --no-cache nginx redis python3 supervisor sqlite tzdata && \
    ln -sf python3 /usr/bin/python && \
    python3 -m ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools pipenv

COPY vue-connect-api/ /dist/python
RUN cd /dist/python && pipenv install --system --deploy --ignore-pipfile

COPY --from=build-stage /app/dist /dist/html

COPY rootfs /

# ngix
EXPOSE 8080

# gunicorn
EXPOSE 8081

ENTRYPOINT ["/docker-entrypoint.sh"]
