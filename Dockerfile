FROM python:3.7.12-slim

ARG EXTRA_TOOLS="python3-dev git git-lfs vim"

RUN apt-get update \
    && apt-get install -y --no-install-recommends $EXTRA_TOOLS

RUN pip3 install pyyaml==5.3.1

WORKDIR /workspace
COPY . .

RUN cd tool \
    && wget https://github.com/tuning003/zhila/releases/download/v1.1.3/zhila-linux_x86_64-v1.1.3.zip \
    && unzip *.zip \
    && rm *.zip \
    && mv zhila-* zhila/

ENTRYPOINT ["/workspace/entrypoint.sh"]
