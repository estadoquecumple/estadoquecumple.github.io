$ErrorActionPreference = "Stop"
Set-Location "C:\Users\Usuario\GitHub\estadoquecumple.github.io"

Write-Host "=== Preparación Python 3.12 para Laboratorio V4 ==="

if (Get-Command deactivate -ErrorAction SilentlyContinue) {
    deactivate
}

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw "No se encontró el lanzador 'py'. Instale Python 3.12 con: winget install -e --id Python.Python.3.12"
}

$python312 = & py -3.12 -c "import sys; print(sys.executable)" 2>$null
if ($LASTEXITCODE -ne 0 -or -not $python312) {
    throw "Python 3.12 no está instalado. Ejecute: winget install -e --id Python.Python.3.12 ; cierre y vuelva a abrir la terminal."
}

Write-Host "Python 3.12 encontrado en: $python312"

if (Test-Path ".venv") {
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $backup = ".venv-python314-backup-$stamp"
    Rename-Item ".venv" $backup
    Write-Host "Entorno anterior conservado como $backup"
}

& py -3.12 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& ".\.venv\Scripts\Activate.ps1"

python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-data.txt
python -m pip install -r requirements-platform-core.txt

python -c "import sys, duckdb, pyarrow, h3, great_expectations, networkx, rapidfuzz; print(sys.version); print('Dependencias Python V4: OK')"

Write-Host ""
Write-Host "Entorno Python V4 listo."
Write-Host "Ejecute después:"
Write-Host "  npm explain esbuild"
Write-Host "  npm explain sharp"
Write-Host "  npm approve-scripts esbuild sharp"
Write-Host "  npm audit --omit=dev"
Write-Host "  npm audit"
