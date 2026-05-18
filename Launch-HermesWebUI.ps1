$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$startScript = Join-Path $repoRoot "start-remote.ps1"
$envFile = Join-Path $repoRoot ".env"
$defaultUrl = "http://127.0.0.1:8787"

if (-not (Test-Path $startScript)) {
    throw "Missing start script: $startScript"
}

$targetUrl = $defaultUrl
if (Test-Path $envFile) {
    $hostValue = "127.0.0.1"
    $portValue = "8787"
    Get-Content $envFile | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith("#") -or $line.IndexOf("=") -lt 1) {
            return
        }
        $parts = $line.Split("=", 2)
        $name = $parts[0].Trim()
        $value = $parts[1].Trim().Trim("'").Trim('"')
        switch ($name) {
            "HERMES_WEBUI_HOST" { if ($value) { $hostValue = $value } }
            "HERMES_WEBUI_PORT" { if ($value) { $portValue = $value } }
        }
    }
    if ($hostValue -eq "0.0.0.0") {
        $hostValue = "127.0.0.1"
    }
    $targetUrl = "http://$hostValue`:$portValue"
}

$running = $false
try {
    $health = Invoke-WebRequest -Uri "$targetUrl/health" -UseBasicParsing -TimeoutSec 2
    if ($health.StatusCode -eq 200) {
        $running = $true
    }
} catch {
}

if (-not $running) {
    Start-Process powershell.exe -ArgumentList @(
        "-NoExit",
        "-ExecutionPolicy", "Bypass",
        "-File", $startScript
    ) -WorkingDirectory $repoRoot | Out-Null
}

for ($i = 0; $i -lt 30; $i++) {
    try {
        $health = Invoke-WebRequest -Uri "$targetUrl/health" -UseBasicParsing -TimeoutSec 2
        if ($health.StatusCode -eq 200) {
            Start-Process $targetUrl | Out-Null
            exit 0
        }
    } catch {
    }
    Start-Sleep -Seconds 1
}

Start-Process $targetUrl | Out-Null
