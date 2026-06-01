param(
    [string]$ExecutablePath = (Join-Path $PSScriptRoot '..\dist\windows\NoDoze.exe')
)

$ErrorActionPreference = 'Stop'
$ExecutablePath = [System.IO.Path]::GetFullPath($ExecutablePath)

function Stop-ProcessTree {
    param([int]$ProcessId)

    $children = @(Get-CimInstance Win32_Process -Filter "ParentProcessId = $ProcessId")
    foreach ($child in $children) {
        Stop-ProcessTree -ProcessId $child.ProcessId
    }

    Stop-Process -Id $ProcessId -Force -ErrorAction SilentlyContinue
}

if (-not (Test-Path -LiteralPath $ExecutablePath -PathType Leaf)) {
    throw "Executable not found: $ExecutablePath"
}

$existingProcesses = @(Get-Process -Name 'NoDoze' -ErrorAction SilentlyContinue)
if ($existingProcesses.Count -gt 0) {
    throw 'Close any running NoDoze instances before running this smoke test.'
}

$process = Start-Process -FilePath $ExecutablePath -PassThru

try {
    Start-Sleep -Seconds 4
    $process.Refresh()

    if ($process.HasExited) {
        throw "NoDoze exited during startup with code $($process.ExitCode)."
    }

    Write-Host "NoDoze remained running after startup (PID $($process.Id))."
}
finally {
    Stop-ProcessTree -ProcessId $process.Id
}
