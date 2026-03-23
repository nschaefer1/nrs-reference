
# Recommended PyWebview Architecture

## Purpose

PyWebview is a heavyweight GUI application that is easily deployed to users witout requiring Python to be installed on their computer. This architecture allows distribution of an executable and the utility of `pyinstaller` to package and distribute dependencies.

## Repository Structure

```
app/
├── .venv/
├── .gitignore
|
├── README.md
├── CHANGELOG.md
├── TODO.md
|
├── icon.ico
├── requirements.txt
|
├── main.py             ← entry point
|
├── backend/
|   ├── api/            ← documented in API section
|   ├── data/           ← documented in Data section
|   ├── models/
|   ├── utils/
|   └── services/
├── database.db         ← breifly covered in Data section
├── sql/                ← breifly covered in Data section
|   ├── seeds/
|   ├── create_dim.sql
|   ├── create_ft.sql
|   └── [additional_sql]/
|
├── frontend/
|   ├── index.html
|   ├── css/
|   ├── html/
|   ├── js/             ← router semantics covered in Router section
|   └── assets/
|
├── core/
├── config.json
├── data/
├── tests/
├── build/
└── dist/
```

## Module Setup

### Entry Point (MainApp)

The core entry point of the application should remain in `main.py` or `app.py`. This module should remain slim in nature, and only coordinate key players of the applicaiton. PyWebview module has a specific function to create a window.

- `db_manager` is a database manager that's passed into the main application. This controls all database interaction.
- `api` is the api that often takes the `db_manager` as an argument.

An example of a `db_manager` and `api` are provided below.

```python
import sys
import os
import webview

from backend.api.api import API
from backend.data.db_manager import DBManager

class MainApp:

    def __init__(self, db_manager, api):
        self.db_manager = db_manager
        self.api = api 
        index_html = self.app_path('index.html').replace('\\', '/')     # ← Update HTML path
        self.window = webview.create_window(
            'Window Title',
            f'file:///{index_html}',
            width=1200,
            height=800,
            js_api=self.api,
            text_select=True        # ← Users ability to select text in wrapper
        )

    def app_path(self, relative_path)
        if getattr(sys, 'frozen', False): 
            base_dir = os.path.dirname(sys.executable)
        else:   # This is the dev-env
            base_dir = os.path.dirname(__file__)
        return os.path.join(base_dir, relative_path)

    def run(self):
        webview.start(debug=True)       # ← Update debug/non-debug mode

if __name__ = '__main__':

    # Instantiate a logger
    # Load environment variables

    db_manager = DBManager()

    # Additional managers

    api = API(db_manager)
    app = MainApp(db_manager, api)

    # App startup
    app.run()    
```

### API

The core `api.py` module is the main coordinator of the API. Dependency classes are *optional* but *recommended* to increase scalability and modularity. Additionally, a `db_manager` is provided during instantiation - an example of this class is provided in the DBManager section.

**Assumed Module Structure** 

```
api/
└── api.py
    └── http_req/
        ├── __init__.py
        ├── delete.py
        ├── get.py
        ├── patch.py
        ├── post.py
        ├── put.py
        └── api_models/
            ├── api_response.py
            └── base_api.py
```

#### Main API Class (API)

```python
from backend.http_req import (
    APIDelete,
    APIGet,
    APIPatch,
    APIPost,
    APIPut
)

class API(APIDelete, APIGet, APIPatch, APIPost, APIPut):

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.session = {}                   # ← Editable in BaseAPI Class

    def resolve_path(self, rel_path: str) -> str:
        full = self.app_path(f'../frontend/{rel_path}')
        return full.replace('\\', '/')
    
    def app_path(self, relative_path):      # ← Also present in main app, duplicated to prevent coupling
        if getattr(sys, 'frozen', False):       
            base_dir = os.path.dirname(sys.executable)
        else:   # This is the dev-env
            base_dir = os.path.dirname(__file__)
        return os.path.join(base_dir, relative_path)
```

#### API Response

A response dataclass is provided for all HTTP requests to normalize the output and prepare for Javascript reception. 

