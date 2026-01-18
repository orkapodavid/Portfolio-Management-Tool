<#
.SYNOPSIS
    Updates the Reflex application from a new package.

.DESCRIPTION
    1. Stops the Windows Service.
    2. Overwrites application files.
    3. Updates dependencies (offline).
    4. Runs DB migrations.
    5. Updates frontend static files.
    6. Restarts the service and verifies.

    NOTE: Database (MS SQL) is hosted externally. Backup is managed separately.

.NOTES
    Run as Administrator.
    Ensure the new deployment package is unzipped to the package root.
#>

$ErrorActionPreference = "Stop"
$ScriptDir = $PSScriptRoot
$PackageRoot = "$ScriptDir\.."

# --- Configuration ---
$AppName = "ReflexPMT"
$AppRoot = "C:\Inetpub\wwwroot\$AppName"
$ServiceName = "reflex_service"
$LogDir = "$AppRoot\logs"

Write-Host "Starting Update for $AppName..." -ForegroundColor Cyan

# --- 1. Stop Service ---
$svc = Get-Service $ServiceName -ErrorAction SilentlyContinue
if ($svc) {
    if ($svc.Status -eq 'Running') {
        Write-Host "Stopping Service..."
        Stop-Service $ServiceName -Force
        # Wait for service to fully stop
        $svc.WaitForStatus('Stopped', '00:00:30')
        Write-Host "[OK] Service stopped" -ForegroundColor Green
    }
    else {
        Write-Host "Service already stopped (status: $($svc.Status))"
    }
}
else {
    Write-Warning "Service '$ServiceName' not found. Continuing with update..."
}

# --- 3. Backup current version (for rollback) ---
$BackupDir = "$AppRoot\backups\$(Get-Date -Format 'yyyyMMddHHmmss')"
Write-Host "Creating backup of current version..."
New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
Copy-Item "$AppRoot\app" "$BackupDir\app" -Recurse -ErrorAction SilentlyContinue
Copy-Item "$AppRoot\rxconfig.py" "$BackupDir\" -ErrorAction SilentlyContinue
Copy-Item "$AppRoot\pyproject.toml" "$BackupDir\" -ErrorAction SilentlyContinue
Write-Host "Backup created at: $BackupDir"

# --- 4. Overwrite Code ---
Write-Host "Overwriting files..."
# Exclude items that should not be overwritten
$ExcludeItems = @("scripts", "*.db", ".venv", "wheels", "logs", "backups", "public")
Copy-Item "$PackageRoot\*" "$AppRoot" -Recurse -Force -Exclude $ExcludeItems

# Update wheels folder (merge new wheels)
if (Test-Path "$PackageRoot\wheels") {
    New-Item -ItemType Directory -Force -Path "$AppRoot\wheels" | Out-Null
    Copy-Item "$PackageRoot\wheels\*" "$AppRoot\wheels\" -Recurse -Force
}

# --- 5. Update Dependencies ---
Write-Host "Updating dependencies..." -ForegroundColor Cyan
$uvSrc = "$AppRoot\uv.exe"

# Verify uv.exe exists
if (-not (Test-Path $uvSrc)) {
    Write-Error "uv.exe not found at $uvSrc"
}

# Use explicit python path for venv targeting
& $uvSrc pip install --python "$AppRoot\.venv\Scripts\python.exe" --no-index --find-links "$AppRoot\wheels" -r "$AppRoot\requirements.txt" --upgrade

# --- 6. Migrations ---
Write-Host "Running Migrations..." -ForegroundColor Cyan
Set-Location $AppRoot
$env:PATH = "$AppRoot\.venv\Scripts;$env:PATH"
# Ensure env vars are set correctly.
# python-dotenv (if used in pyproject) should load from .env file
reflex db migrate

# --- 7. Update Frontend Static Files ---
Write-Host "Updating Frontend..." -ForegroundColor Cyan
if (Test-Path "$PackageRoot\frontend_static") {
    # Backup old public folder
    if (Test-Path "$AppRoot\public") {
        Copy-Item "$AppRoot\public" "$BackupDir\public" -Recurse -ErrorAction SilentlyContinue
        Remove-Item "$AppRoot\public" -Recurse -Force
    }
    New-Item -ItemType Directory -Force -Path "$AppRoot\public" | Out-Null
    Copy-Item "$PackageRoot\frontend_static\*" "$AppRoot\public\" -Recurse -Force
    # Re-apply web.config
    Copy-Item "$AppRoot\config\web.config" "$AppRoot\public\web.config"
    Write-Host "Frontend updated."
}
else {
    Write-Host "No frontend_static in package. Frontend unchanged."
}

# --- 8. Restart Service and Verify ---
Write-Host "Starting Service..." -ForegroundColor Cyan
Start-Service $ServiceName

# Wait and verify service started successfully
Start-Sleep -Seconds 5
$svc = Get-Service $ServiceName
if ($svc.Status -eq 'Running') {
    Write-Host "[OK] Service '$ServiceName' is running" -ForegroundColor Green
}
else {
    Write-Error "Service '$ServiceName' failed to start (status: $($svc.Status)). Check logs at $LogDir"
}

# --- 9. Health Check (Optional) ---
Write-Host "Performing health check..." -ForegroundColor Cyan
Start-Sleep -Seconds 3
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/ping" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "[OK] Backend health check passed" -ForegroundColor Green
    }
}
catch {
    Write-Warning "Health check failed. Backend may still be starting up. Check logs at $LogDir"
}

# --- Finish ---
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Update Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Rollback available at: $BackupDir"
Write-Host "To rollback: Stop service, restore files from backup, start service"
