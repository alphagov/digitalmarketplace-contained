FROM ubuntu:21.04

RUN mkdir /dmp-contained

COPY ./files-for-container /dmp-contained/files

RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y pip

ENV NODE_VERSION=14.7.0
RUN apt install -y curl
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN node --version
RUN npm --version

RUN apt-get install -y postgresql postgresql-contrib

RUN apt-get install -y nginx-full

RUN apt-get install -y redis-server
