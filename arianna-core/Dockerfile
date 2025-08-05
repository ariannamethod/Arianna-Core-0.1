# syntax=docker/dockerfile:1

# Pass kernel version at build time and expose to the runtime environment
ARG KERNEL_VERSION=6.6.32

# Build stage with full toolchain and headers
FROM alpine:3.20 AS build
ARG KERNEL_VERSION
ENV KERNEL_VERSION=${KERNEL_VERSION}
WORKDIR /root

# Required packages for building the kernel
RUN apk add --no-cache bash busybox-suid util-linux python3 py3-pip nodejs npm curl wget && \
    apk add --no-cache --virtual .build-deps build-base linux-headers git bc bison flex elfutils-dev openssl-dev pkgconfig

# Copy sources and build script
COPY kernel.config ./kernel.config
COPY build_kernel.sh /usr/local/bin/build_kernel.sh
# Build kernel and clean up build dependencies
RUN chmod +x /usr/local/bin/build_kernel.sh && \
    /usr/local/bin/build_kernel.sh && \
    apk del .build-deps

# Runtime stage with only the tools needed to run Arianna Core
FROM alpine:3.20
ARG KERNEL_VERSION
ENV KERNEL_VERSION=${KERNEL_VERSION}
WORKDIR /root

RUN apk add --no-cache bash busybox-suid util-linux python3 py3-pip nodejs npm curl wget

# Copy build artifacts
COPY --from=build /root/core /arianna_core/core
COPY --from=build /root/modules /arianna_core/modules
# Directories for custom scripts and logs
RUN mkdir -p /arianna_core/cmd /arianna_core/log
ENV PYTHONPATH=/arianna_core/cmd
ENV NODE_PATH=/arianna_core/cmd

CMD ["/bin/bash"]
