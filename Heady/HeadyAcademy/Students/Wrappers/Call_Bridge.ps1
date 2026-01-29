param([string]$Target, [string]$Action)
$BASE = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Write-Host "[BRIDGE] Establishing connection..."

if ($Target -eq "mcp_client") {
    python "$BASE\Tools\MCP\Client.py" $Action
} elseif ($Target -eq "warp") {
    python "$BASE\Tools\Network\Warp_Manager.py" $Action
} else {
    Write-Host ">> Starting MCP Server on Stdio..."
    python "$BASE\Tools\MCP\Server.py"
}
