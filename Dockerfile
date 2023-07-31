FROM python:3.7.12-slim

ARG EXTRA_TOOLS="vim wget zip unzip python3-dev git git-lfs"

RUN apt-get update \
    && apt-get install -y --no-install-recommends $EXTRA_TOOLS

WORKDIR /zhila
COPY . .

RUN cd tool \
    && wget https://github.com/szhili365/zhila/releases/download/v1.1.6/zhila-linux_x86_64-v1.1.6.zip \
    && unzip *.zip \
    && rm *.zip \
    && mv zhila-* zhila/ \
    && chmod +x zhila/bin/*

ENTRYPOINT ["/zhila/entrypoint.sh"]
