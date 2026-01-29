$BASE = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "$BASE\Tools\Daemons\Natural_Observer.py"
