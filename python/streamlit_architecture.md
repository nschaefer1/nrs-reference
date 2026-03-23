
# Streamlit Architecture

[Official Streamlit API Documentation](https://docs.streamlit.io/develop/api-reference)

## Recommended Directory Structure

```
app/
├── .streamlit/
|   └── config.toml     (optional)
├── README.md
├── CHANGELOG.md        (optional)
├── TODO.md             (optional)
├── app.py
├── .venv/
├── startup.bat         (optional)
├── data/
├── assets/
├── pages/              (streamlit routing)
└── src/
    ├── utils/          (shared helpers)
    ├── components/     (UI elements)
    ├── services/       (business logic / state)
    ├── state/          (session state management)
    └── models/         (optional, data structures)
```

**Mental Model**

```
UI (components/pages)
    ↓
State (session orchestration)
    ↓
Services (pure logic)
    ↓
Models (data)
```

## Streamlit Page Configurations

By defualt, this is a useful page config you can utilize. This sets the page title, icon, and page layout to wide. Additional arguments are available.

```python
import streamlit as st

st.set_page_config(
    page_title='Streamlit System Grid',
    page_icon='assets/png/heart-beats.png',
    layout='wide',
    menu_items=None
)
```

## Multipage Applications

Streamlit offers a multipage function by default interactable via the sidebar with a root directory `pages/` folder. Pages can also be navigated with the `switch_page` function in streamlit.

```python
import streamlit as st

if st.button('Hi'):
    st.switch_page('page.py')
```

To turn the automatic loading of the pages in the sidebar, this piece of code can be deposited in the `config.toml` of the `.streamlit/` directory.

```toml
[server]
enableStaticServing = false

[global]
showWarningOnDirectExecution = false

[client]
showSidebarNavigation = false
```

## Running a Streamlit Applicatoin

**Basic Method**

```powershell
cd "path/to/wd"

streamlit run app.py
```

**Advanced Method**

```powershell
Start-Process `
    -FilePath "path/to/python.exe" `
    -ArgumentList "-m streamlit run app.py --server.port 8501 --server.headless true" `
    -WorkingDirectory "." `
    -RedirectStandardOutput ".\streamlit.log" `
    -RedirectStandardError ".\streamlit_error.log" `
    -PassThru `
    -NoNewWindow
```

