$ErrorActionPreference = "Continue"

$computer = Get-CimInstance Win32_ComputerSystem
$cpu = Get-CimInstance Win32_Processor
$gpus = Get-CimInstance Win32_VideoController
$disks = Get-PSDrive -PSProvider FileSystem

$result = [ordered]@{
    Timestamp = (Get-Date).ToString("o")
    Computer = $env:COMPUTERNAME
    TotalRAM_GB = [math]::Round($computer.TotalPhysicalMemory / 1GB, 2)
    CPU = @($cpu | ForEach-Object {
        [ordered]@{
            Name = $_.Name
            Cores = $_.NumberOfCores
            LogicalProcessors = $_.NumberOfLogicalProcessors
        }
    })
    GPU = @($gpus | ForEach-Object {
        [ordered]@{
            Name = $_.Name
            AdapterRAM_GB = if ($_.AdapterRAM) {[math]::Round($_.AdapterRAM / 1GB, 2)} else {$null}
            DriverVersion = $_.DriverVersion
        }
    })
    Disks = @($disks | ForEach-Object {
        [ordered]@{
            Name = $_.Name
            Used_GB = [math]::Round($_.Used / 1GB, 2)
            Free_GB = [math]::Round($_.Free / 1GB, 2)
        }
    })
    NvidiaSMI = $null
}

if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) {
    $result.NvidiaSMI = (nvidia-smi --query-gpu=name,memory.total,memory.free,driver_version --format=csv,noheader)
}

New-Item -ItemType Directory -Force ".\reports" | Out-Null
$result | ConvertTo-Json -Depth 6 |
    Set-Content ".\reports\inventario-hardware-ia.json" -Encoding UTF8

$result | ConvertTo-Json -Depth 6
Write-Host "Guardado en reports/inventario-hardware-ia.json"
