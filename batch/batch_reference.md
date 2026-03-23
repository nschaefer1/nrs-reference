# Batch Scripting (CMD) Reference

## Overview

Batch scripting is a text-based command interpreter (CMD). It operates
on plain text, not objects.

## Core Command Table

  Command    Use Case           Example
  ---------- ------------------ -------------------------
  echo       Print text         `echo Hello`
  set        Define variable    `set x=10`
  cd         Change directory   `cd C:\Temp`
  dir        List files         `dir`
  copy       Copy files         `copy file.txt dest\`
  del        Delete files       `del file.txt`
  start      Run program        `start notepad`
  tasklist   List processes     `tasklist`
  taskkill   Kill process       `taskkill /PID 1234 /F`

## Variables

  ---------------------------------------------------------------------------------------
  Concept                   Example                   Notes
  ------------------------- ------------------------- -----------------------------------
  Declare variable          `set VAR=value`           No spaces

  Use variable              `%VAR%`                   Static expansion

  Delayed expansion         `!VAR!`                   Requires
                                                      `setlocal enabledelayedexpansion`

  Environment vars          `%PATH%`                  Built-in
  ---------------------------------------------------------------------------------------

## Using Variables

``` bat
set NAME=John
echo Hello %NAME%
```

With delayed expansion:

``` bat
setlocal enabledelayedexpansion
set COUNT=0
set /a COUNT=!COUNT!+1
echo !COUNT!
```

## Running Scripts

  Method         Example
  -------------- --------------------
  Direct run     `script.bat`
  From CMD       `call script.bat`
  Double-click   Runs in new window

## Parameters in Scripts

``` bat
echo First param: %1
echo Second param: %2
```

Call:

``` bat
script.bat hello world
```

## Control Flow

``` bat
if "%1"=="test" echo Match

for %%A in (1 2 3) do echo %%A

goto :label

:label
echo Done
```

## Script vs Interactive Use

  Scenario          Recommendation
  ----------------- -------------------
  Simple commands   Run directly
  Reusable tasks    `.bat` file
  Automation        `.bat` file
  Complex logic     Prefer PowerShell

## Key Differences vs PowerShell

-   Text-based (no objects)
-   Limited error handling
-   Simpler syntax
-   Faster startup
-   Less powerful for data manipulation

## Things to Keep in Mind

-   `%VAR%` evaluated at parse time
-   Use `!VAR!` inside loops
-   No native JSON/object handling
-   Quoting is fragile
-   Debugging is harder

## Common Patterns

### Silent execution

``` bat
@echo off
```

### Error handling

``` bat
command || exit /b
```

### Redirect output

``` bat
command > output.txt
command 2> error.txt
```

## When to Use Batch

-   Lightweight scripts
-   System startup scripts
-   Simple automation
-   Legacy environments
