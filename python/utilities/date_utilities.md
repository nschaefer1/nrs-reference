
# Date Utilities

### Get Today Date as Integer

```python
from datetime import date

def get_today_as_int() -> int:
    """
    Return today's date as an integer in YYYYMMDD format.

    Returns:
        int: Today's date formatted as YYYYMMDD
    """
    today = date.today()
    return int(today.strftime('%Y%m%d'))
```


## Conversions

#### Convert Date to Integer

```python
def convert_date_to_int(d) -> int:
    """
    Convert a date-like input into an integer of format YYYYMMDD.

    Accepts:
        - datetime.datetime
        - datetime.date
        - ISO format string (YYYY-MM-DD)

    Returns:
        int: Date represented as YYYYMMDD
    """

    # Normalize input
    if isinstance(d, str):
        d = datetime.fromisoformat(d)
    elif isinstance(d, date) and not isinstance(d, datetime):
        d = datetime.combine(d, datetime.min.time())

    return int(d.strftime('%Y%m%d'))
```