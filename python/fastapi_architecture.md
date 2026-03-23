
# FastAPI Architecture

FastAPI is a lightweight framework for building APIs that expose endpoints over HTTP. These endpoints can eb consumed by frontend applications, scripts, or other services.

FastAPI applications are typically run using `uvicorn`, which serves the app.

## Directory Structure

```
app/
├── main.py            (entry point)
├── requirements.txt
├── .venv/
├── startup.bat        (optional)
├── logs/              (optional)
└── src/
    ├── routes/        (API endpoints)
    ├── services/      (business logic)
    ├── utils/         (helpers)
    └── models/        (optional data structures)
```

## Modularity in Endpoints

As your API grows, avoid putting everything in one file. Split endpoints into modules based on **feature** or **domain**, not just size.

```python
@app.get("/...")
@app.post("/...")
@app.put("/...")
```

**Example: route separation**

```
src/
├── routes/
│   ├── users.py
│   ├── jobs.py
│   └── health.py
```

**Example: `users.py`**

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_users():
    return {"users": []}
```

**Registering the Route in `main.py`**

```python
from fastapi import FastAPI
from src.routes import users

app = FastAPI()

app.include_router(users.router, prefix="/users")
```

### Separation of Concerns

**routes/**
  - Defines HTTP endpoints
  - Handles requests/response

**services/**
  - Contains logic (calculations, DB calls, etc.)
  - Should not depend on FastAPI

**models/** (optional)
  - Data structures / schemas

### Separation of HTTP Verbs in Modules

Do not split files by *get* vs *post* commands. Group by *feature* not *HTTP verb*. 

## Startup of Process

**Basic Method**

```powershell
cd "path/to/root"

uvicorn file_name:app
uvicorn file_name:app --reload
```

Use the `--reload` argument automatically restarts the server when code changes.

**Advanced Method**

You may need to "cd" to a file path before this, see PowerShell references for more information on this and parameterization.

```powershell
Start-Process `
    -FilePath "path/to/python.exe" `
    -ArgumentList "-m uvicorn file_name:app --host 127.0.0.1 --port 8001" `
    -Working Directory "." `
    -RedirectStandardOutput ".\uvicorn.log" `
    -RedirectStandardError ".\uvicorn_error.log" `
    -PassThru `
    -NoNewWindow
```