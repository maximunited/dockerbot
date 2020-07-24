# Base image
FROM python:slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PROJECT_NAME dockerbot
LABEL ${PROJECT_NAME}.image=base


# Staging image
FROM base as builder

ENV PROJECT_NAME dockerbot
LABEL ${PROJECT_NAME}.image=builder

# Dev packages needed for compilation of PIP packages
RUN apt-get update \
&& apt-get install libc-dev gcc -y --no-install-recommends \
&& apt-get clean
COPY requirements.txt /
RUN pip install --trusted-host pypi.python.org --user --no-cache-dir --no-warn-script-location -r /requirements.txt 

# Here is the production image
FROM base as app

ENV PROJECT_NAME dockerbot
LABEL ${PROJECT_NAME}.image=application

COPY --from=builder /root/.local /root/.local
COPY dockerbot.py /opt/dockerbot/
WORKDIR /opt/dockerbot
ENV PATH=/root/.local/bin:$PATH
ENTRYPOINT ["python"]
CMD ["/opt/dockerbot/dockerbot.py"]
