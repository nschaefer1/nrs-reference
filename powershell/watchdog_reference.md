
# Powershell Poor Man's Watchdog

This is an example script which can be ran to start up a specific process. The process PID is documented and reports are generated to give the RAM and CPU usage. More processes can be appended to this script if necessary.

```powershell
# =========================
# CONFIGURATION
# =========================

$basePath = "C:\path\to\your\project"               # ← edit with your project directory
$logPath = "$basePath\logs"                         # ← logs will be written here

$cloudflaredPath = "C:\path\to\cloudflared.exe"     # ← edit with your cloudflared executable
$tunnelName = "core-tunnel"                         # ← edit with your tunnel name

# =========================
# SETUP
# =========================

# Ensure log directory exists
if (!(Test-Path $logPath)) {
    New-Item -ItemType Directory -Path $logPath | Out-Null
}

Set-Location $basePath   # ← ensures relative paths behave correctly

# =========================
# START CLOUDFLARED
# =========================

$tunnel = Start-Process `
    -FilePath $cloudflaredPath `
    -ArgumentList "tunnel run $tunnelName" `
    -WorkingDirectory "." `
    -RedirectStandardOutput "$logPath\cloudflared.log" `
    -RedirectStandardError "$logPath\cloudflared_error.log" `
    -PassThru `
    -NoNewWindow

# Save PID for monitoring
$tunnel.Id | Out-File "$basePath\cloudflared.pid" -Force

Write-Output "Cloudflared started (PID: $($tunnel.Id))"

# =========================
# SIMPLE MONITOR (OPTIONAL)
# =========================

$cpuThreshold = 80       # ← percent (approximate)
$memoryThresholdMB = 500 # ← MB
$checkInterval = 5       # ← seconds

while ($true) {
    Start-Sleep -Seconds $checkInterval

    try {
        $p = Get-Process -Id $tunnel.Id -ErrorAction Stop
    } catch {
        Write-Output "Cloudflared process exited."
        break
    }

    # Memory usage
    $memoryMB = [math]::Round($p.WorkingSet64 / 1MB, 2)

    # CPU approximation (sampling)
    $cpu1 = $p.CPU
    Start-Sleep -Seconds 1
    $p2 = Get-Process -Id $tunnel.Id
    $cpu2 = $p2.CPU
    $cpuPercent = (($cpu2 - $cpu1) * 100) / $env:NUMBER_OF_PROCESSORS

    Write-Output "CPU: $([math]::Round($cpuPercent,2))% | Memory: $memoryMB MB"

    if ($memoryMB -gt $memoryThresholdMB -or $cpuPercent -gt $cpuThreshold) {
        Write-Output "Threshold exceeded. Stopping cloudflared."
        Stop-Process -Id $p.Id -Force
        break
    }
}
```
