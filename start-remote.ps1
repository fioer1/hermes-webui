$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$envFile = Join-Path $repoRoot ".env"
$venvPython = Join-Path $repoRoot ".venv\\Scripts\\python.exe"

if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith("#") -or $line.IndexOf("=") -lt 1) {
            return
        }
        $parts = $line.Split("=", 2)
        $name = $parts[0].Trim()
        $value = $parts[1].Trim().Trim("'").Trim('"')
        Set-Item -Path "Env:$name" -Value $value
    }
}

if (-not (Test-Path $venvPython)) {
    throw "Missing virtualenv python: $venvPython"
}

Push-Location $repoRoot
try {
    & $venvPython "server.py"
}
finally {
    Pop-Location
}
