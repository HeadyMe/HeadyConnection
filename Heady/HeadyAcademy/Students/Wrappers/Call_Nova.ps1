param([string]$Path = ".")
$BASE = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Write-Host "[NOVA] Scanning for gaps..."
python "$BASE\Tools\Gap_Scanner.py" $Path
