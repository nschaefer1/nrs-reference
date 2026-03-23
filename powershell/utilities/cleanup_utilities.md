

# Powershell Cleanup Utilities

### __pycache__ cleanup

```powershell
# Recursively find and remove all __pycache__ folders from the current directory
Get-ChildItem -Path . -Recurse -Force -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force -Confirm:$false
Write-Output "All __pycache__ folders removed."
```