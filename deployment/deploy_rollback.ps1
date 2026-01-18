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
#>

$ScriptDir = $PSScriptRoot
Import-Module "$ScriptDir\deploy_utils.psm1" -Force

$ErrorActionPreference = "Stop"

# --- Load Configuration ---
try {
    $Config = Get-DeployConfig
    Write-Host "Reflex PMT Rollback Utility" -ForegroundColor Cyan
}
catch {
    Write-Error "Failed to load configuration: $_"
    exit 1
}

$BackupRoot = if ($Config.BackupRoot) { $Config.BackupRoot } else { "$($Config.AppRoot)\backups" }

# --- List Available Backups ---
if (-not (Test-Path $BackupRoot)) {
    Write-ErrorLog "No backups directory found at $BackupRoot"
    exit 1
}

$backups = Get-ChildItem $BackupRoot -Directory | Sort-Object Name -Descending
if ($backups.Count -eq 0) {
    Write-ErrorLog "No backups available in $BackupRoot"
    exit 1
}

Write-Log "Available Backups:" "Yellow"
for ($i = 0; $i -lt $backups.Count; $i++) {
    $backup = $backups[$i]
    $timestamp = $backup.Name
    # Parse timestamp: yyyyMMddHHmmss if possible
    try {
        if ($timestamp.Length -ge 14) {
            $year = $timestamp.Substring(0, 4)
            $month = $timestamp.Substring(4, 2)
            $day = $timestamp.Substring(6, 2)
            $hour = $timestamp.Substring(8, 2)
            $min = $timestamp.Substring(10, 2)
            $formatted = "$year-$month-$day $hour`:$min"
            Write-Host "  [$i] $formatted ($($backup.Name))"
        }
        else {
            Write-Host "  [$i] $($backup.Name)"
        }
    }
    catch {
        Write-Host "  [$i] $($backup.Name)"
    }
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
Write-Log "Selected backup: $($selectedBackup.Name)" "Yellow"
$confirm = Read-Host "Are you sure you want to rollback? (yes/no)"

if ($confirm -ne "yes") {
    Write-Host "Rollback cancelled."
    exit 0
}

# --- 1. Stop Service ---
Ensure-ServiceStopped -ServiceName $Config.ServiceName

# --- 2. Restore Files ---
Write-Log "Restoring files from backup..."

# Restore app folder
if (Test-Path "$($selectedBackup.FullName)\app") {
    Remove-Item "$($Config.AppRoot)\app" -Recurse -Force -ErrorAction SilentlyContinue
    Copy-Item "$($selectedBackup.FullName)\app" "$($Config.AppRoot)\app" -Recurse
    Write-Log "  Restored: app/"
}

# Restore config files
if (Test-Path "$($selectedBackup.FullName)\rxconfig.py") {
    Copy-Item "$($selectedBackup.FullName)\rxconfig.py" "$($Config.AppRoot)\" -Force
    Write-Log "  Restored: rxconfig.py"
}

if (Test-Path "$($selectedBackup.FullName)\pyproject.toml") {
    Copy-Item "$($selectedBackup.FullName)\pyproject.toml" "$($Config.AppRoot)\" -Force
    Write-Log "  Restored: pyproject.toml"
}

# Restore frontend
if (Test-Path "$($selectedBackup.FullName)\public") {
    Remove-Item "$($Config.AppRoot)\public" -Recurse -Force -ErrorAction SilentlyContinue
    Copy-Item "$($selectedBackup.FullName)\public" "$($Config.AppRoot)\public" -Recurse
    Write-Log "  Restored: public/"
}

# --- 3. Restart Service ---
Ensure-ServiceStarted -ServiceName $Config.ServiceName

Write-Host ""
Write-Success "Rollback Complete!"
Write-Log "Rolled back to: $($selectedBackup.Name)"

