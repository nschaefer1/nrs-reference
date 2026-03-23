
# Powershell Command Reference

## Overview

Powershell is an object-based shell and scripting language. Commands (cmdlets) return structured objects, not plain text.

## Core Command Table

Command | Use Case | Example
---- | ---- | ----
`Get-Command` | List available commands | `Get-Command`
`Get-Help` | View help/docs | `Get-Help Get-Process -Full`
`Get-Location` | Current directory | `Get-Location`
`Set-Location` | Change directory | `cd C:\Temp`
`Get-ChildItem` | List files (like `ls`) | `ls`
`Copy-Item` | Copy files | `cp file.txt dest\`
`Remove-Item` | Delete files | `rm file.txt`
`Start-Process` | Run external program | `Start-Process notepad`
`Get-Process` | List processes | `Get-Process`

## Variables

Concept | Example | Notes
--- | --- | ---
Declare variable | `$x = 10` | No type required
Use variable | `$x + 5` | Direct usage
Environment vars | `$env:PATH` | System variables
Automatic vars | `$PWD`, `$HOME`, `$PSVersionTable` | Built-in

## Using Variables

`$name = "John"`

`Write-Output "Hello $name"`

## Running Scripts

Method | Example
--- | ---
Direct run | `.\script.ps1`
With parameters | `.\script.ps1 -Name "John"`
Bypass policy | `powershell -ExecutionPolicy Bypass -File script.ps1`

## Parameters in Scripts

```powershell
param(
    [string]$Name,
    [int]$Age = 30
)

Write-Output "Name: $Name Age: $Age"
```

Call:

`.\script.ps1 -Name "Alice" -Age 25`

## Differences vs CMD/Bash

- Object-based (not text)
- Strong pipeline support
- Verb-Noun naming convention (`Get-Process`)
- Built-in error handling (`try/catch`)

## Things to Keep In Mind

- Execution policy may block scripts
- Paths require `.\` for local execution
- Case-insensitive by default
- Uses `.ps1` extension
- Better for structured data manipulation

