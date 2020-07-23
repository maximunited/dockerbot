#FROM python
#
#RUN pip install  docker speedtest-cli telepot --no-cache-dir
#
#RUN mkdir /opt/dockerbot
#
#COPY dockerbot.py /opt/dockerbot
#
#ENTRYPOINT ["/usr/bin/python", "/opt/dockerbot/dockerbot.py"]

FROM python:slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1


FROM base as builder

RUN apt-get update \
&& apt-get install libc-dev gcc -y --no-install-recommends\
&& apt-get clean
RUN mkdir /opt/dockerbot
WORKDIR /opt/dockerbot
COPY requirements.txt .
RUN pip install --trusted-host pypi.python.org --user --no-cache-dir -r requirements.txt

# Here is the production image
FROM base as app

ENV PATH=/root/.local/bin:$PATH
COPY --from=builder /root/.local /root/.local
COPY dockerbot.py /opt/dockerbot/dockerbot.py
WORKDIR /opt/dockerbot
ENTRYPOINT ["python"]
CMD ["/opt/dockerbot/dockerbot.py"]