```python
import logging
from dataclasses import dataclass
from typing import Any, Optional

logger = logging.getLogger(__name__)

##############################################################################

# RESPONSE CODES

    # 2xx Success
        # 200 OK: Request succeeded
        # 201 Created: Resource created (e.g., POST/PUT)
        # 204 No Content: Success, but not body to return (e.g., Delete)

    # 4xx Client Error
        # 400 Bad Request: Server cannot process due to client error
        # 401 Unauthorized: authentication missing or invalid
        # 403 Forbidden: Authenticated, but lacking permission
        # 404 Not Found: Resource does not exist
        # 429 Too Many Requests: Rate limit exceeded

    # 5xx Server Error
        # 500 Internal Server Error: Generic server error
        # 503 Service Unavailable: Server overloaded or down
        # 504 Gateway Timeout: Server acting as a gateway timed out

##############################################################################

@dataclass(frozen=True)
class APIResponse:
    success: bool
    message: str = ""
    data: Optional[Any] = None
    response_code: int = 200

    def __post_init__(self):
        if not self.success:
            logger.error(
                "API Response Failure | Code=%s | Message=%s",
                self.response_code,
                self.message
            )
        else:
            logger.debug(
                "API Resonse Success | Code=%s",
                self.response_code
            )
    
    def to_dict(self):
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "response_code": self.response_code
        }
```

#### BaseAPI

All HTTP verb Request classes are provided a BaseAPI class that houses functions utilized by all HTTP request types.

```python
import logging

logger = logging.getLogger(__name__)

from .api_response import APIResponse

class BaseAPI:

    def __init__(self):
        pass

    def _pull_into_json(self, data, col_names): # converts DB-style rows into JSON-friendly data
        return [
            {col: self._normalize_str(val) for col, val in zip(col_names, row)}
            for row in data
        ]   
    def _normalize_str(self, value):            # converts empty strings → None
        if isinstance(value, str) and value.strip() == "":
            return None
        return value
    def _normalize(self, obj):                  # converts empty strings → None in nested circumstances
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, str) and not v.strip():
                    obj[k] = None
                else:
                    self._normalize(v)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                if isinstance(v, str) and not v.strip():
                    obj[i] = None
                else:
                    self._normalize(v)
    
    # Proxy session state controls
    def set_session(self, key, value):
        self.session[key] = value
        logger.debug(f'Set {key}: {value}')
        return True
    def get_session(self, key):
        return self.session.get(key, None)
    def remove_session(self, key):
        logger.debug(f'Removed `{key}` from session')
        return self.session.pop(key, False)

    # Response wrappers
    def _success_response(self, data=None, message="", response_code=200):
        return APIResponse(
            success=True,
            message=message,
            data=data,
            response_code=response_code
        ).to_dict()
    def _failure_response(self, message, response_code=500, data=None):
        return APIResponse(
            success=False,
            message=message,
            data=data,
            response_code=response_code
        ).to_dict()
    def _format_db_rows(self, db_result, normalize=True):
        outgoing = self._pull_into_json(db_result.rows, db_result.columns)
        if normalize:
            outgoing = self._normalize(outgoing)
        return outgoing

    # Database response checks
    def _db_failure(self, db_result, default_message="Database failure"):
        if not db_result.success:
            return self._failure_response(
                    message = default_message,
                    response_code = 500
                )
        return None
            
    
    
```

**Important Notes**:
- `_pull_into_json` prepares structured data for Javascript reception
- `_normalize_str` nullifies any empty strings
- `_normalize` nullifies any empty strings in potential nested structure types
- Session state controls are not true session-state variables. These are intended to be persistent variables across different frontend views (e.g., Username)
- Standard response types are provided which wrap `APIResponse` for convenience - these are not required to be utilized.
- A `_db_failure` check is also provided presuming one is using the recommended `db_manager` structure outlined in this document.

**Backend → Frontend Pattern**

```python
# Steps

data = self._pull_into_json(rows, cols)
data = self._normalize(data)

return APIResponse(success=True, data=data).to_dict()
```

**Frontend → Backend Pattern**

```python
incoming = self._normalize(request_data)

# Steps

return APIResponse(success=True).to_dict()
```

> Ensure `to_dict()` is called after each APIResponse when explicitly sending a response back to the frontend.  

#### API Request Types (HTTP Verbs)

