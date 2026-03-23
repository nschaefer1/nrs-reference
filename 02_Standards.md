
# Standards

## Commit Structure & Headers

All commits should fall into one of the following categories. The first line of a commit should be concise and describe the change clearly. Additional context may be added below the first line when necessary. Commit messages should follow the format:

```
<type>: <concise description of the change>

<Additional details may be included below the main commit line when necessary>
```


### Feat 
Represents the addition of a new feature or capability.  
The primary commit line should briefly describe the feature being introduced. Additional details describing individual changes should be included as bullet points below the main line when appropriate.

```
Feat: user can now remove and add items in inventory from inventory side panel.

- Method added to Pythonic Proxy API PUT class
- HTML updated with up/down, number, and submit buttons
- CSS updated with formatting
- JS updated with functionality & comms to API
- Additional logging added to Database Manager class to capture the edge-case of editing an inventory item that does not exist
```


### Fix

Represents a bug fix.

The primary line should briefly descirbe the issue resolved. Additional context may be provided below when necessary.

```
Fix: up button no longer resets the counter.

Additional context: the "up" button in the add item to inventory panel would reset the counter to zero in a scenario where the user had a negative. For example: a user wants to remove 4 items from inventory. They press the down button 5 times accidentally and then go to press the up button. The up button press resets the counter to zero, leading the user to have to press the down button 4 more times.
```

### Refactor

Represents code changes that improve structure, readability, or organization without altering functioanlity.

The primary line should descirbe the refactor objective. Additional context is optional.

```
Refactor: reorganized and renamed methods for a more logical and readable flow.

Additional context: the database manager methods were previously out of order and difficult to read without significant focus. Methods were renamed and reordered to improve clarity without changing performance or functionality.
```

### Chore / Style

Represents non-functional code changes such as formatting adjustments, comment additions, dependency cleanup, or other maintenance tasks.

```
Chore: removed unnecessary library imports at the start of script
```
```
Style: empty lines of code deleted
```

### Docs

Represents updates to documentation such as README files or other markdown-based documentation.

```
Docs: updated for v1.0.1 deployment
```

### Build

Represents changes to build systems, utility modules, or supporting files used by the application.

```
Build: initial commit on file utility module

Additional context: this file is intended to contain file manipulation functions such as reading files, performing atomic file saves, and related filesystem utilities.
```

### Perf

Represents performance based improvements that do not alter functionality.

```
Perf: streamlined API query to join on keys rather than a proxy custom index

Additional context: API query was joining on multiple columns instead of using the primary/foreign key relationship in the database. This has been updated to use the key relationship to improve efficiency where an index already exists.
```

### Test

Represents additions or changes to testing modules and test cases.


```
Test: initial commit on testing module
```
```
Test: added an edge case test for the grab_user API method
```
---

<div style="page-break-after: always;"></div>

## Repository Categorization

All repositories should be assigned a primary category that defines the intended structure, development expectations, and operational purpose of the project.

The base directory structure below is a recommended guideline, not a strict requirement. All repositories should maintain a clear and logical separation of concerns, regardless of their specific structure

```
Branch References:
├ (branch connector) Alt + 195
─ (horizontal line) Alt + 196
└ (end branch) Alt + 192
```

### Research and Development

This is the default state for new repositories.

Research and development repositories are intended for experimentation, prototyping, and exploratory work. During this phase, strict structural standards are not required. Development may include notebooks, exploratory scripts, and rapid iteration. Commit conventions and documentation requirements may be relaxed during this stage.

```
repo_name/
├── README.md
├── CHANGELOG.md        (optional)
├── TODO.md             (optional)
├── main.py             (optional entry point)
├── .venv/
├── data/               (optional local data, not required)
├── notebooks/          (optional)
├── experiments/        (optional)
├── outputs/            (optional)
└── src/
    ├── utils/          (shared helpers)
    ├── prototypes/     (experimental logic)
    ├── managers/       (orchestration / coordination)
    └── models/         (data structures / schemas)
```

### Command Line Interface Application

Command Line Interface (CLI) applications provide lightweight tools for interacting with systems or datasets through terminal commands.

These applications are typically used for operational tasks such as data input, administrative actions, system diagnostics, or generating quick reports. CLI tools may interact with other services or pipelines but generally remain minimal in scope and interface complexity.

```
+ pyproject.toml        (or requirements.txt)
+ cli.py                (argument parsing / commands)
+ tests/

src/
├── commands/           (CLI-specific actions)
├── services/           (core logic separated from CLI)
```

### Extract, Transform, Load Application

Extract, Transform, Load (ETL) applications are designed to move and process data between systems.

These applications typically operate without a graphical interface and are executed through scheduled jobs or automated pipelines. Their primary responsibilities include extracting data from external sources (e.g., files, APIs, databases), transforming that data into a structured format, and loading it into a destination system such as a database or data warehouse.

Communication from ETL applications typically occurs through logging or monitoring systems rather than interactive user interfaces.

```
+ config/               (connections, settings)
+ logs/                 (optional)
+ tests/

src/
├── extract/            (data ingestion)
├── transform/          (data processing)
├── load/               (data persistence)
├── pipelines/          (job orchestration)
```

### Insights Graphical User Interface Application

Insights GUI applications are designed to present analytical insights or summaries derived from datasets to end users.

These applications are often implemented using lightweight frameworks such as Python Streamlit or R Shiny. Deployments may be hosted internally on lightweight servers or distributed in a form that allows users to run the application locally. The primary goal of these applications is to allow users to explore and interpret data through visual interfaces.

```
+ app.py                (UI entry point)
+ assets/               (static resources)

src/
├── components/         (UI building blocks)
├── pages/              (views / screens)
├── services/           (data + business logic)
```

### Heavyweight Graphical User Interface Application

Heavyweight GUI applications are standalone desktop applications intended to run directly on a user's machine.

These applications are distributed as compiled executables and do not require the user to install development environments such as Python. The application is packaged with its required runtime and dependencies and operates independently of external servers, although it may interact with external services such as APIs.

Within this repository, heavyweight GUI applications are currently implemented using `PyWebview` and packaged with `PyInstaller`.

```
app/
│
├─ main.py                # application entrypoint
│
├─ frontend/              # UI layer
│   ├─ index.html
│   ├─ css/
│   ├─ js/
│   └─ assets/
│
├─ backend/               # application logic
│   ├─ api/               # exposed functions to frontend
│   ├─ services/          # business logic
│   ├─ models/            # data structures
│   └─ utils/
│
├─ core/                  # shared/system-level logic
│   ├─ config.py
│   ├─ logging.py
│   └─ constants.py
│
├─ data/                  # optional local data storage
│
├─ tests/
│
├─ requirements.txt
└─ build/                 # packaging (pyinstaller, etc.)
```