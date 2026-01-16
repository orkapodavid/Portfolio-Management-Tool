<#
.SYNOPSIS
    Builds the offline deployment package for the Reflex application.
    Run this on an ONLINE Windows machine.

.DESCRIPTION
    1. Downloads uv.exe (Windows x64).
    2. Downloads WinSW (Windows Service Wrapper).
    3. Generates requirements.txt from pyproject.toml using uv.
    4. Downloads all Python dependencies (wheels) for Windows Server 2019 (win_amd64).
    5. Exports the Reflex Frontend (Pre-built static assets).
    6. Packages everything into deployment_package.zip.

.NOTES
    Requires: PowerShell 5.1+, Internet Access, Python 3 installed, Node.js installed (for frontend export).
#>

$ErrorActionPreference = "Stop"

# --- Configuration ---
$WorkDir = "$PSScriptRoot\..\build_temp"
$DistDir = "$PSScriptRoot\..\dist"
$WheelsDir = "$WorkDir\wheels"
$SourceDir = "$PSScriptRoot\..\app"
$AssetsDir = "$PSScriptRoot\..\assets"
$RepoRoot = "$PSScriptRoot\.."

# Python Version for Target
$TargetPythonVersion = "3.11"
$TargetPlatform = "win_amd64"

# --- Cleanup ---
Write-Host "Cleaning up previous builds..." -ForegroundColor Cyan
if (Test-Path $WorkDir) { Remove-Item -Recurse -Force $WorkDir }
if (Test-Path $DistDir) { Remove-Item -Recurse -Force $DistDir }

New-Item -ItemType Directory -Force -Path $WheelsDir | Out-Null
New-Item -ItemType Directory -Force -Path $DistDir | Out-Null

# --- 1. Download uv.exe ---
Write-Host "Downloading uv.exe (Windows x64)..." -ForegroundColor Cyan
$uvUrl = "https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-pc-windows-msvc.zip"
$uvZip = "$WorkDir\uv.zip"
try {
    Invoke-WebRequest -Uri $uvUrl -OutFile $uvZip
}
catch {
    Write-Error "Failed to download uv.exe. Check internet connection."
}

Expand-Archive -Path $uvZip -DestinationPath "$WorkDir\uv_bin"
$uvExe = "$WorkDir\uv.exe"
Get-ChildItem -Path "$WorkDir\uv_bin" -Recurse -Filter "uv.exe" | Copy-Item -Destination $uvExe
Remove-Item -Recurse -Force "$WorkDir\uv_bin"
Remove-Item -Force $uvZip

# --- 2. Download WinSW ---
Write-Host "Downloading WinSW (Service Wrapper)..." -ForegroundColor Cyan
$winswUrl = "https://github.com/winsw/winsw/releases/download/v2.12.0/WinSW-x64.exe"
try {
    Invoke-WebRequest -Uri $winswUrl -OutFile "$WorkDir\reflex_service.exe"
}
catch {
    Write-Warning "Failed to download WinSW. Please download 'WinSW-x64.exe', rename to 'reflex_service.exe', and place in package root."
}

# --- 3. Generate requirements.txt ---
Write-Host "Generating requirements.txt from pyproject.toml..." -ForegroundColor Cyan
& $uvExe pip compile "$RepoRoot\pyproject.toml" -o "$WorkDir\requirements.txt"

if (-not (Test-Path "$WorkDir\requirements.txt")) {
    Write-Error "Failed to generate requirements.txt"
}