All HTTP verbs should have separate classes to maintain scalability and modularity. It's recommended to have these following classes in separate Python modules.

```python
import logging

logger = logging.getLogger(__name__)

from .api_models.api_response import APIResponse   # ← This import method sometimes does not work with Pyinstaller
from .api_models.base_api import BaseAPI

class APIDelete(BaseAPI):
    def __init__(self, db_manager):
        self.db_manager = db_manager

class APIGet(BaseAPI):
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def sample_get_request(self, user_id):              # SAMPLE
        db_result = self.db_manager.execute("query", params=(user_id,))

        failure = self._db_failure(db_result)
        if failure:
            return failure

        outgoing = self._format_db_rows(db_result)
        return self._success_response(data=outgoing)

    def verbose_sample_get_request(self, user_id):      # SAMPLE (returns same result as sample_get_request)
        db_result = self.db_manager.execute("query", params=(user_id,))

        if not db_result.success:
            return APIResponse(
                success=False,
                message="Database failure",
                response_code = 500,
            ).to_dict()
        
        outgoing = self._pull_into_json(db_result.rows, db_result.columns)
        outgoing = self._normalize(outgoing)        # Optional depending on DB schema

        return APIResponse(
            success=True,
            data=outgoing
        ).to_dict()
        
class APIPatch(BaseAPI):
    def __init__(self, db_manager):
        self.db_manager = db_manager

class APIPost(BaseAPI):
    def __init__(self, db_manager):
        self.db_manager = db_manager

class APIPut(BaseAPI):
    def __init__(self, db_manager):
        self.db_manager = db_manager
```

### Data

Data is assumed to be structured and updated with the application. It's intended that data sources are utilized for the current app runtime and not other sources. Helper SQL and the database itself should *not be contained in this folder*. This folder is *not intended* for distribution and accompanying `sql/` directories and `database.db` should remain next to the executable and not in any nested directory structures.

**Assumed Module Structure** 

```
data/
├── db_manager.py
└── db_response.py
```

#### SQL 

SQL will most likley need to be packaged in deployment with the main application. This folder should belong alongside the executable and accessed without any issue.

- `seeds/` is assumed to contain any prepopulated data required for the database to function.
- `create_dim.sql` is for *dimension* tables - assuming a relational database structure.
- `create_ft.sql` is for *fact* tables - assuming a relational database structure.
- `additional_sql/` directories are optional and can be applied to organize required SQL.

#### Database

The database is assumed to be a *SQLite* database using the `sqlite3` package in the Python Standard Library. This database is assumed to be in the same directory as the deployed executable. The Database Manager `DBManager` class outlined in this document will create this file if it does not exist during first application launch.

#### Database Return (DBReturn) 

The database return dataclass assists with normalizing database returns to ensure all data given is standardized and digestible for the API and any other Pythonic reception.

```python
import logging
from dataclasses import dataclass
from typing import List, Tuple, Any, Optional

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class DBReturn:
    success: bool
    columns: Optional[Tuple[str, ...]] = None
    rows: Optional[List[Tuple[Any, ...]]] = None
    row: Optional[Tuple[Any, ...]] = None
    row_count: Optional[int] = None

    def __post_init__(self):
        if not self.success:
            logger.error("DBReturn failure")
            return

        # Debug-level summary (safe, not too verbose)
        logger.debug(
            "DBReturn success | row_count=%s | columns=%s",
            self.row_count,
            self.columns
        )
```

#### Database Manager (DBManager)

The database manager is responsible for communications to the local database. It's presumed that the database will be a **SQLite** database. It's critical the schema is created *or checked to already be created* at every startup of the application.

