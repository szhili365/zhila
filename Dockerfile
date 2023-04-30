FROM python:3.7.12-slim

ARG EXTRA_TOOLS="vim wget zip unzip python3-dev git git-lfs"

RUN apt-get update \
    && apt-get install -y --no-install-recommends $EXTRA_TOOLS

WORKDIR /workspace
COPY . .

RUN cd tool \
    && wget https://github.com/tuning003/zhila/releases/download/v1.1.4/zhila-linux_x86_64-v1.1.4.zip \
    && unzip *.zip \
    && rm *.zip \
    && mv zhila-* zhila/ \
    && ls -la \
    && pwd

ENTRYPOINT ["/workspace/entrypoint.sh"]
