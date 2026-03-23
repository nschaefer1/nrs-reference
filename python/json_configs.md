# JSON Configuration Class

## Purpose

Provide a simple consistent mechanism for reading, modifying, and persisting application configuration files.

This pattern ensures that configuartion is: 

- automatically initialized with defaults
- safely loaded into memory
- persistently saved after motification

## Pattern

**Edit the following before incorporating**:  
1. Default dictionary attribute
2. Default config path in constructor

```python
import json

class ConfigJSON:

    DEFAULTS = {
        'x': 'y'
    }

    def __init__(self, path='config.json'):
        self.path = path 

    def __enter__(self):
        try:
            with open(self.path, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = dict(self.DEFAULTS)
            with open(self.path, 'w') as f:
                json.dump(self.data, f, indent=1)
        return self.data
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=1)
```

## Behavior and Usage

Example usage if a user were to press a button changing from light to dark mode (or other mode types).

```python
if theme_change_button_press:

    new_theme = 'light' if curr_theme != 'light' else 'dark'

    try:
        with ConfigJSON() as config:
            config['theme'] = new_theme
    except Exception as e:
        print(f'Critical error updating config file: {e}')
        return  # stop if we error

    try:
        backup_theme = curr_theme
        curr_theme = new_theme
    except Exception as e:
        print(f'Error applying theme in application, rolling back config: {e}')
        with ConfigJSON() as config:
            config['theme'] = backup_theme
        curr_theme = backup_theme
 
```