# Environment Probe

A reproducible Python diagnostic CLI package built with Python 3.12+ to inspect and verify runtime environment isolation and configuration state.

---

## 1. Fresh Setup

From a clean working directory, clone the repository and reproduce the isolated environment using the committed lockfile:

```bash
# Clone the repository
git clone https://github.com/yuwa619/environment-probe
cd environment-probe

# Reproduce the exact isolated environment from the lockfile
uv sync --frozen
```

---

## 2. Successful Execution

Set the required `APE_ENVIRONMENT` variable and execute the probe as a module using `uv run`:

```bash
$ APE_ENVIRONMENT=development uv run python -m environment_probe
{
  "package_version": "0.1.0",
  "python_version": "3.12.3",
  "environment_name": "development"
}

$ echo $?
0
```

* **Exit Code:** `0`
* **Output:** Formatted JSON payload printed to `stdout` containing `package_version`, `python_version`, and `environment_name`.

---

## 3. Missing-Configuration Failure

When executed without `APE_ENVIRONMENT`, the probe terminates immediately with an informative error message and suppresses raw stack traces or internal paths:

```bash
$ unset APE_ENVIRONMENT
$ uv run python -m environment_probe
Configuration Error: Required environment variable 'APE_ENVIRONMENT' is not set.

$ echo $?
1
```

* **Exit Code:** `1`
* **Output:** Error string written to `stderr` without tracebacks or path exposure.

---

## 4. Verification Results

### A. Bytecode Compilation
Verifies all source files within `src/` are syntactically valid and compile cleanly:

```bash
$ uv run python -m compileall src/
Listing 'src'...
Listing 'src/environment_probe'...
Compiling 'src/environment_probe/__init__.py'...
Compiling 'src/environment_probe/__main__.py'...
Compiling 'src/environment_probe/probe.py'...

$ echo $?
0
```

### B. Static Type Checking (`mypy`)
Validates that all public functions and signatures conform to type annotations:

```bash
$ uv run mypy src/
Success: no issues found in 3 source files

$ echo $?
0
```

---

## 5. Engineering Decisions

This project standardizes on `uv` alongside a `src`-layout structure to eliminate non-reproducible runtime environments and "works on my machine" defects.

Managing project dependencies across varied developer laptops and CI runners frequently suffers from drift caused by unpinned transitive dependencies and implicit reliance on global site-packages. Using `uv` guarantees strict virtual environment isolation, ensuring that Python resolves only explicitly declared packages inside `.venv` rather than ambient system installations.

Deterministic reproducibility is enforced via the committed `uv.lock` file. While `pyproject.toml` declares high-level dependency constraints, `uv.lock` records the exact pinned versions, transitive dependency graphs, and platform hashes. Executing `uv sync --frozen` guarantees that every fresh clone builds an identical environment bit-for-bit without querying remote registries or unexpectedly resolving newer, breaking releases.

Additionally, adopting a `src`-layout (`src/environment_probe`) prevents Python from implicitly adding the project root to `sys.path`. This forces Python to execute the code as a formally installed package inside the isolated virtual environment, matching production packaging and import behaviors. Together, `uv`, `uv.lock`, and the `src` layout provide lightweight, deterministic isolation without requiring container overhead.

