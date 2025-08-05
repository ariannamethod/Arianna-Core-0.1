#!/bin/sh
set -e
# RU: Скрипт сборки ядра Arianna Core
# Требуемые пакеты: git build-base bc bison flex elfutils-dev openssl-dev linux-headers

KERNEL_VERSION=${KERNEL_VERSION:-6.6.32}

apk add --no-cache git build-base bc bison flex elfutils-dev openssl-dev linux-headers wget

if [ ! -d "linux-$KERNEL_VERSION" ]; then
    wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-"$KERNEL_VERSION".tar.xz
    tar -xf linux-"$KERNEL_VERSION".tar.xz
fi

cd "linux-$KERNEL_VERSION"
cp ../kernel.config .config
# RU: Настройка конфигурации
make olddefconfig

# RU: Сборка
make -j"$(nproc)"
make modules_install INSTALL_MOD_PATH=../modules

mkdir -p ../core/boot
cp arch/x86/boot/bzImage ../core/boot/vmlinuz-"$KERNEL_VERSION"

# RU: Пробный запуск через QEMU
# Требуется qemu-system-x86_64 и initramfs
if [ "${RUN_QEMU:-no}" = "yes" ]; then
    if ! command -v qemu-system-x86_64 >/dev/null 2>&1; then
        echo "qemu-system-x86_64 not found. Install QEMU to run the boot test." >&2
        exit 1
    fi
    if [ ! -f ../initramfs.img ]; then
        echo "initramfs.img not found at ../initramfs.img" >&2
        exit 1
    fi
    qemu-system-x86_64 -kernel ../core/boot/vmlinuz-"$KERNEL_VERSION" -initrd ../initramfs.img \
        -nographic -append "console=ttyS0"
else
    echo "RUN_QEMU not set to yes; skipping QEMU boot test."
fi
