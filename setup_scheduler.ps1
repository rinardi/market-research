# Setup Windows Task Scheduler for Daily Market Analysis
# Run as Administrator

Write-Host "=================================================="
Write-Host "SWING TRADING - SETUP TASK SCHEDULER"
Write-Host "=================================================="
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "[ERROR] This script must be run as Administrator!"
    Write-Host "Right-click PowerShell -> Run as Administrator"
    exit 1
}

Write-Host "[OK] Running as Administrator`n"

# Define task parameters
$taskName = "SwingTradingDailyAnalysis"
$taskDescription = "Run daily swing trading market analysis and update dashboard"
$scriptPath = "D:\market-research\run_daily_analysis.bat"
$taskTime = "09:00"

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "[WARNING] Task '$taskName' already exists"
    Write-Host "Unregistering existing task..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "[OK] Existing task removed"
}

Write-Host ""
Write-Host "Creating new scheduled task..."
Write-Host "  Name: $taskName"
Write-Host "  Schedule: Daily at $taskTime AM"
Write-Host "  Action: Run $scriptPath"
Write-Host ""

# Create task trigger (9:00 AM daily)
$trigger = New-ScheduledTaskTrigger -Daily -At $taskTime

# Create task action
$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$scriptPath`""

# Create task settings
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Register the task
try {
    Register-ScheduledTask -TaskName $taskName `
        -Trigger $trigger `
        -Action $action `
        -Settings $settings `
        -Description $taskDescription `
        -RunLevel Highest `
        -Force

    Write-Host "[OK] Task created successfully!"
    Write-Host ""
    Write-Host "Task Details:"
    $task = Get-ScheduledTask -TaskName $taskName
    Write-Host "  Name: $($task.TaskName)"
    Write-Host "  Status: $($task.State)"
    Write-Host "  Next Run: Will run at $taskTime AM tomorrow"

} catch {
    Write-Host "[ERROR] Failed to create task: $_"
    exit 1
}

Write-Host ""
Write-Host "==================================================="
Write-Host "SCHEDULER SETUP COMPLETE!"
Write-Host "==================================================="
Write-Host ""
Write-Host "Your market analysis will run automatically every"
Write-Host "day at $taskTime AM!"
Write-Host ""
Write-Host "Dashboard location:"
Write-Host "  file:///D:/market-research/dashboard.html"
Write-Host ""
Write-Host "To view/manage tasks:"
Write-Host "  1. Open Task Scheduler (taskschd.msc)"
Write-Host "  2. Look for '$taskName' under Task Scheduler Library"
Write-Host "  3. Right-click to run manually or modify settings"
Write-Host ""
Write-Host "To disable/enable:"
Write-Host "  Disable:  Disable-ScheduledTask -TaskName '$taskName'"
Write-Host "  Enable:   Enable-ScheduledTask -TaskName '$taskName'"
Write-Host "  Remove:   Unregister-ScheduledTask -TaskName '$taskName'"
Write-Host ""
Write-Host "==================================================="
Write-Host ""

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
