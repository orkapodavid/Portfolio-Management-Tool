<#
.SYNOPSIS
    Verifies all prerequisites for deploying the Reflex application on Windows Server 2019.

.DESCRIPTION
    Checks for required Windows features, IIS modules, and software availability.
    Uses centrally defined configuration in deploy_config.psd1.

.NOTES
    Run as Administrator.
#>

$ScriptDir = $PSScriptRoot
Import-Module "$ScriptDir\deploy_utils.psm1" -Force

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Reflex Deployment Prerequisites Check" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

try {
    $Config = Get-DeployConfig
    Write-Log "Configuration loaded." "Info"
}
catch {
    Write-ErrorLog "Failed to load configuration: $_"
    exit 1
}

$allPassed = $true

function Test-Prerequisite {
    param(
        [string]$Name,
        [scriptblock]$Test,
        [string]$FixInstructions
    )
    
    $result = & $Test
    if ($result) {
        Write-Success "[PASS] $Name"
        return $true
    }
    else {
        Write-ErrorLog "[FAIL] $Name"
        Write-Log "       Fix: $FixInstructions" "Yellow"
        return $false
    }
}

# --- Windows Features ---
Write-Log "Checking Windows Features..." "Cyan"
Write-Host ""

$requiredFeatures = @(
    @{Name = "Web-Server"; Display = "IIS Web Server" },
    @{Name = "Web-WebSockets"; Display = "WebSocket Protocol" },
    @{Name = "Web-Asp-Net45"; Display = "ASP.NET 4.5+" },
    @{Name = "Web-Mgmt-Console"; Display = "IIS Management Console" },
    @{Name = "Web-Mgmt-Tools"; Display = "IIS Management Tools" }
)

foreach ($feature in $requiredFeatures) {
    if (-not (Test-Prerequisite -Name $feature.Display -Test {
                $f = Get-WindowsFeature -Name $feature.Name -ErrorAction SilentlyContinue
                return ($f -and $f.Installed)
            } -FixInstructions "Install-WindowsFeature -Name $($feature.Name)")) {
        $allPassed = $false
    }
}

Write-Host ""

# --- IIS Modules ---
Write-Log "Checking IIS Modules..." "Cyan"
Write-Host ""

if (-not (Test-Prerequisite -Name "URL Rewrite Module" -Test {
            Test-Path "C:\Windows\System32\inetsrv\rewrite.dll"
        } -FixInstructions "Install from https://www.iis.net/downloads/microsoft/url-rewrite or use installer in $($Config.SoftwareCache)")) {
    $allPassed = $false
}

if (-not (Test-Prerequisite -Name "Application Request Routing (ARR)" -Test {
            Test-Path "C:\Program Files\IIS\Application Request Routing\requestRouter.dll"
        } -FixInstructions "Install from https://www.iis.net/downloads/microsoft/application-request-routing or use installer in $($Config.SoftwareCache)")) {
    $allPassed = $false
}

Write-Host ""

# --- Software Cache ---
Write-Log "Checking Software Cache ($($Config.SoftwareCache))..." "Cyan"
Write-Host ""

if (-not (Test-Prerequisite -Name "Software Cache Directory" -Test {
            Test-Path $Config.SoftwareCache
        } -FixInstructions "Create directory: New-Item -ItemType Directory -Path '$($Config.SoftwareCache)'")) {
    $allPassed = $false
}
else {
    # Only check files if cache dir exists
    if (-not (Test-Prerequisite -Name "uv.exe (Python Package Manager)" -Test {
                Test-Path (Join-Path $Config.SoftwareCache "uv.exe")
            } -FixInstructions "Download uv.exe and place in $($Config.SoftwareCache)")) {
        $allPassed = $false
    }
    
    if (-not (Test-Prerequisite -Name "WinSW (Windows Service Wrapper)" -Test {
                $null -ne (Get-ChildItem "$($Config.SoftwareCache)\WinSW*.exe" -ErrorAction SilentlyContinue | Select-Object -First 1)
            } -FixInstructions "Download WinSW-x64.exe and place in $($Config.SoftwareCache)")) {
        $allPassed = $false
    }
    
    if (-not (Test-Prerequisite -Name "Node.js (node.exe)" -Test {
                Test-Path (Join-Path $Config.SoftwareCache "node.exe")
            } -FixInstructions "Download node.exe (win-x64) and place in $($Config.SoftwareCache)")) {
        $allPassed = $false
    }
}

Write-Host ""

# --- Python ---
Write-Log "Checking Python Installation..." "Cyan"
Write-Host ""

if (-not (Test-Prerequisite -Name "Python 3.11+" -Test {
            try {
                $version = python --version 2>&1
                return $version -match "Python 3\.(1[1-9]|[2-9][0-9])"
            }
            catch { return $false }
        } -FixInstructions "Install Python 3.11+")) {
    $allPassed = $false
}

Write-Host ""

# --- Network/Ports ---
Write-Log "Checking Port Availability..." "Cyan"
Write-Host ""

if (-not (Test-Prerequisite -Name "Port $($Config.ServicePort) (Backend)" -Test {
            return Test-PortAvailability -Port $Config.ServicePort
        } -FixInstructions "Port $($Config.ServicePort) is in use. Stop the conflicting service.")) {
    $allPassed = $false
}

if (-not (Test-Prerequisite -Name "Port 80 (IIS HTTP)" -Test {
            $listener = Get-NetTCPConnection -LocalPort 80 -ErrorAction SilentlyContinue
            if ($listener) {
                $process = Get-Process -Id $listener[0].OwningProcess -ErrorAction SilentlyContinue
                return ($process.ProcessName -eq "System" -or $process.ProcessName -eq "w3wp")
            }
            return $true
        } -FixInstructions "Port 80 is used by a non-IIS process.")) {
    $allPassed = $false
}

Write-Host ""

# --- IIS Configuration ---
Write-Log "Checking IIS Configuration..." "Cyan"
Write-Host ""

if (-not (Test-Prerequisite -Name "Default Web Site Running" -Test {
            try {
                $site = Get-Website -Name $Config.IISSiteName -ErrorAction SilentlyContinue
                return ($site -and $site.State -eq "Started")
            }
            catch { return $false }
        } -FixInstructions "Start IIS Site: Start-Website -Name '$($Config.IISSiteName)'")) {
    $allPassed = $false
}

Write-Host ""

# --- Summary ---
Write-Host "============================================" -ForegroundColor Cyan
if ($allPassed) {
    Write-Success "  ALL PREREQUISITES PASSED!"
    Write-Success "  You can proceed with deployment."
    exit 0
}
else {
    Write-ErrorLog "  SOME PREREQUISITES FAILED"
    Write-Log "  Please address the issues above before deployment." "Yellow"
    exit 1
}
Write-Host "============================================" -ForegroundColor Cyan

