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

Write-Host "== BOM (full, grouped)"
$bomAll = Join-Path $fab "${name}_BOM.csv"
Invoke-Cli sch export bom --output $bomAll `
    --fields "Reference,Value,Footprint,`${QUANTITY},LCSC,Assembly,MPN,Description" `
    --labels "Reference,Value,Footprint,Qty,LCSC,Assembly,MPN,Description" `
    --group-by "Value,Footprint,LCSC" --exclude-dnp $sch
$rows = Import-Csv $bomAll

Write-Host "== JLCPCB PCBA: BOM + CPL (only parts with an LCSC number)"
$jlc = $rows | Where-Object { $_.LCSC -ne "" }
$jlc | ForEach-Object {
    [pscustomobject]@{
        "Comment"      = $_.Value
        "Designator"   = $_.Reference
        "Footprint"    = ($_.Footprint -split ":")[-1]
        "LCSC Part #"  = $_.LCSC
    }
} | Export-Csv -NoTypeInformation -Encoding UTF8 (Join-Path $fab "${name}_JLCPCB_BOM.csv")
# expand "R5-R7" style ranges and comma lists into individual designators
$jlcRefs = @{}
foreach ($r in $jlc) {
    foreach ($tok in ($r.Reference -split ",")) {
        $tok = $tok.Trim()
        if ($tok -match '^([A-Z]+)(\d+)-[A-Z]*(\d+)$') {
            for ($i = [int]$Matches[2]; $i -le [int]$Matches[3]; $i++) { $jlcRefs["$($Matches[1])$i"] = $true }
        } else { $jlcRefs[$tok] = $true }
    }
}
$posRaw = Join-Path $fab "pos_all.csv"
Invoke-Cli pcb export pos --output $posRaw --format csv --units mm --side front $pcb
Import-Csv $posRaw | Where-Object { $jlcRefs.ContainsKey($_.Ref) } | ForEach-Object {
    [pscustomobject]@{
        "Designator" = $_.Ref
        "Mid X"      = "$($_.PosX)mm"
        "Mid Y"      = "$($_.PosY)mm"
        "Layer"      = "Top"
        "Rotation"   = $_.Rot
    }
} | Export-Csv -NoTypeInformation -Encoding UTF8 (Join-Path $fab "${name}_JLCPCB_CPL.csv")
Remove-Item $posRaw -ErrorAction SilentlyContinue
$missing = $jlcRefs.Keys | Where-Object { -not ((Import-Csv (Join-Path $fab "${name}_JLCPCB_CPL.csv")).Designator -contains $_) }
if ($missing) { throw "CPL is missing placements for: $($missing -join ', ')" }

Write-Host "== Parts to hand-solder (Assembly=USER)"
$rows | Where-Object { $_.Assembly -eq "USER" } |
    Select-Object Reference, Value, Footprint, Qty, MPN, Description |
    Export-Csv -NoTypeInformation -Encoding UTF8 (Join-Path $fab "${name}_hand_solder.csv")

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
