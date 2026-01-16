<#
.SYNOPSIS
    Updates the Reflex application from a new package.

.DESCRIPTION
    1. Stops the Windows Service.
    2. Backups the database (if sqlite).
    3. Overwrites application files.
    4. Updates dependencies (offline).
    5. Runs DB migrations.
    6. Restarts the service.
#>

$ErrorActionPreference = "Stop"
$ScriptDir = $PSScriptRoot
$PackageRoot = "$ScriptDir\.."

# --- Configuration ---
$AppName = "ReflexPMT"
$AppRoot = "C:\Inetpub\wwwroot\$AppName"
$ServiceName = "reflex_service"

Write-Host "Starting Update for $AppName..." -ForegroundColor Cyan

# --- 1. Stop Service ---
if (Get-Service $ServiceName -ErrorAction SilentlyContinue) {
    Write-Host "Stopping Service..."
    Stop-Service $ServiceName -Force
}

# --- 2. Backup DB ---
# Assuming sqlite for now as user mentioned ".db".
$DbFile = "$AppRoot\app.db" # Default reflex db name?
if (Test-Path $DbFile) {
    $BackupName = "$DbFile.bak.$(Get-Date -Format 'yyyyMMddHHmmss')"
    Copy-Item $DbFile $BackupName
    Write-Host "Database backed up to $BackupName"
}

# --- 3. Overwrite Code ---
Write-Host "Overwriting files..."
Copy-Item "$PackageRoot\*" "$AppRoot" -Recurse -Force -Exclude "scripts", "app.db", ".venv", "wheels"
# Update wheels folder
Copy-Item "$PackageRoot\wheels\*" "$AppRoot\wheels\" -Recurse -Force

# --- 4. Update Dependencies ---
Write-Host "Updating dependencies..."
$uvSrc = "$AppRoot\uv.exe"
& $uvSrc pip install --no-index --find-links "$AppRoot\wheels" -r "$AppRoot\requirements.txt" --upgrade

# --- 5. Migrations ---
Write-Host "Running Migrations..."
Set-Location $AppRoot
$env:PATH = "$AppRoot\.venv\Scripts;$env:PATH"
# Ensure env vars are set correctly.
# If you have a .env file, python-dotenv (used in pyproject) should load it.
reflex db migrate

# --- 6. Restart Service ---
Write-Host "Starting Service..."
Start-Service $ServiceName

Write-Host "Update Complete!" -ForegroundColor Green
