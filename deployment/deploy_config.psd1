@{
    # Application Basics
    AppName       = "ReflexPMT"
    AppRoot       = "C:\Inetpub\wwwroot\ReflexPMT"
    LogDir        = "C:\Inetpub\wwwroot\ReflexPMT\logs"
    BackupRoot    = "C:\Inetpub\wwwroot\ReflexPMT\backups"
    
    # IIS Configuration
    IISSiteName   = "Default Web Site"
    IISAppPath    = "/pmt"  # The sub-application path (e.g. https://server/pmt)
    
    # Backend Service Configuration
    ServiceName   = "reflex_service"
    ServicePort   = 8000
    
    # Dependencies
    SoftwareCache = "C:\Apps\Software"
    
    # Scheduled Task for Nightly Restart
    TaskName      = "ReflexPMT_NightlyRestart"
    TaskTime      = "00:00"
}
