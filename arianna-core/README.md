# Arianna Core Kernel v0.1

Минимальное ядро на базе Alpine Linux для будущих AI‑систем. Проект демонстрирует подход к созданию лёгкого ядра с поддержкой контейнеров, Python и Node.js.

## Структура

```
/core            — собранное ядро и модули
/arianna_core
  └── cmd       — пользовательские скрипты (Python/Node)
/usr/bin        — минимально необходимые утилиты
/etc, /lib      — чистые конфиги и библиотеки
```

## Сборка ядра

```sh
# Внутри контейнера Alpine
apk add --no-cache bash util-linux build-base linux-headers \
    git bc bison flex elfutils-dev openssl-dev pkgconfig \
    python3 py3-pip nodejs npm curl wget

sh build_kernel.sh
```

После сборки ядро располагается в `core/boot`. Скрипт пробует автозапуск через `qemu-system-x86_64` при наличии `initramfs.img`.

## Кросс‑компиляция

Для ARM или других архитектур установите соответствующие `*-cross` пакеты Alpine и задайте переменные окружения `ARCH` и `CROSS_COMPILE` перед запуском `build_kernel.sh`.

## Инструменты разработки

Обязательные пакеты: `bash`, `busybox`, `util-linux`, `coreutils`, `build-base`, `linux-headers`, `python3`, `nodejs`, `npm`, `pkgconfig`.

Опциональные: `nano`, `vim`, `curl`, `wget`, `git`, `qemu-system-x86_64`.

## API / CLI

* `ariannactl.js` — Node CLI для запуска сервисов и монтирования томов.
* `health_monitor.py` — пишет отчёты о CPU, памяти и диске в `/arianna_core/log/health.json`.

Добавьте `/arianna_core/cmd` в `PYTHONPATH` и `NODE_PATH`, чтобы расширять функциональность и подключать свои агенты.

## Hooks и события

В будущих версиях можно подписываться на события ядра через `netlink`, `dbus` или файловые наблюдатели. Скрипты в `cmd` могут реагировать на новые логи или подключения, реализуя интерактивные AI‑агенты.

## Расширение

* Для добавления нового драйвера — активируйте нужный `CONFIG_` в `kernel.config` и пересоберите.
* Для поддержки других языков (Rust, Go) установите соответствующие компиляторы и добавьте их в образ.
* Поддержка shared libraries обеспечивается `pkgconfig` и `build-base`.

## Dockerfile

`Dockerfile` в этом каталоге создаёт воспроизводимую среду сборки, пригодную для запуска в Railway или на любом сервере.

## Загрузка образа

Результат сборки можно упаковать в `tar.gz` или создать ISO/IMG средствами `grub-mkrescue` и записать на флешку.
