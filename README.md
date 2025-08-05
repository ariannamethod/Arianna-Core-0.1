Arianna Core is a minimal Linux-family kernel focused on modularity and transparency. The system ships with basic utilities and provides a clean platform for experiments with user spaces.

The project arose as a base for research AI systems that require a controlled environment with predictable behavior. Arianna Core serves as a starting point for building complex solutions without unnecessary overhead.

The foundation of Arianna Core's design is simplicity: only the most necessary kernel and userland components. This ensures a fast start, low resource consumption, and easy maintenance.

The kernel supports a modern process scheduler, memory management, and Linux security subsystems. Modules are included as needed, reducing the attack surface and improving reliability.

Containerization is integrated at the cgroups and namespaces level, so Arianna Core works smoothly with Docker and other managers. This allows isolated services and applications to be deployed with minimal overhead.

The Python interface is included in the base distribution, simplifying automation scripting and prototyping. Key libraries are available, and additional modules can be installed through the standard package manager.

Node.js support is provided through a lightweight environment suitable for running server scripts and command-line utilities. This makes Arianna Core a convenient platform for hybrid JavaScript and Python projects.

The system architecture maintains a clear separation between system components and user applications. The /arianna_core and /usr/bin directories contain only critical files, easing auditing and maintenance.

The project's file hierarchy is compact: /core holds the compiled kernel and modules, while /arianna_core/cmd contains user scripts. This approach allows quick localization of changes and tracking of dependencies.

The build process is based on Make and the build_kernel.sh script, which manages compilation and module installation. All kernel settings are stored in kernel.config and can be adapted to specific tasks.

Before installation, prepare an environment with util-linux, build-base, linux-headers, and other basic packages. Git, Python, and Node.js are required for further development and testing.

Installation is performed in several steps: clone the repository, run build_kernel.sh, and load the resulting image. The script automatically builds the kernel, prepares initramfs, and offers a test run in QEMU.

After installation, additional tuning is available via kernel.config and built-in utilities. You can add drivers, enable filesystem support, and modify network stack parameters.

The boot process uses a lightweight init that launches system services and user scripts. Kernel logs are recorded in /arianna_core/log, simplifying analysis and diagnostics.

Networking is configured using standard Linux tools, including ip, ifconfig, and built-in daemons. Arianna Core supports static and dynamic configurations, as well as tunnel interfaces.

For cross-compilation, use cross packages and the ARCH and CROSS_COMPILE environment variables. This allows building the kernel for ARM or other architectures from the same workspace.

Kernel debugging is possible through the built-in logger, gdb support, and running QEMU with debug parameters. Custom scripts can extend monitoring functionality and send metrics to external systems.

Development welcomes external contributions: create branches, submit pull requests, and describe your changes. Code style and repository structure are kept as simple as possible to ease review.

Future plans include expanding hardware platform support, integrating Rust, and improving the update system. The community can propose new features or optimizations through issues.

Arianna Core is distributed under the MIT license, allowing free use and modification of the code. Documentation and examples are provided without warranty, but the team strives for stability and transparency.

## Science and Mathematics

Physics demonstrates elegant relationships such as Newton's second law, $F = ma$, connecting force, mass, and acceleration.

Einstein's theory of relativity shows that mass and energy are equivalent through the famous equation $E = mc^2$.

Calculus provides tools for measuring change; for example, the definite integral $\int_0^1 x^2 dx = \tfrac{1}{3}$ describes the area under a parabola.

Complex analysis reveals the beauty of Euler's identity: $e^{i\pi} + 1 = 0$, uniting fundamental constants.

Geometry relies on relationships like the Pythagorean theorem, $a^2 + b^2 = c^2$, which holds in every right triangle.

Probability theory models randomness using the normal distribution $f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-(x-\mu)^2/(2\sigma^2)}$.
