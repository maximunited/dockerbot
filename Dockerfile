FROM python:2-slim

LABEL maintainer="tomer.klein@gmail.com"

RUN pip install --trusted-host pypi.python.org --no-cache-dir docker speedtest-cli telepot --no-cache-dir

RUN mkdir /opt/dockerbot

COPY dockerbot.py /opt/dockerbot

ENTRYPOINT ["python", "/opt/dockerbot/dockerbot.py"]
