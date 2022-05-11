# Example run to put the files in /host/path/dir on the host:
# docker run -it -v /tmp/resto:/data --rm m1dnight/vub-resto-v3 --history --version 1

FROM python:3.10
LABEL maintainer "Christophe De Troyer <christophe@call-cc.be>"

# Get project
ADD . /app
WORKDIR /app

# Dependencies
RUN pip install -r requirements.txt

RUN mkdir /data

ENTRYPOINT ["python", "/app/main.py", "--output", "/data"]