```python
import sqlite3 as sql
import logging
import os

logger = logging.getLogger(__name__)

from .db_response import DBReturn
from contextlib import contextmanager

class DBManager:
    
    db_path = 'database.db'

    def __init__(self):
        start_sql = [
            "sql/create_dim.sql",
            "sql/create_ft.sql"
            # Insert additional sql files (create_index, etc.)
        ]
        for f in start_sql:
            result = self.execute_path(path=f, script=True)
            if not result.success:
                logger.error(f"Database initialization failed on step {f}")
                raise RuntimeError("Database initialization failed")
     
    def execute(self, query, params=None):
        with sql.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('PRAGMA foreign_keys = ON;') 
                if params is not None:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                rows = cursor.fetchall()
                conn.commit()
                columns = tuple([desc[0] for desc in cursor.description]) if cursor.description else ()
                return DBReturn(
                    success = True,
                    columns = columns,
                    rows = rows,
                    row_count = len(rows)
                )
            except Exception as e:
                conn.rollback()
                logger.exception(f'Execution failed, transaction rolled back')
                return DBReturn(
                    success = False
                )
    
    def execute_script(self, query):
        with sql.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('PRAGMA foreign_keys = ON;')
                cursor.executescript(query)
                conn.commit()
                return DBReturn(
                    success = True
                )
            except Exception as e:
                conn.rollback()
                logger.exception(f'SQL Script execution failed, transaction rolled back')
                return DBReturn(
                    success = False
                )
    
    def execute_path(self, path, script=False, params=None):
        with open(path, 'r', encoding = 'utf-8') as f:
            query = f.read()
        if script:
            return self.execute_script(query)
        else:
            return self.execute(query, params)

    def executemany(self, query, param_list):
        with sql.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('PRAGMA foreign_keys = ON;')
                cursor.executemany(query, param_list)
                conn.commit()
                return DBReturn(success=True)
            except Exception as e:
                conn.rollback()
                logger.exception(f'Executemany failed')
                return DBReturn(success=False)
    
    @contextmanager
    def transaction(self):
        conn = sql.connect(self.db_path)
        try: 
            conn.execute('PRAGMA foreign_keys = ON;')
            yield conn
            conn.commit()
            logger.debug(f'SQL transaction completed successfully.')
        except:
            conn.rollback()
            logger.exception(f'SQL transaction failed, rolling back.')
            raise
        finally:
            conn.close()
```

### Router

An example of a Javascript router is below containing information of how to navigate between multiple HTML pages with the PyWebview wrapper. This is sometimes complex given the HTML navigation is possible, but not always able to pass the API objects between them given the ecosystem of the wrapper.

> This is not covered in the Javascript directory given its specific use towards PyWebview and not applicable to other JS settings.

```javascript

// Function to utilize in other scripts
async function go(page) {
    const map = {
        
        // Sample pages
        pg1:   'html/pg1.html',
        pg2: 'html/pg2.html'

        // Add HTML here
    };

    const file = map[page];
    if (!file) {
        console.error('Route not found:', page);
        return;
    }

    try {
        const absolutePath = await window.pywebview.api.resolve_path(file);     // ← Present in the API class covered in this document
        window.location.href = `file:///${absolutePath}`;
    } catch (e) {
        console.error('Navigation failed:', e);
    }
}

// Expose function to window
window.go = go;

// F5 or Ctrl+R → refresh current page
document.addEventListener('keydown', (e) => {
    if (e.key === 'F5' || (e.ctrlKey && e.key === 'r')) {
        e.preventDefault();
        location.reload();
    }
});
```

**Usage Pattern**

This router should be included in **every single** HTML script before any other scripts. This exposes the function to the window making it available.

```html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="../css/global.css">
</head>

<body>
</body>

<script src="../js/router.js"></script>
<script src="../js/other_script.js"></script>

```

```javascript
window.addEventListener('pywebviewready', () => {
    let api = window.pywebview.api;
    init(api);
});

async function init(api) {
    html_item.addEventListener('click', () => {
        go('pg2')       // Navigates to pg2 given the click
    })
}
```

## Deployment

PyWebview deployment may require dependencies to be deployed for Windows. To do this you can use *PyInstaller*.

**Build Steps**

1. Install PyInstaller
   
```powershell
pip install pyinstaller
```

2. From the rpoject root, run:

```powershell
pyinstaller --noconfirm --onefile --windowed --name "Application Name v1.0.0" --icon "icon.ico" main.py
```

3. A `dist/` and `build/` folder should manifest the deployed executable.

**Notes**

- Additional assets like data, sql, and icons may need to be included in the build. You can configure this in a `.spec` file, or just accompany them during distribution.
- For more advanced distribution, consider using **Inno Setup** or **NSIS** once the `.exe` is stable
- A good source of icons is https://game-icons.net/ 
  - **No copyright infringement intended, will remove upon request.**