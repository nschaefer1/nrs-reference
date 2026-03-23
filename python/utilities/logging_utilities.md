
# Logging Utilities

#### Basic Logger

```python
import logging
from typing import Optional


def init_logger(
    log_file: Optional[str] = None,
    mode: str = "a",
    level: int = logging.INFO
) -> None:
    """
    Initialize application logging.

    Args:
        log_file (str, optional): File path for logging output. If None, logs to console only.
        mode (str): File mode - "w" (overwrite) or "a" (append). Defaults to "a".
        level (int): Logging level. Defaults to logging.INFO.
    """
    if log_file and mode not in {"w", "a"}:
        raise ValueError("mode must be 'w' (write) or 'a' (append)")

    handlers = [logging.StreamHandler()]

    if log_file:
        handlers.append(logging.FileHandler(log_file, mode=mode))

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers
    )
```
