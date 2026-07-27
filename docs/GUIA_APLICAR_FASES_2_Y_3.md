# Guía para aplicar las Fases 2 y 3 del Laboratorio Territorial V4

## Advertencia

El paquete V4 original puede extraerse para conservarlo como referencia, pero sus prompts de Fase 2 y Fase 3 quedaron desactualizados respecto de las decisiones posteriores:

- mencionan Great Expectations, aunque la Fase 1 migró a Pandera;
- incluyen MinIO como opción, aunque se decidió una ruta totalmente gratuita y abierta;
- incluyen proveedores de IA comerciales;
- no incorporan la corrección de seguridad y publicación de la Fase 1;
- no distinguen claramente backend local, backend público y modo degradado de GitHub Pages.

Use los prompts actualizados de este paquete.

## Orden obligatorio

1. Preparar documentos.
2. Verificar WSL 2 y un motor de contenedores.
3. Ejecutar Codex para Fase 2.
4. Auditar, probar, fusionar y publicar el código de Fase 2.
5. Levantar localmente API, PostgreSQL/PostGIS, worker y bóveda.
6. Solo después ejecutar Codex para Fase 3.
7. No ejecutar ambos Codex simultáneamente.

## Extracción

Desde PowerShell:

```powershell
cd C:\Users\Usuario\GitHub\estadoquecumple.github.io

$paquete = Get-ChildItem "$env:USERPROFILE\Downloads" `
  -Filter "PAQUETE_FASES_2_Y_3_ACTUALIZADO*.zip" |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1

if (-not $paquete) {
  throw "No se encontró PAQUETE_FASES_2_Y_3_ACTUALIZADO*.zip en Descargas."
}

$destino = "$env:TEMP\estadoquecumple-fases-2-3"
Remove-Item $destino -Recurse -Force -ErrorAction SilentlyContinue
Expand-Archive $paquete.FullName $destino -Force

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& "$destino\preparar-documentos-fases-2-3.ps1" -SourceDirectory $destino
```

## Limpieza previa

Mueva cualquier informe no rastreado:

```powershell
$externo = "$env:USERPROFILE\Desktop\estadoquecumple-reportes"
New-Item -ItemType Directory -Force $externo | Out-Null

Get-ChildItem .\reports -Filter "npm-audit-*.json" -ErrorAction SilentlyContinue |
  Where-Object { (git ls-files --error-unmatch $_.FullName 2>$null) -eq $null } |
  Move-Item -Destination $externo -Force

git status --short --branch
```

No continúe si hay modificaciones desconocidas.

## Motor de contenedores recomendado

Para mantener una ruta gratuita y de código abierto, use Podman Desktop.

Antes de instalar:

```powershell
wsl --version
wsl --status
wsl -l -v
```

Si WSL no está instalado, abra PowerShell como administrador:

```powershell
wsl --install
```

Reinicie Windows cuando lo solicite.

Instalación de Podman Desktop:

```powershell
winget install -e --id RedHat.Podman-Desktop
```

Después de completar el asistente de Podman Desktop:

```powershell
podman --version
podman machine list
podman info
podman compose version
```

Docker Desktop puede usarse si ya está instalado y su licencia resulta aplicable, pero el proyecto no dependerá de él.

## Fase 2

Pegue en Codex el contenido completo de:

`docs/PROMPT_CODEX_V4_FASE_2_BACKEND_LOCAL_GRATUITO.md`

No copie fragmentos TypeScript, SQL o YAML directamente en PowerShell.

## Fase 3

Solo después de cerrar Fase 2, pegue:

`docs/PROMPT_CODEX_V4_FASE_3_GRAFO_OPTIMIZACION_IA_LOCAL.md`

Antes, ejecute:

```powershell
.\inventario-hardware-ia.ps1
```

Conserve el resultado para que Codex no descargue un modelo superior a la capacidad del equipo.
