<#
.SYNOPSIS
    Updates the Reflex application from a new package.

.DESCRIPTION
    1. Stops the Windows Service.
    2. Backs up current version.
    3. Overwrites application files.
    4. Updates dependencies (offline).
    5. Runs DB migrations.
    6. Updates frontend static files.
    7. Restarts the service.

.NOTES
    Run as Administrator.
#>

$ScriptDir = $PSScriptRoot
Import-Module "$ScriptDir\deploy_utils.psm1" -Force

$ErrorActionPreference = "Stop"
$PackageRoot = "$ScriptDir\.."

# --- Load Configuration ---
try {
    $Config = Get-DeployConfig
    Write-Host "Starting Update for $($Config.AppName)..." -ForegroundColor Cyan
}
catch {
    Write-Error "Failed to load configuration: $_"
    exit 1
}

# --- 1. Stop Service ---
Ensure-ServiceStopped -ServiceName $Config.ServiceName

# --- 3. Backup current version ---
$BackupConfigDir = if ($Config.BackupRoot) { $Config.BackupRoot } else { "$($Config.AppRoot)\backups" }
$BackupDir = "$BackupConfigDir\$(Get-Date -Format 'yyyyMMddHHmmss')"

Write-Log "Creating backup of current version..."
New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
Copy-Item "$($Config.AppRoot)\app" "$BackupDir\app" -Recurse -ErrorAction SilentlyContinue
Copy-Item "$($Config.AppRoot)\rxconfig.py" "$BackupDir\" -ErrorAction SilentlyContinue
Copy-Item "$($Config.AppRoot)\pyproject.toml" "$BackupDir\" -ErrorAction SilentlyContinue
Write-Log "Backup created at: $BackupDir"

# --- 4. Overwrite Code ---
Write-Log "Overwriting files..."
# Exclude items that should not be overwritten
$ExcludeItems = @("scripts", "*.db", ".venv", "wheels", "logs", "backups", "public")
Copy-Item "$PackageRoot\*" "$Config.AppRoot" -Recurse -Force -Exclude $ExcludeItems

# Update wheels folder
if (Test-Path "$PackageRoot\wheels") {
    New-Item -ItemType Directory -Force -Path "$($Config.AppRoot)\wheels" | Out-Null
    Copy-Item "$PackageRoot\wheels\*" "$($Config.AppRoot)\wheels\" -Recurse -Force
}

# --- 5. Update Dependencies ---
Write-Log "Updating dependencies..." "Cyan"
$uvSrc = "$($Config.AppRoot)\uv.exe"

if (-not (Test-Path $uvSrc)) {
    Write-ErrorLog "uv.exe not found at $uvSrc"
    exit 1
}

& $uvSrc pip install --python "$($Config.AppRoot)\.venv\Scripts\python.exe" --no-index --find-links "$($Config.AppRoot)\wheels" -r "$($Config.AppRoot)\requirements.txt" --upgrade

# --- 6. Migrations ---
Write-Log "Running Migrations..." "Cyan"
Set-Location $Config.AppRoot
$env:PATH = "$($Config.AppRoot)\.venv\Scripts;$env:PATH"
reflex db migrate

# --- 7. Update Frontend Static Files ---
Write-Log "Updating Frontend..." "Cyan"
if (Test-Path "$PackageRoot\frontend_static") {
    # Backup old public folder
    if (Test-Path "$($Config.AppRoot)\public") {
        Copy-Item "$($Config.AppRoot)\public" "$BackupDir\public" -Recurse -ErrorAction SilentlyContinue
        Remove-Item "$($Config.AppRoot)\public" -Recurse -Force
    }
    New-Item -ItemType Directory -Force -Path "$($Config.AppRoot)\public" | Out-Null
    Copy-Item "$PackageRoot\frontend_static\*" "$($Config.AppRoot)\public\" -Recurse -Force
    
    # Re-apply web.config
    Copy-Item "$($Config.AppRoot)\config\web.config" "$($Config.AppRoot)\public\web.config"
    Write-Log "Frontend updated."
}
else {
    Write-Log "No frontend_static in package. Frontend unchanged."
}

# --- 8. Restart Service and Verify ---
Ensure-ServiceStarted -ServiceName $Config.ServiceName

# Ensure nightly restart is configured (idempotent)
Ensure-ScheduledRestart -TaskName $Config.TaskName -ServiceName $Config.ServiceName -Time $Config.TaskTime

# --- 9. Health Check (Optional) ---
Write-Log "Performing health check..." "Cyan"
Start-Sleep -Seconds 3
try {
    $response = Invoke-WebRequest -Uri "http://localhost:$($Config.ServicePort)/ping" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Success "Backend health check passed"
    }
}
catch {
    Write-WarningLog "Health check failed. Backend may still be starting up. Check logs at $($Config.LogDir)"
}

# --- Finish ---
Write-Host ""
Write-Success "Update Complete!"
Write-Log "Rollback available at: $BackupDir"
Write-Log "To rollback, run deploy_rollback.ps1"
Write-Host ""

