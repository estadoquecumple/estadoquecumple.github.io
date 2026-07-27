$ErrorActionPreference = "Continue"

Write-Host "=== Sistema ==="
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber

Write-Host "`n=== WSL ==="
wsl --version
wsl --status
wsl -l -v

Write-Host "`n=== Contenedores ==="
if (Get-Command podman -ErrorAction SilentlyContinue) {
    podman --version
    podman machine list
    podman info
    podman compose version
} elseif (Get-Command docker -ErrorAction SilentlyContinue) {
    docker --version
    docker compose version
    docker info
} else {
    Write-Warning "No se encontró Podman ni Docker."
}

Write-Host "`n=== Lenguajes ==="
node --version
npm --version
& ".\.venv\Scripts\python.exe" --version
git --version
gh --version

Write-Host "`n=== Disco ==="
Get-PSDrive -PSProvider FileSystem |
    Select-Object Name,
        @{N='UsadoGB';E={[math]::Round($_.Used/1GB,1)}},
        @{N='LibreGB';E={[math]::Round($_.Free/1GB,1)}}

Write-Host "`n=== Git ==="
git branch --show-current
git status --short --branch
