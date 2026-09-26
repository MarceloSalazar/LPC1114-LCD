<#
.SYNOPSIS
  Runs ERC/DRC and exports every manufacturing and documentation file for LPC1114-LCD.

.DESCRIPTION
  Outputs (relative to the repository root):
    hardware/fabrication/gerbers/            Gerber + Excellon drill files (JLCPCB settings)
    hardware/fabrication/LPC1114-LCD_JLCPCB.zip   Upload this file to jlcpcb.com
    hardware/fabrication/LPC1114-LCD_BOM.csv      Grouped bill of materials
    hardware/fabrication/LPC1114-LCD.step         3D model (for the 3D-printed case)
    docs/hardware/LPC1114-LCD_schematic.pdf
    docs/images/pcb_top.png, pcb_bottom.png

  Stops with a non-zero exit code if ERC or DRC report errors.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File hardware\scripts\export_fab.ps1
#>
param(
    [string]$KiCadCli = "C:\Program Files\KiCad\10.0\bin\kicad-cli.exe",
    [switch]$SkipRenders
)

$ErrorActionPreference = "Stop"
$hw   = Split-Path -Parent $PSScriptRoot
$root = Split-Path -Parent $hw
$name = "LPC1114-LCD"
$sch  = Join-Path $hw "$name.kicad_sch"
$pcb  = Join-Path $hw "$name.kicad_pcb"
$fab  = Join-Path $hw "fabrication"
$gbr  = Join-Path $fab "gerbers"
$docs = Join-Path $root "docs\hardware"
$img  = Join-Path $root "docs\images"

if (-not (Test-Path $KiCadCli)) { throw "kicad-cli not found at $KiCadCli (use -KiCadCli <path>)" }
foreach ($d in @($fab, $gbr, $docs, $img)) { New-Item -ItemType Directory -Force $d | Out-Null }

function Invoke-Cli {
    & $KiCadCli @args
    if ($LASTEXITCODE -ne 0) { throw "kicad-cli failed: $args" }
}

Write-Host "== ERC"
Invoke-Cli sch erc --exit-code-violations --output (Join-Path $fab "erc.rpt") $sch

Write-Host "== DRC (with schematic parity)"
Invoke-Cli pcb drc --schematic-parity --refill-zones --exit-code-violations --output (Join-Path $fab "drc.rpt") $pcb

Write-Host "== Gerbers + drill"
Remove-Item (Join-Path $gbr "*") -Force -ErrorAction SilentlyContinue
Invoke-Cli pcb export gerbers --output "$gbr\" `
    --layers "F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts" `
    --subtract-soldermask --no-x2 --no-netlist $pcb
Invoke-Cli pcb export drill --output "$gbr\" --format excellon --excellon-units mm `
    --excellon-zeros-format decimal --excellon-oval-format alternate --excellon-separate-th `
    --generate-map --map-format gerberx2 $pcb
$zip = Join-Path $fab "${name}_JLCPCB.zip"
Remove-Item $zip -Force -ErrorAction SilentlyContinue
Compress-Archive -Path (Join-Path $gbr "*") -DestinationPath $zip

Write-Host "== BOM"
Invoke-Cli sch export bom --output (Join-Path $fab "${name}_BOM.csv") `
    --fields "Reference,Value,Footprint,`${QUANTITY},MPN,Description" `
    --labels "Reference,Value,Footprint,Qty,MPN,Description" `
    --group-by "Value,Footprint" --exclude-dnp $sch

Write-Host "== Schematic PDF"
Invoke-Cli sch export pdf --output (Join-Path $docs "${name}_schematic.pdf") $sch

Write-Host "== STEP 3D model"
Invoke-Cli pcb export step --force --subst-models --output (Join-Path $fab "$name.step") $pcb

if (-not $SkipRenders) {
    Write-Host "== Renders"
    Invoke-Cli pcb render --side top --width 1600 --height 1520 --quality high --output (Join-Path $img "pcb_top.png") $pcb
    Invoke-Cli pcb render --side bottom --width 1600 --height 1520 --quality high --output (Join-Path $img "pcb_bottom.png") $pcb
}

Write-Host "Done. Upload $zip to https://jlcpcb.com"
