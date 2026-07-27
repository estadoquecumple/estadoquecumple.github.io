$ErrorActionPreference = "Stop"
Set-Location "C:\Users\Usuario\GitHub\estadoquecumple.github.io"

if (Get-Command deactivate -ErrorAction SilentlyContinue) {
    deactivate
}

Write-Host "Entornos encontrados:"
Get-ChildItem -Directory -Filter ".venv*" | ForEach-Object {
    $python = Join-Path $_.FullName "Scripts\python.exe"
    if (Test-Path $python) {
        Write-Host ""
        Write-Host $_.Name
        & $python -c "import sys, importlib.util; print('Python', sys.version.split()[0]); print('duckdb=', importlib.util.find_spec('duckdb') is not None); print('great_expectations=', importlib.util.find_spec('great_expectations') is not None)"
    }
}

$working = ".venv-python314-backup"
$workingPython = Join-Path $working "Scripts\python.exe"

if (-not (Test-Path $workingPython)) {
    throw "No se encontró $working. Revise la salida anterior y seleccione manualmente el entorno Python 3.12 con duckdb=True."
}

$check = & $workingPython -c "import sys, importlib.util; print(sys.version_info[:2] == (3,12) and importlib.util.find_spec('duckdb') is not None)"
if ($check -ne "True") {
    throw "$working no es el entorno Python 3.12 funcional esperado."
}

if (Test-Path ".venv") {
    Remove-Item ".venv" -Recurse -Force
}

Rename-Item $working ".venv"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& ".\.venv\Scripts\Activate.ps1"

python -c "import duckdb, pyarrow, h3, great_expectations, networkx, rapidfuzz; print('Entorno restaurado: OK')"
Write-Host "No se hizo ningún pago ni se activó ningún servicio externo."
