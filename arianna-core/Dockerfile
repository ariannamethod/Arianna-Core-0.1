# syntax=docker/dockerfile:1
FROM alpine:3.20

# RU: Базовые пакеты и инструменты разработки
RUN apk add --no-cache bash busybox-suid util-linux build-base linux-headers \
    git bc bison flex elfutils-dev openssl-dev pkgconfig \
    python3 py3-pip nodejs npm curl wget

# RU: Копируем конфиг и скрипт сборки
COPY kernel.config /root/kernel.config
COPY build_kernel.sh /usr/local/bin/build_kernel.sh
RUN chmod +x /usr/local/bin/build_kernel.sh

# RU: Директория для кастомных скриптов
RUN mkdir -p /arianna_core/cmd /arianna_core/log
ENV PYTHONPATH=/arianna_core/cmd
ENV NODE_PATH=/arianna_core/cmd

CMD ["/bin/bash"]
