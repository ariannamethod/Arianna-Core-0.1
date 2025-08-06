# Arianna Core (Arianna Linux)

**Arianna Core** is a compact Linux-family kernel engineered for modularity, transparency, and efficient research workflows.  
It provides a lightweight foundation for building AI-driven systems and controlled user spaces, while maintaining clarity in both architecture and usage.

## Overview

Arianna Core was created as a research baseline for AI environments that demand predictable behavior and minimal overhead.  
By focusing only on essential kernel and userland components, the system ensures fast boot times, low resource consumption, and straightforward maintenance.

- **Modern process scheduler, memory management, and Linux security subsystems** are included.
- Modules are loaded as needed, keeping the attack surface small and reliability high.

## Features

- **Containerization**: Built-in support for cgroups and namespaces enables seamless operation with Docker and other container managers. This makes isolated deployments trivial and resource-efficient.
- **Python interface**: Pre-installed Python and key libraries simplify automation and rapid prototyping. Additional packages can be managed with the standard package manager.
- **Node.js support**: Lightweight Node.js environment for running server-side scripts and CLI tools, perfect for hybrid Python/JS projects.
- **Clear file hierarchy**:  
  - `/core`: compiled kernel and modules  
  - `/arianna_core/cmd`: user scripts  
  - `/usr/bin`: only essential binaries  
  This structure simplifies updates, auditing, and troubleshooting.
- **Easy build and configuration**:  
  - Uses `Make` and `build_kernel.sh` for compilation and module installation.  
  - Kernel settings are centralized in `kernel.config` for quick adaptation.

## Installation

1. **Prepare the environment**:  
   Install `util-linux`, `build-base`, `linux-headers`, plus `git`, `python`, and `nodejs`.
2. **Clone the repository**.
3. **Build**:  
   Run `build_kernel.sh` to compile the kernel, set up modules, and prepare `initramfs`.
4. **Test**:  
   The script offers test boot in QEMU.
5. **Tune**:  
   Further configuration is done via `kernel.config` and provided utilities. Add drivers, enable filesystems, adjust network stack, etc.

## Boot and Logging

- Boot uses a minimal init to launch system services and user scripts.
- Kernel logs are stored in `/arianna_core/log` for easy diagnostics.

## Networking

- Standard Linux networking tools (`ip`, `ifconfig`, built-in daemons) for configuration.
- Supports both static/dynamic IPs and tunnel interfaces.

## Development

- **Cross-compilation**: Use cross packages and set `ARCH` and `CROSS_COMPILE` as needed (e.g., for ARM).
- **Debugging**: Integrated logger, gdb support, and QEMU debug flags are available. Custom monitoring and metric scripts can be added.
- **Contribution**: External contributions are welcome — branch, PR, describe your changes. Code style and repo structure are kept intentionally simple.

## Future Roadmap

- Expanding hardware/platform support
- Native Rust integration
- Smarter update and patch system
- Community-driven feature proposals and optimizations

## Licensing

Arianna Core is released under the MIT license — open for any use or modification.  
Docs and examples come as-is, but the team strives for clarity, stability, and transparent development.

---

## Science and Mathematics

Physics demonstrates elegant relationships, e.g. **Newton's second law**:  
$F = ma$ (force, mass, acceleration)

Einstein's theory of relativity equates mass and energy:  
$E = mc^2$

Calculus tools for change, e.g.  
$\int_0^1 x^2 dx = \tfrac{1}{3}$ (area under a parabola)

Complex analysis reveals the beauty of **Euler’s identity**:  
$e^{i\pi} + 1 = 0$

Geometry relies on the **Pythagorean theorem**:  
$a^2 + b^2 = c^2$

Probability models randomness:  
$f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-(x-\mu)^2/(2\sigma^2)}$ (normal distribution)

---

*For documentation, usage, and troubleshooting, see included examples or open an issue.*