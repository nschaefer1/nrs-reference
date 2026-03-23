
# File Utilities

#### Text Files

Basic text file *reading*, *writing* and *appending*.

```python
def read_text(path: str) -> str:
    """
    Read a text-based file and return its contents.

    Args:
        path (str): Path to the file.

    Returns:
        str: File contents as a single string.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
```

```python
def write_text(data: str, path: str, mode: str = "w") -> None:
    """
    Write text to a file.

    Args:
        data (str): Text to write.
        path (str): Destination file path.
        mode (str): File mode - "w" (overwrite) or "a" (append). Defaults to "w".
    """
    if mode not in {"w", "a"}:
        raise ValueError("mode must be 'w' (write) or 'a' (append)")

    with open(path, mode, encoding="utf-8") as f:
        f.write(data)
```

**Read and Write Single Lines**

```python
from typing import Callable, TypeVar
T = TypeVar("T")

def read_single_line(path: str, cast_type: Callable[[str], T] = str, default: T | None = None) -> T | None:
    """
    Read a file, strip surrounding whitespace, and cast the result.

    Args:
        path: File path to read from.
        cast_type: Function or type used to cast the string value.
        default: Value returned if reading or casting fails.

    Returns:
        The casted value, or the default if an error occurs.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            value = f.read().strip()

        if value == "":
            return default

        return cast_type(value)
    except Exception:
        return default
```

```python
from typing import Any

def write_single_line(content: Any, path: str) -> None:
    """
    Write a single value to a file as text.

    Args:
        content: Value to write.
        path: File path to write to.
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(content))
```

#### Directory Walker

Take a root directory and return all of the file paths that have the requested extension.

```python
def dir_walker(root, ext=None, mode=None):
    '''
    Walks all files under a given root directory and returns paths. 

    Libraries
    ----
    import os

    Parameters
    ----
    root : str
        The starting directory to walk.

    ext : str, optional
        If provided, only files ending with the extension are returned (e.g., 'png').

    mode: str, optional
        Controls how returned paths are formatted:
        - None (default): full normalized file paths.
        - 'relative': paths relative to the given root.
        - 'uri': file paths formatted as file:/// URIs.

    Returns
    ----
    list[str]
        A list of file paths formatted according to the selected mode.
    '''

    paths = []
    root_norm = os.path.abspath(root).replace('\\','/')

    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            # Skip files not matching the given extension
            if ext is not None and not name.lower().endswith(ext.lower()):
                continue
            # Remove backward slashes cuz we don't like those
            full_path = os.path.join(dirpath, name)
            normalized = os.path.abspath(full_path).replace('\\','/')
            # --- mode handling ---
            if mode == 'relative':
                trimmed = normalized.replace(root_norm + '/', '')
                paths.append(trimmed)
            elif mode == 'uri':
                drive, rest = os.path.splitdrive(normalized)
                drive = drive.upper() 
                uri = f"file:///{drive}{rest}"
                paths.append(uri)
            else:
                paths.append(normalized)

    return paths
```

#### CSV Files

CSV file handling of *reading*, *writing* and *appending*.

```python
import csv
from typing import List, Dict

def load_csv(path: str) -> List[Dict[str, str]]:
    """
    Load a CSV file and return rows as a list of dictionaries.

    Args:
        path (str): Path to the CSV file.

    Returns:
        List[Dict[str, str]]: Rows with column headers as keys.
    """
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

```

```python
import csv
from typing import List, Dict

def write_csv(
    data: List[Dict[str, str]],
    path: str,
    mode: str = "w"
) -> None:
    """
    Write rows to a CSV file.

    Args:
        data (List[Dict[str, str]]): Rows to write.
        path (str): Destination file path.
        mode (str): File mode - "w" (overwrite) or "a" (append). Defaults to "w".
    """
    if mode not in {"w", "a"}:
        raise ValueError("mode must be 'w' (write) or 'a' (append)")

    if not data:
        return  # nothing to write

    fieldnames = data[0].keys()

    write_header = True
    if mode == "a":
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                write_header = not f.read().strip()
        except FileNotFoundError:
            write_header = True

    with open(path, mode, newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if write_header:
            writer.writeheader()

        writer.writerows(data)
```