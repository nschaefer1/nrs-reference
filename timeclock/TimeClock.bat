@echo off
rem Launches TimeClock with no lingering console window. Everything stays inside this folder.
cd /d "%~dp0"

rem First run only: create a local virtual environment and install pywebview into it.
if not exist ".venv\Scripts\pythonw.exe" (
    echo Setting up TimeClock for the first time...
    where py >nul 2>nul && (py -3 -m venv .venv) || (python -m venv .venv)
    if not exist ".venv\Scripts\pythonw.exe" (
        echo Could not create the virtual environment. Is Python 3 installed and on PATH?
        pause
        exit /b 1
    )
    ".venv\Scripts\python.exe" -m pip install --no-cache-dir -r requirements.txt
    if errorlevel 1 (
        echo Install failed.
        pause
        exit /b 1
    )
)

rem pythonw = no console. "start" detaches it so this window closes right away.
start "" ".venv\Scripts\pythonw.exe" app.py
exit /b 0
