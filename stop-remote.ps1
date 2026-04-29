$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$targetPython = (Join-Path $repoRoot ".venv\\Scripts\\python.exe").ToLowerInvariant()

Get-CimInstance Win32_Process |
    Where-Object {
        $_.ExecutablePath -and $_.ExecutablePath.ToLowerInvariant() -eq $targetPython -and $_.CommandLine -match "server\\.py"
    } |
    ForEach-Object {
        Stop-Process -Id $_.ProcessId -Force
    }
