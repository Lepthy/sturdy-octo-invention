FROM debian:latest

RUN apt-get update \
    && apt-get install -y make \
    && apt-get install -y python3 \
    && apt-get install -y python3-venv

ENV PROJECT_DIRECTORY /var/crawler

ADD . ${PROJECT_DIRECTORY}
WORKDIR ${PROJECT_DIRECTORY}

# This is used to docker-cache the setup
ADD requirements.txt requirements.txt

RUN make setup

ENTRYPOINT [ "./run.sh" ]