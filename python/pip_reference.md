
# Pip Command Reference

## Install Packages

```bash
pip install package_name
pip install package_name==1.2.3
pip install "package_name>=1.0,<2.0"
```

## Upgrade / Reinstall

```bash
pip install --upgrade package_name
pip install --force-reinstall package_name
```

## Uninstall

```base
pip uninstall package_name
```

## List / Inspect

```bash
pip list
pip show package_name
pip freeze
```

## Requirements File

```bash
pip install -r requirements.txt
pip freeze > requirements.txt
```

## Virtual Environments

```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

## Cache

```bash
pip cache dir
pip cache purge
```

## Git Install

```bash
pip install git+https://github.com/user/repo.git
```