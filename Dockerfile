FROM python:3.6-slim-buster

EXPOSE 80

USER root

RUN apt-get update -y

# from DMp base image https://github.com/alphagov/digitalmarketplace-docker-base/blob/main/base.docker
RUN /usr/bin/apt-get install -y --no-install-recommends nginx gcc curl xz-utils git \
        libpcre3-dev libpq-dev libffi-dev libxml2-dev libxslt-dev libssl-dev zlib1g-dev


# from DMp frontend image https://github.com/alphagov/digitalmarketplace-docker-base/blob/main/frontend.docker
ENV DEP_NODE_VERSION 14.16.1
RUN /usr/bin/curl -SLO "https://nodejs.org/dist/v${DEP_NODE_VERSION}/node-v${DEP_NODE_VERSION}-linux-x64.tar.xz" && \
    test $(sha256sum node-v${DEP_NODE_VERSION}-linux-x64.tar.xz | cut -d " " -f 1) = 85a89d2f68855282c87851c882d4c4bbea4cd7f888f603722f0240a6e53d89df && \
    /bin/tar -xJf "node-v${DEP_NODE_VERSION}-linux-x64.tar.xz" -C /usr/local --strip-components=1 && \
    /bin/rm "node-v${DEP_NODE_VERSION}-linux-x64.tar.xz"

RUN apt-get install -y postgresql postgresql-contrib

RUN apt-get install -y nginx-full

RUN apt-get install -y redis-server

# TODO remove this line - it is just to install tools for experimenting
RUN apt-get install -y vim net-tools telnet iproute2

RUN mkdir /dmp-contained

COPY ./files-for-container /dmp-contained/files

WORKDIR /dmp-contained/files/env-runner

RUN pip install -r requirements.in

# CMD ["/usr/local/bin/python3.6", "setup.py"]
