# Arianna Core Kernel v0.1

Minimal kernel on top of Arianna Core Linux for future AI systems. The project showcases a lightweight kernel with container, Python, and Node.js support.

## Structure

```
/core            — compiled kernel and modules
/arianna_core
  └── cmd       — monolithic Python utility
/usr/bin        — essential userland tools
/etc, /lib      — clean configs and libraries
```

## Kernel build

```sh
# Inside the Arianna Core container
apk add --no-cache bash util-linux build-base linux-headers \
    git bc bison flex elfutils-dev openssl-dev pkgconfig \
    python3 py3-pip nodejs npm curl wget

sh build_kernel.sh
```

After compilation the kernel resides in `core/boot`. The script attempts an automatic run via `qemu-system-x86_64` when `initramfs.img` is available.

## Cross-compilation

For ARM or other architectures install the appropriate `*-cross` packages and set `ARCH` and `CROSS_COMPILE` before running `build_kernel.sh`.

## Development tools

Required packages: `bash`, `busybox`, `util-linux`, `coreutils`, `build-base`, `linux-headers`, `python3`, `nodejs`, `npm`, `pkgconfig`.

Optional: `nano`, `vim`, `curl`, `wget`, `git`, `qemu-system-x86_64`.

## CLI

* `arianna.py` — unified tool that can mount devices, start services, and record health metrics to `/arianna_core/log/health.json`.

Add `/arianna_core/cmd` to `PYTHONPATH` to extend functionality and plug in custom agents.

## Hooks and events

Future versions may subscribe to kernel events through `netlink`, `dbus`, or file watchers. Scripts in `cmd` can react to logs or connections, enabling interactive AI agents.

## Extension

* To add a driver enable the proper `CONFIG_` flag in `kernel.config` and rebuild.
* Install compilers for other languages (Rust, Go) and include them in the image.
* Shared library support is provided by `pkgconfig` and `build-base`.

## Dockerfile

The `Dockerfile` here creates a reproducible build environment for Railway or any server.

## Bootable image

The build output can be packed into `tar.gz` or an ISO/IMG via `grub-mkrescue` and flashed to a USB drive.