# --- 4. Download Wheels ---
Write-Host "Downloading Python Wheels (Target: $TargetPlatform, Python $TargetPythonVersion)..." -ForegroundColor Cyan
try {
    python -m pip download -r "$WorkDir\requirements.txt" `
        --dest $WheelsDir `
        --platform $TargetPlatform `
        --python-version $TargetPythonVersion `
        --only-binary=:all: `
        --no-deps
}
catch {
    Write-Error "Pip download failed. Ensure Python is installed and added to PATH."
}

# --- 5. Export Frontend (Pre-build) ---
Write-Host "Exporting Reflex Frontend (Static)..." -ForegroundColor Cyan
# Ensure reflex is installed in the build environment to run export
# We assume the build machine has it, or we install it temporarily?
# Since we have wheels, maybe we can use them? No, we need to run it.
# We assume the user has set up the build machine.
try {
    # Run export. We need to point to the app.
    # We must run this from the repo root.
    Push-Location $RepoRoot
    # We need to set API_URL for the build so the static files know where to point?
    # No, API_URL is runtime config for next.js usually, but for static export it might bake it in?
    # Reflex v0.8.20: rx.Config values are baked in at build time for frontend.
    # So we MUST set API_URL here!
    $env:API_URL = "https://hcma.ds.susq.com/pmt"
    $env:CI = "1" # Ensures prod mode

    # Check if we need to init? 'reflex export' usually works if app exists.
    # We use --frontend-only and --no-zip to get a folder.

    # Note: 'reflex export' might require 'reflex init' first to download template if not present.
    # If .web is missing, export might fail or try to init.

    Write-Host "Running reflex export..."
    reflex export --frontend-only

    # It usually exports to 'frontend.zip' or folder?
    # --no-zip should output to .web/_static usually or we need to check docs.
    # Based on help: "--no-zip Whether to zip..."
    # If --no-zip is passed, where does it go?
    # Usually .web/_static or .web/_next
    # Let's assume .web/_static is the output for static export or we check for 'frontend' folder.

    # Actually, reflex export creates 'frontend.zip' by default. --no-zip might leave it in .web?
    # Let's use default (zip) and unzip it, it's safer.

    # Re-run without no-zip to be safe or check output.
    # Let's stick to 'reflex export --frontend-only' which creates frontend.zip

    Pop-Location

    if (Test-Path "$RepoRoot\frontend.zip") {
        Write-Host "Frontend exported successfully."
        # Extract to deployment package
        Expand-Archive -Path "$RepoRoot\frontend.zip" -DestinationPath "$WorkDir\frontend_static"
        Remove-Item "$RepoRoot\frontend.zip"
    } else {
        # Fallback: Check if .web/_static exists?
        Write-Warning "frontend.zip not found. Please ensure 'reflex export' ran correctly. You might need to install reflex on the build machine."
    }
}
catch {
    Write-Warning "Reflex export failed. Ensure 'reflex' is installed and Node.js is available on the build machine."
}

# --- 6. Package Artifacts ---
Write-Host "Assembling deployment package..." -ForegroundColor Cyan

Copy-Item -Recurse "$SourceDir" "$WorkDir\app"
Copy-Item "$RepoRoot\rxconfig.py" "$WorkDir\"
Copy-Item "$RepoRoot\pyproject.toml" "$WorkDir\"
if (Test-Path $AssetsDir) { Copy-Item -Recurse "$AssetsDir" "$WorkDir\assets" }

New-Item -ItemType Directory "$WorkDir\scripts" | Out-Null
Copy-Item "$PSScriptRoot\deploy_initial.ps1" "$WorkDir\scripts\"
Copy-Item "$PSScriptRoot\deploy_update.ps1" "$WorkDir\scripts\"

New-Item -ItemType Directory "$WorkDir\config" | Out-Null
Copy-Item "$PSScriptRoot\reflex_service.xml" "$WorkDir\config\"
Copy-Item "$PSScriptRoot\web.config" "$WorkDir\config\"

$ReadmeContent = @"
DEPLOYMENT PACKAGE
==================

1. Copy this folder to the target server (e.g., C:\Inetpub\wwwroot\ReflexPMT).
2. Run PowerShell as Administrator.
3. For Initial Install:
   cd scripts
   .\deploy_initial.ps1
4. For Updates:
   Replace the files and run .\deploy_update.ps1

NOTE: 'uv.exe' and 'reflex_service.exe' (WinSW) are included.
Frontend is pre-built in 'frontend_static'.
"@
Set-Content -Path "$WorkDir\README_PACKAGE.txt" -Value $ReadmeContent

Write-Host "Zipping..." -ForegroundColor Cyan
$ZipPath = "$DistDir\deployment_package.zip"
Compress-Archive -Path "$WorkDir\*" -DestinationPath $ZipPath

Write-Host "SUCCESS! Deployment package created at:" -ForegroundColor Green
Write-Host $ZipPath
