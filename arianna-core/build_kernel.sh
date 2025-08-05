#!/bin/sh
set -euo pipefail
# RU: Скрипт сборки ядра Arianna Core
# Требуемые пакеты: git build-base bc bison flex elfutils-dev openssl-dev linux-headers

KERNEL_VERSION=${KERNEL_VERSION:-6.6.32}

packages="git build-base bc bison flex elfutils-dev openssl-dev linux-headers wget"
for pkg in $packages; do
    if ! apk info --installed "$pkg" >/dev/null 2>&1; then
        apk add --no-cache "$pkg"
    fi
done

if [ ! -d "linux-$KERNEL_VERSION" ]; then
    wget "https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-$KERNEL_VERSION.tar.xz"
    tar -xf "linux-$KERNEL_VERSION.tar.xz"
    rm "linux-$KERNEL_VERSION.tar.xz"
fi

cd "linux-$KERNEL_VERSION"
cp ../kernel.config .config
# RU: Настройка конфигурации
make olddefconfig

# RU: Сборка
make -j"$(nproc)"
make modules_install INSTALL_MOD_PATH=../modules

mkdir -p "../core/boot"
cp arch/x86/boot/bzImage "../core/boot/vmlinuz-$KERNEL_VERSION"

# RU: Пробный запуск через QEMU
# Требуется qemu-system-x86_64 и initramfs
if command -v qemu-system-x86_64 >/dev/null 2>&1 && [ -f ../initramfs.img ]; then
    qemu-system-x86_64 -kernel "../core/boot/vmlinuz-$KERNEL_VERSION" -initrd "../initramfs.img" \
        -nographic -append "console=ttyS0" || true
fi
