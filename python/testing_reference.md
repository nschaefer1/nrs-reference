# Python Testing Reference

A practical, step-by-step reference for installing, creating, and running tests with `pytest`, plus common ways to gate script execution based on test results.

## 1) Install pytest

Create and activate a virtual environment first.

```bash
python -m venv .venv
```

### Windows
```bash
.venv\Scripts\activate
```

## 2) Create your first test

Example project:

```text
project/
├─ app.py
└─ tests/
   └─ test_app.py
```

`app.py`

```python
def add(a, b):
    return a + b
```

`tests/test_app.py`

```python
from app import add


def test_add():
    assert add(2, 3) == 5
```

Basic pytest conventions:

- Test files usually start with `test_` or end with `_test.py`.
- Test functions usually start with `test_`.
- `assert` is the normal way to express expectations.

## 3) Run tests

Run all discovered tests:

```bash
pytest
```

Recommended form:

```bash
python -m pytest
```

Run one file:

```bash
python -m pytest tests/test_app.py
```

Run one test function:

```bash
python -m pytest tests/test_app.py::test_add
```

Useful options:

```bash
python -m pytest -q        # quieter output
python -m pytest -v        # more detail
python -m pytest -x        # stop on first failure
python -m pytest --maxfail=3
```

## 4) Understand pass / fail behavior

Pytest exits with a process exit code. For normal scripting, the main thing you need is:

- `0` = tests passed
- non-zero = something failed or pytest hit an error

That means you can gate other commands based on whether tests succeed.

## 5) Run tests before running a script

### Scenario A: Only run the script if tests pass

#### Windows batch
```bat
python -m pytest
if errorlevel 1 exit /b 1
python app.py
```

#### PowerShell
```powershell
python -m pytest
if ($LASTEXITCODE -ne 0) { exit 1 }
python app.py
```
Use this when you want a hard gate: test failures should stop execution.

### Scenario B: Run the script even if tests fail

#### Windows batch
```bat
python -m pytest
python app.py
```

#### PowerShell
```powershell
python -m pytest
python app.py
```

Use this when tests are informational only.

### Scenario C: Run tests, log failure, then continue

#### Windows batch
```bat
python -m pytest
if errorlevel 1 echo Tests failed, continuing anyway...
python app.py
```

Use this when you want visibility without blocking the script.

## 6) Put the test gate inside Python

If you want one Python file to run tests first and decide what happens next:

```python
import subprocess
import sys

result = subprocess.run([sys.executable, "-m", "pytest"])
if result.returncode != 0:
    print("Tests failed")
    sys.exit(1)

print("Tests passed; running app")
```

Change the failure branch if you want to continue instead of exiting.

## 7) Make this your standard command

A common workflow is:

```bash
python -m pytest && python app.py
```

That is the simplest answer to: "Make sure tests run before the script, and fail if they do not pass."

## 8) Add a reusable launcher script

### Windows `run_app.bat`

```bat
@echo off
python -m pytest
if errorlevel 1 (
    echo Tests failed. Stopping.
    exit /b 1
)
python app.py
```

### PowerShell `run_app.ps1`

```powershell
python -m pytest
if ($LASTEXITCODE -ne 0) {
    Write-Host "Tests failed. Stopping."
    exit 1
}
python app.py
```

This is usually the cleanest local setup on Windows.

## 9) Common testing patterns

### Basic assert

```python
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
```

### Check that an exception is raised

```python
import pytest


def divide(a, b):
    return a / b


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
```

### Group related cases

```python
import pytest


@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (2, 3, 5),
    (10, 5, 15),
])
def test_add_cases(a, b, expected):
    assert a + b == expected
```

## 10) Skip or mark tests intentionally

Skip a test:

```python
import pytest


@pytest.mark.skip(reason="not ready yet")
def test_future_feature():
    assert True
```

Mark as expected failure:

```python
import pytest


@pytest.mark.xfail(reason="bug not fixed yet")
def test_known_bug():
    assert 1 == 2
```

Use `skip` when you do not want the test to run. Use `xfail` when you expect it to fail for now.

## 11) Keep configuration in one place

You can put pytest config in `pyproject.toml`.

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-q"
```

This keeps your command line simpler.

## 12) Run tests automatically before commits

If you want tests to run before every Git commit, `pre-commit` is a common choice.

Install it:

```bash
python -m pip install pre-commit
pre-commit install
```

Example `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: python -m pytest
        language: system
        pass_filenames: false
```

Now commits will run tests first. If the hook fails, the commit is blocked.

## 13) Run tests across environments

If you want a more formal test runner for multiple Python versions or multiple commands, use `tox`.

Install it:

```bash
python -m pip install tox
```

Example `tox.toml`:

```toml
env_list = ["py"]

[env.py]
deps = ["pytest"]
commands = [["python", "-m", "pytest"]]
```

Run it:

```bash
tox
```

Use `tox` when you want repeatable environments, not just one local test command.

## 14) Most useful commands at a glance

```bash
python -m pip install pytest
python -m pytest
python -m pytest -q
python -m pytest -v
python -m pytest -x
python -m pytest tests/test_app.py
python -m pytest tests/test_app.py::test_add
```

## 15) Recommended default workflow

For a simple local project:

1. Put tests in `tests/`
2. Run with `python -m pytest`
3. Launch your script through a small wrapper script
4. Use a hard gate unless you have a reason not to

Example hard-gate launcher:

```bat
python -m pytest
if errorlevel 1 exit /b 1
python app.py
```

## 16) Quick decision guide

- Want the script to stop when tests fail? Use `&&` or an `errorlevel` check.
- Want the script to continue even when tests fail? Run pytest first, then run the script without checking the exit code.
- Want automatic enforcement before commits? Use `pre-commit`.
- Want reproducible test environments? Use `tox`.

## Sources

This reference follows the official pytest getting started and usage docs, the Python `unittest` docs for standard-library context, the official `pre-commit` docs for commit hooks, and the official tox user guide for multi-environment test automation.

