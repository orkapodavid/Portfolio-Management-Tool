<#
.SYNOPSIS
    Rolls back to a previous deployment version.

.DESCRIPTION
    1. Stops the Windows Service.
    2. Lists available backups.
    3. Restores selected backup.
    4. Restarts the service.

.NOTES
    Run as Administrator.
    Backups are stored in C:\Inetpub\wwwroot\ReflexPMT\backups\
#>

$ErrorActionPreference = "Stop"

# --- Configuration ---
$AppName = "ReflexPMT"
$AppRoot = "C:\Inetpub\wwwroot\$AppName"
$ServiceName = "reflex_service"
$BackupRoot = "$AppRoot\backups"

Write-Host "Reflex PMT Rollback Utility" -ForegroundColor Cyan
Write-Host ""

# --- List Available Backups ---
if (-not (Test-Path $BackupRoot)) {
    Write-Error "No backups directory found at $BackupRoot"
}

$backups = Get-ChildItem $BackupRoot -Directory | Sort-Object Name -Descending
if ($backups.Count -eq 0) {
    Write-Error "No backups available in $BackupRoot"
}

Write-Host "Available Backups:" -ForegroundColor Yellow
for ($i = 0; $i -lt $backups.Count; $i++) {
    $backup = $backups[$i]
    $timestamp = $backup.Name
    # Parse timestamp: yyyyMMddHHmmss
    $year = $timestamp.Substring(0, 4)
    $month = $timestamp.Substring(4, 2)
    $day = $timestamp.Substring(6, 2)
    $hour = $timestamp.Substring(8, 2)
    $min = $timestamp.Substring(10, 2)
    $formatted = "$year-$month-$day $hour`:$min"
    
    Write-Host "  [$i] $formatted ($($backup.Name))"
}

Write-Host ""
$selection = Read-Host "Enter backup number to restore (or 'q' to quit)"

if ($selection -eq 'q') {
    Write-Host "Rollback cancelled."
    exit 0
}

$index = [int]$selection
if ($index -lt 0 -or $index -ge $backups.Count) {
    Write-Error "Invalid selection"
}

$selectedBackup = $backups[$index]
Write-Host ""
Write-Host "Selected backup: $($selectedBackup.Name)" -ForegroundColor Yellow
$confirm = Read-Host "Are you sure you want to rollback? (yes/no)"

if ($confirm -ne "yes") {
    Write-Host "Rollback cancelled."
    exit 0
}

# --- 1. Stop Service ---
$svc = Get-Service $ServiceName -ErrorAction SilentlyContinue
if ($svc -and $svc.Status -eq 'Running') {
    Write-Host "Stopping Service..."
    Stop-Service $ServiceName -Force
    $svc.WaitForStatus('Stopped', '00:00:30')
    Write-Host "[OK] Service stopped" -ForegroundColor Green
}

# --- 2. Restore Files ---
Write-Host "Restoring files from backup..."

# Restore app folder
if (Test-Path "$($selectedBackup.FullName)\app") {
    Remove-Item "$AppRoot\app" -Recurse -Force -ErrorAction SilentlyContinue
    Copy-Item "$($selectedBackup.FullName)\app" "$AppRoot\app" -Recurse
    Write-Host "  Restored: app/"
}

# Restore config files
if (Test-Path "$($selectedBackup.FullName)\rxconfig.py") {
    Copy-Item "$($selectedBackup.FullName)\rxconfig.py" "$AppRoot\" -Force
    Write-Host "  Restored: rxconfig.py"
}

if (Test-Path "$($selectedBackup.FullName)\pyproject.toml") {
    Copy-Item "$($selectedBackup.FullName)\pyproject.toml" "$AppRoot\" -Force
    Write-Host "  Restored: pyproject.toml"
}

# Restore frontend
if (Test-Path "$($selectedBackup.FullName)\public") {
    Remove-Item "$AppRoot\public" -Recurse -Force -ErrorAction SilentlyContinue
    Copy-Item "$($selectedBackup.FullName)\public" "$AppRoot\public" -Recurse
    Write-Host "  Restored: public/"
}

# --- 3. Restart Service ---
Write-Host "Starting Service..."
Start-Service $ServiceName

Start-Sleep -Seconds 5
$svc = Get-Service $ServiceName
if ($svc.Status -eq 'Running') {
    Write-Host "[OK] Service '$ServiceName' is running" -ForegroundColor Green
}
else {
    Write-Warning "Service status: $($svc.Status). Check logs."
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Rollback Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Rolled back to: $($selectedBackup.Name)"
