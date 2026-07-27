param(
  [switch]$InstallOptionalSystemTools
)

$ErrorActionPreference = "Stop"
Set-Location "C:\Users\Usuario\GitHub\estadoquecumple.github.io"

function Require-Command {
  param([string]$Name)
  if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
    throw "Falta la herramienta requerida: $Name"
  }
}

Require-Command git
Require-Command node
Require-Command npm
Require-Command python

Write-Host "Git:" (git --version)
Write-Host "Node:" (node --version)
Write-Host "npm:" (npm --version)
Write-Host "Python:" (python --version)

if ($InstallOptionalSystemTools) {
  if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    winget install --id Docker.DockerDesktop -e
    Write-Warning "Docker Desktop puede requerir reinicio y activación de WSL2."
  }
  if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    winget install --id GitHub.cli -e
  }
}

if (-not (Test-Path ".venv")) {
  python -m venv .venv
}

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& ".\.venv\Scripts\Activate.ps1"

python -m pip install --upgrade pip
python -m pip install -r requirements-data.txt

if (Test-Path "requirements-platform-core.txt") {
  python -m pip install -r requirements-platform-core.txt
} else {
  Write-Warning "Copie requirements-platform-core.txt al repositorio antes de continuar."
}

npm ci

Write-Host "Bootstrap terminado. No se instalaron secretos ni se crearon cuentas externas."
