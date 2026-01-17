<#
.SYNOPSIS
    Verifies all prerequisites for deploying the Reflex application on Windows Server 2019.

.DESCRIPTION
    Checks for required Windows features, IIS modules, and software availability.
    Run this BEFORE attempting deployment to identify any missing components.

.NOTES
    Run as Administrator.
    All required binaries should be in C:\Apps\Software
#>

param(
    [string]$SoftwareCache = "C:\Apps\Software"
)

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Reflex Deployment Prerequisites Check" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$allPassed = $true

function Test-Prerequisite {
    param(
        [string]$Name,
        [scriptblock]$Test,
        [string]$FixInstructions
    )
    
    $result = & $Test
    if ($result) {
        Write-Host "[PASS] $Name" -ForegroundColor Green
        return $true
    }
    else {
        Write-Host "[FAIL] $Name" -ForegroundColor Red
        Write-Host "       Fix: $FixInstructions" -ForegroundColor Yellow
        return $false
    }
}

# --- Windows Features ---
Write-Host "Checking Windows Features..." -ForegroundColor Cyan
Write-Host ""

$requiredFeatures = @(
    @{Name = "Web-Server"; Display = "IIS Web Server" },
    @{Name = "Web-WebSockets"; Display = "WebSocket Protocol" },
    @{Name = "Web-Asp-Net45"; Display = "ASP.NET 4.5+" },
    @{Name = "Web-Mgmt-Console"; Display = "IIS Management Console" },
    @{Name = "Web-Mgmt-Tools"; Display = "IIS Management Tools" }
)

foreach ($feature in $requiredFeatures) {
    $result = Test-Prerequisite -Name $feature.Display -Test {
        $f = Get-WindowsFeature -Name $feature.Name -ErrorAction SilentlyContinue
        return ($f -and $f.Installed)
    } -FixInstructions "Install-WindowsFeature -Name $($feature.Name)"
    
    if (-not $result) { $allPassed = $false }
}

Write-Host ""

# --- IIS Modules ---
Write-Host "Checking IIS Modules..." -ForegroundColor Cyan
Write-Host ""

$result = Test-Prerequisite -Name "URL Rewrite Module" -Test {
    Test-Path "C:\Windows\System32\inetsrv\rewrite.dll"
} -FixInstructions "Install from https://www.iis.net/downloads/microsoft/url-rewrite or use installer in $SoftwareCache"
if (-not $result) { $allPassed = $false }

$result = Test-Prerequisite -Name "Application Request Routing (ARR)" -Test {
    Test-Path "C:\Program Files\IIS\Application Request Routing\requestRouter.dll"
} -FixInstructions "Install from https://www.iis.net/downloads/microsoft/application-request-routing or use installer in $SoftwareCache"
if (-not $result) { $allPassed = $false }

Write-Host ""

# --- Software Cache ---
Write-Host "Checking Software Cache ($SoftwareCache)..." -ForegroundColor Cyan
Write-Host ""

$result = Test-Prerequisite -Name "Software Cache Directory" -Test {
    Test-Path $SoftwareCache
} -FixInstructions "Create directory: New-Item -ItemType Directory -Path '$SoftwareCache'"
if (-not $result) { $allPassed = $false }

if (Test-Path $SoftwareCache) {
    $result = Test-Prerequisite -Name "uv.exe (Python Package Manager)" -Test {
        Test-Path (Join-Path $SoftwareCache "uv.exe")
    } -FixInstructions "Download uv.exe from https://github.com/astral-sh/uv/releases and place in $SoftwareCache"
    if (-not $result) { $allPassed = $false }
    
    $result = Test-Prerequisite -Name "WinSW (Windows Service Wrapper)" -Test {
        $null -ne (Get-ChildItem "$SoftwareCache\WinSW*.exe" -ErrorAction SilentlyContinue | Select-Object -First 1)
    } -FixInstructions "Download WinSW-x64.exe from https://github.com/winsw/winsw/releases and place in $SoftwareCache"
    if (-not $result) { $allPassed = $false }
    
    $result = Test-Prerequisite -Name "Node.js (node.exe)" -Test {
        Test-Path (Join-Path $SoftwareCache "node.exe")
    } -FixInstructions "Download node.exe from https://nodejs.org/dist/ (win-x64) and place in $SoftwareCache"
    if (-not $result) { $allPassed = $false }
}

Write-Host ""

# --- Python ---
Write-Host "Checking Python Installation..." -ForegroundColor Cyan
Write-Host ""

$result = Test-Prerequisite -Name "Python 3.11+" -Test {
    try {
        $version = python --version 2>&1
        return $version -match "Python 3\.(1[1-9]|[2-9][0-9])"
    }
    catch {
        return $false
    }
} -FixInstructions "Install Python 3.11+ from https://www.python.org/downloads/ or use embedded Python from $SoftwareCache"
if (-not $result) { $allPassed = $false }

Write-Host ""

# --- Network/Ports ---
Write-Host "Checking Port Availability..." -ForegroundColor Cyan
Write-Host ""

$result = Test-Prerequisite -Name "Port 8000 (Backend)" -Test {
    $listener = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
    return ($null -eq $listener)
} -FixInstructions "Port 8000 is in use. Stop the conflicting service or configure a different port."
if (-not $result) { $allPassed = $false }

$result = Test-Prerequisite -Name "Port 80 (IIS HTTP)" -Test {
    $listener = Get-NetTCPConnection -LocalPort 80 -ErrorAction SilentlyContinue
    # Port 80 should be used by IIS (System process)
    if ($listener) {
        $process = Get-Process -Id $listener[0].OwningProcess -ErrorAction SilentlyContinue
        return ($process.ProcessName -eq "System" -or $process.ProcessName -eq "w3wp")
    }
    return $true
} -FixInstructions "Port 80 is used by a non-IIS process. Check with: Get-NetTCPConnection -LocalPort 80"
if (-not $result) { $allPassed = $false }

Write-Host ""

# --- IIS Configuration ---
Write-Host "Checking IIS Configuration..." -ForegroundColor Cyan
Write-Host ""

$result = Test-Prerequisite -Name "Default Web Site Running" -Test {
    try {
        Import-Module WebAdministration -ErrorAction Stop
        $site = Get-Website -Name "Default Web Site" -ErrorAction SilentlyContinue
        return ($site -and $site.State -eq "Started")
    }
    catch {
        return $false
    }
} -FixInstructions "Start IIS: Start-Website -Name 'Default Web Site'"
if (-not $result) { $allPassed = $false }

Write-Host ""

# --- Summary ---
Write-Host "============================================" -ForegroundColor Cyan
if ($allPassed) {
    Write-Host "  ALL PREREQUISITES PASSED!" -ForegroundColor Green
    Write-Host "  You can proceed with deployment." -ForegroundColor Green
}
else {
    Write-Host "  SOME PREREQUISITES FAILED" -ForegroundColor Red
    Write-Host "  Please address the issues above before deployment." -ForegroundColor Yellow
}
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Return exit code for automation
if ($allPassed) {
    exit 0
}
else {
    exit 1
}
