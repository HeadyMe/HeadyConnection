# HEADY ACADEMY VAULT SETUP (PowerShell Version)
$VAULT_ENV = ".\Vault\.env"
Write-Host "=== HEADY ACADEMY VAULT SETUP ==="

if (!(Test-Path $VAULT_ENV)) { New-Item -ItemType File -Path $VAULT_ENV -Force | Out-Null }

function Invest-Key {
    param([string]$KeyName)
    $val = Read-Host "Enter $KeyName (Leave empty to skip)" -AsSecureString
    $plainVal = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($val))
    if ($plainVal) {
        $content = Get-Content $VAULT_ENV | Where-Object { $_ -notmatch "^$KeyName=" }
        $content += "$KeyName=$plainVal"
        $content | Set-Content $VAULT_ENV
        Write-Host ">> $KeyName secured."
    }
}

Invest-Key "GEMINI_API_KEY"
Invest-Key "OPENAI_API_KEY"
Invest-Key "YANDEX_API_KEY"
Invest-Key "GITHUB_TOKEN"
Invest-Key "HEADY_SIGNATURE_KEY"
Invest-Key "CLOUDFLARE_API_TOKEN"
Invest-Key "ADMIN_PASSWORD_HASH"
Invest-Key "LEDGER_MASTER_KEY"
Invest-Key "WARP_LICENSE_KEY"
Write-Host "Vault Setup Complete."
