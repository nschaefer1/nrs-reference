
# Batch Startup References

This batch snippet walks through how to create a `.bat` file that starts up a Pythonic process with optional checks beforehand.

## Starting Lines

```bat
@echo off
setlocal enabledelayedexpansion
```

`enabledelayedexpansion` assists with expansive calculations in batch scripting. This is critical for for loops to behave as other languages.

## Security

The security layer here contains optional blocked path substrings, a keywrod, and and the script path. The *script path* is required in the final version of the script.

Replace the substrings, separated with a space, in 

```bat
:: ---- CONFIG: blocked path substrings (use quotes for spaces) ----
set BLOCKED="C:" "OneDrive" "Trend Analysis"

:: ---- CONFIG: keyword ----
set "SECRET=mysecret"

:: ---- Get script path ----
set "SCRIPT_PATH=%~dp0"
```

## Execution Blocker

This loops through all of the blocked paths and kills the script if the location of the batch script contains the value.

```bat
:: ---- Block execution if path contains forbidden strings ----
for %%B in (%BLOCKED%) do (
    set "TERM=%%~B"
    echo %SCRIPT_PATH% | find /i "!TERM!" >nul && exit /b
)
```

## Keyword Prompt

This asks the user for the keyword, killing the process if the keywork is incorrect. 

```bat
:: ---- Keyword prompt ----
set /p "USER_KEY=Enter keyword: "
if not "%USER_KEY%"=="%SECRET%" exit /b
```

## Begin Actual Process

1. Navigate to script directory
2. Create a virtual environment
3. Activate environment
4. Install requirements
5. Run python script
6. Capture PID

```bat
:: ---- Move to script directory ----
cd /d "%SCRIPT_PATH%"

:: ---- Create virtual environment if missing ----
if not exist venv (
    python -m venv venv || goto :end
)

:: ---- Activate virtual environment ----
call venv\Scripts\activate || goto :end

:: ---- Install requirements if present ----
if exist requirements.txt (
    pip install -r requirements.txt || goto :end
)

:: ---- Run python script + capture PID ----
for /f %%P in ('powershell -command "(Start-Process python main.py -PassThru).Id"') do (
    > pid.txt echo %%P
)

:end
echo.
pause
endlocal
```