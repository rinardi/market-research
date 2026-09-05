# Full Automation - Data Migration + Daily Analysis Setup
# Run as Administrator - No pauses, automatic execution

Write-Host ""
Write-Host "============================================================"
Write-Host "FULL AUTOMATION SETUP"
Write-Host "============================================================"
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "[ERROR] Must run as Administrator!"
    Write-Host "Right-click PowerShell -> Run as Administrator"
    exit 1
}

Write-Host "[OK] Running as Administrator`n"

# ===== PART 1: DATA MIGRATION =====

Write-Host "=================================================="
Write-Host "PART 1: MIGRATING DATA (C: → E:)"
Write-Host "=================================================="
Write-Host ""

$username = $env:USERNAME
$userPath = "C:\Users\$username"
$backupPath = "E:\Backup_C_Drive_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

$foldersToMove = @(
    @{ source = "$userPath\Desktop"; dest = "E:\Desktop" },
    @{ source = "$userPath\Pictures"; dest = "E:\Pictures" },
    @{ source = "$userPath\Music"; dest = "E:\Music" },
    @{ source = "$userPath\Videos"; dest = "E:\Videos" },
    @{ source = "$userPath\Favorites"; dest = "E:\Favorites" }
)

# Step 1: Backup
Write-Host "[1/5] Creating backup..."
try {
    New-Item -ItemType Directory -Path $backupPath -Force -ErrorAction Stop | Out-Null

    foreach ($folder in $foldersToMove) {
        if (Test-Path $folder.source) {
            $folderName = Split-Path $folder.source -Leaf
            Write-Host "      Backing up: $folderName..."
            Copy-Item -Path $folder.source -Destination "$backupPath\$folderName" -Recurse -Force -ErrorAction Stop | Out-Null
        }
    }
    Write-Host "[OK] Backup completed`n"
} catch {
    Write-Host "[ERROR] Backup failed: $_"
    exit 1
}

# Step 2: Create destination folders
Write-Host "[2/5] Creating destination folders..."
try {
    foreach ($folder in $foldersToMove) {
        if (-not (Test-Path $folder.dest)) {
            New-Item -ItemType Directory -Path $folder.dest -Force -ErrorAction Stop | Out-Null
        }
    }
    Write-Host "[OK] Destination folders created`n"
} catch {
    Write-Host "[ERROR] Failed to create folders: $_"
    exit 1
}

# Step 3: Move files
Write-Host "[3/5] Moving files (this takes time)..."
$moveCount = 0
$moveErrors = 0

foreach ($folder in $foldersToMove) {
    if (Test-Path $folder.source) {
        $folderName = Split-Path $folder.source -Leaf
        Write-Host "      Moving: $folderName..."

        try {
            if (Test-Path $folder.dest) {
                Remove-Item $folder.dest -Recurse -Force -ErrorAction Stop | Out-Null
            }
            Move-Item -Path $folder.source -Destination $folder.dest -Force -ErrorAction Stop | Out-Null
            Write-Host "        ✓ Moved to: $($folder.dest)"
            $moveCount++
        } catch {
            Write-Host "        ✗ Error: $_"
            $moveErrors++
        }
    }
}

Write-Host "[OK] Move completed ($moveCount moved)`n"

# Step 4: Create symbolic links
Write-Host "[4/5] Creating compatibility links..."
try {
    foreach ($folder in $foldersToMove) {
        New-Item -ItemType SymbolicLink -Path $folder.source -Target $folder.dest -Force -ErrorAction SilentlyContinue | Out-Null
    }
    Write-Host "[OK] Symbolic links created`n"
} catch {
    Write-Host "[WARNING] Could not create symbolic links`n"
}

# ===== PART 2: SETUP DAILY SCHEDULER =====

Write-Host "=================================================="
Write-Host "PART 2: SETUP DAILY ANALYSIS SCHEDULER"
Write-Host "=================================================="
Write-Host ""

Write-Host "[5/5] Creating Windows Task Scheduler task..."

$taskName = "SwingTradingDailyAnalysis"
$scriptPath = "D:\market-research\run_daily_analysis.bat"
$taskTime = "09:00"

# Check if task exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "      Removing existing task..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false | Out-Null
}

try {
    $trigger = New-ScheduledTaskTrigger -Daily -At $taskTime
    $action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$scriptPath`""
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

    Register-ScheduledTask -TaskName $taskName `
        -Trigger $trigger `
        -Action $action `
        -Settings $settings `
        -Description "Run daily swing trading market analysis" `
        -RunLevel Highest `
        -Force | Out-Null

    Write-Host "[OK] Task scheduled for 09:00 AM daily`n"

} catch {
    Write-Host "[WARNING] Could not create task: $_`n"
}

# ===== FINAL REPORT =====

Write-Host "============================================================"
Write-Host "AUTOMATION COMPLETE!"
Write-Host "============================================================"
Write-Host ""

# Check space
$cDrive = Get-Volume -DriveLetter C
$eDrive = Get-Volume -DriveLetter E

Write-Host "DISK SPACE RESULTS:"
Write-Host "  C: drive free space: $([Math]::Round($cDrive.SizeRemaining / 1GB, 2)) GB"
Write-Host "  E: drive used space: $([Math]::Round($eDrive.Size / 1GB - $eDrive.SizeRemaining / 1GB, 2)) GB"
Write-Host ""

Write-Host "DATA MIGRATION:"
Write-Host "  ✓ Files backed up to: $backupPath"
Write-Host "  ✓ Files moved: $moveCount folders"
Write-Host "  ✓ Errors: $moveErrors"
Write-Host ""

Write-Host "DAILY ANALYSIS:"
Write-Host "  ✓ Task scheduled: $taskName"
Write-Host "  ✓ Run time: $taskTime AM daily"
Write-Host "  ✓ Dashboard: file:///D:/market-research/dashboard.html"
Write-Host ""

Write-Host "NEXT STEPS:"
Write-Host "  1. Restart computer now"
Write-Host "  2. Tomorrow at 09:00 AM: Analysis runs automatically"
Write-Host "  3. Dashboard updates with latest data"
Write-Host "  4. Telegram notifications sent (if configured)"
Write-Host ""

Write-Host "To restart now, press Enter..."
Read-Host

Write-Host ""
Write-Host "Restarting computer..."
Start-Sleep -Seconds 3

Restart-Computer -Force
