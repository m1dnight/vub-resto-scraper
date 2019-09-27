# Example run to put the files in /host/path/dir on the host:
# docker run -it --rm -v /host/path/dir:/data m1dnight/vub-resto /data/

FROM python:3.5
LABEL maintainer "Christophe De Troyer <christophe@call-cc.be>"

# Install dependencies.
RUN apt-get update
RUN apt-get install -y --no-install-recommends git ca-certificates python-levenshtein && rm -rf /var/lib/apt/lists/*

# Get project
ADD . /app
WORKDIR /app

# Dependencies
RUN pip install -r requirements.txt

RUN mkdir /data

ENTRYPOINT ["python", "/app/main.py", "--output", "/data"]