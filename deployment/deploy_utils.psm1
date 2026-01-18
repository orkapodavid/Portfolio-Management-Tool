# deploy_utils.psm1

# --- Logging ---

function Write-Log {
    param(
        [Parameter(Mandatory = $true)] [string]$Message,
        [string]$Level = "Info",
        [string]$Color = "White"
    )

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $formattedMsg = "[$timestamp] [$Level] $Message"

    switch ($Level) {
        "Info" { $params = @{ ForegroundColor = if ($Color -eq "White") { "Cyan" } else { $Color } } }
        "Success" { $params = @{ ForegroundColor = "Green" } }
        "Warning" { $params = @{ ForegroundColor = "Yellow" } }
        "Error" { $params = @{ ForegroundColor = "Red" } }
        Default { $params = @{ ForegroundColor = $Color } }
    }

    Write-Host $formattedMsg @params
}

function Write-Success { param([string]$Message) Write-Log -Message $Message -Level "Success" }
function Write-WarningLog { param([string]$Message) Write-Log -Message $Message -Level "Warning" }
function Write-ErrorLog { param([string]$Message) Write-Log -Message $Message -Level "Error" }

# --- Configuration ---

function Get-DeployConfig {
    param([string]$ConfigPath = "$PSScriptRoot\deploy_config.psd1")
    
    if (-not (Test-Path $ConfigPath)) {
        throw "Configuration file not found at $ConfigPath"
    }
    
    return Import-PowerShellDataFile -Path $ConfigPath
}

# --- Checks ---

function Test-PortAvailability {
    param([int]$Port)
    $listener = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
    return $null -eq $listener
}

# --- Service Management ---

function Ensure-ServiceStopped {
    param([string]$ServiceName)
    
    $svc = Get-Service $ServiceName -ErrorAction SilentlyContinue
    if ($svc -and $svc.Status -eq 'Running') {
        Write-Log "Stopping service '$ServiceName'..."
        Stop-Service $ServiceName -Force
        $svc.WaitForStatus('Stopped', '00:00:30')
        Write-Success "Service '$ServiceName' stopped."
    }
    elseif (-not $svc) {
        Write-Log "Service '$ServiceName' does not exist." "Warning"
    }
    else {
        Write-Log "Service '$ServiceName' is already stopped."
    }
}

function Ensure-ServiceStarted {
    param([string]$ServiceName)
    
    Write-Log "Starting service '$ServiceName'..."
    Start-Service $ServiceName
    Start-Sleep -Seconds 5
    
    $svc = Get-Service $ServiceName -ErrorAction SilentlyContinue
    if ($svc.Status -eq 'Running') {
        Write-Success "Service '$ServiceName' is running."
    }
    else {
        throw "Failed to start service '$ServiceName'. Status: $($svc.Status)"
    }
}

function Install-WinSWService {
    param(
        [string]$ExePath,
        [bool]$UninstallExisting = $true
    )
    
    if (-not (Test-Path $ExePath)) {
        throw "Service executable not found at $ExePath"
    }

    if ($UninstallExisting) {
        # Simple check if service exists via the exe's configuration (WinSW convention) or just try uninstall
        # We'll assume the caller handled stopping the service if it's the same name, 
        # but WinSW requires the xml config to verify id. 
        # Safe approach: Just run uninstall, ignore error if not installed.
        Write-Log "Attempting to uninstall existing service wrapper entry..."
        try {
            Start-Process -FilePath $ExePath -ArgumentList "uninstall" -Wait -NoNewWindow -ErrorAction Stop
        }
        catch {
            Write-Log "Uninstall passed (service might not have existed)." "Info"
        }
        Start-Sleep -Seconds 2
    }

    Write-Log "Installing service..."
    $proc = Start-Process -FilePath $ExePath -ArgumentList "install" -Wait -NoNewWindow -PassThru
    
    if ($proc.ExitCode -eq 0) {
        Write-Success "Service installed successfully."
    }
    else {
        throw "Service installation failed with exit code $($proc.ExitCode)."
    }
}

# --- Scheduled Task ---

function Ensure-ScheduledRestart {
    param(
        [string]$TaskName,
        [string]$ServiceName,
        [string]$Time = "00:00"
    )

    Write-Log "Configuring nightly restart task '$TaskName' at $Time..."

    $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -Command Restart-Service -Name $ServiceName -Force"
    $trigger = New-ScheduledTaskTrigger -Daily -At $Time
    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

    # Check if exists
    $existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    
    if ($existing) {
        Write-Log "Updating existing scheduled task..."
        Set-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings | Out-Null
    }
    else {
        Write-Log "Creating new scheduled task..."
        Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings | Out-Null
    }
    
    Write-Success "Scheduled task '$TaskName' configured."
}

# --- IIS ---

function Ensure-IISApp {
    param(
        [string]$SiteName,
        [string]$AppPath,
        [string]$PhysicalPath
    )

    Import-Module WebAdministration -ErrorAction Stop
    
    # Clean AppPath (remove leading slash for some cmdlets if needed, but New-WebApplication handles /name)
    $AppName = $AppPath.TrimStart("/")

    $app = Get-WebApplication -Site $SiteName -Name $AppName -ErrorAction SilentlyContinue

    if (-not $app) {
        Write-Log "Creating IIS Application '$AppPath' under '$SiteName'..."
        New-WebApplication -Name $AppName -Site $SiteName -PhysicalPath $PhysicalPath | Out-Null
        Write-Success "IIS Application created."
    }
    else {
        $currentPath = $app.PhysicalPath
        if ($currentPath -ne $PhysicalPath) {
            Write-Log "Updating IIS Application path from '$currentPath' to '$PhysicalPath'..."
            Set-ItemProperty "IIS:\Sites\$SiteName\$AppName" -Name physicalPath -Value $PhysicalPath
            Write-Success "IIS Application path updated."
        }
        else {
            Write-Log "IIS Application already exists with correct path."
        }
    }
}
