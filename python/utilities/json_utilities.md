# JSON Utilities

#### Read / Write JSON Files



```python
import json
from typing import Any

def read_json(path: str) -> Any:
    """
    Read a JSON file and return its contents.

    Args:
        path (str): Path to the JSON file.

    Returns:
        Any: Parsed JSON data.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

```


```python
import json
from typing import Any

def write_json(data: Any, path: str, indent: int = 1) -> None:
    """
    Write data to a JSON file (overwrite).

    Args:
        data (Any): JSON-serializable data.
        path (str): Destination file path.
        indent (int): Indentation level for formatting. Defaults to 1.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent)
```
