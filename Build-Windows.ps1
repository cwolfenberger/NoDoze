$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = Join-Path $root '.venv-windows'
$pythonPath = Join-Path $venvPath 'Scripts\python.exe'

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw 'Python launcher not found. Install Python 3 for Windows from python.org and include the py launcher.'
}

Push-Location $root

try {
    if (-not (Test-Path -LiteralPath $pythonPath -PathType Leaf)) {
        py -3 -m venv $venvPath
        if ($LASTEXITCODE -ne 0) {
            throw 'Unable to create the Windows virtual environment.'
        }
    }

    & $pythonPath -m pip install --disable-pip-version-check -r (Join-Path $root 'requirements-windows.txt')
    if ($LASTEXITCODE -ne 0) {
        throw 'Unable to install Windows build dependencies.'
    }

    & $pythonPath -m PyInstaller `
        --noconfirm `
        --clean `
        --distpath (Join-Path $root 'dist\windows') `
        --workpath (Join-Path $root 'build\windows') `
        (Join-Path $root 'nodoze-windows.spec')

    if ($LASTEXITCODE -ne 0) {
        throw 'Windows executable build failed.'
    }

    Write-Host "Built $(Join-Path $root 'dist\windows\NoDoze.exe')"
}
finally {
    Pop-Location
}

