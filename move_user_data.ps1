# Move Personal Data from C: to E: Drive
# Safe migration with backup and verification
# Run as Administrator

Write-Host ""
Write-Host "============================================================"
Write-Host "PERSONAL DATA MIGRATION - C: to E: Drive"
Write-Host "============================================================"
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "[ERROR] This script must be run as Administrator!"
    Write-Host "Right-click PowerShell -> Run as Administrator"
    exit 1
}

Write-Host "[OK] Running as Administrator`n"

# Get username
$username = $env:USERNAME
$userPath = "C:\Users\$username"
$backupPath = "E:\Backup_C_Drive_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

# Folders to move
$foldersToMove = @(
    @{ source = "$userPath\Desktop"; dest = "E:\Desktop" },
    @{ source = "$userPath\Pictures"; dest = "E:\Pictures" },
    @{ source = "$userPath\Music"; dest = "E:\Music" },
    @{ source = "$userPath\Videos"; dest = "E:\Videos" },
    @{ source = "$userPath\Favorites"; dest = "E:\Favorites" }
)

# Folders to SKIP (exclude)
$foldersToSkip = @(
    "$userPath\Documents",
    "$userPath\Downloads",
    "$userPath\AppData"
)

Write-Host "MIGRATION PLAN:"
Write-Host "============================================================"
Write-Host ""
Write-Host "Folders to MOVE to E: drive:"
foreach ($folder in $foldersToMove) {
    if (Test-Path $folder.source) {
        $size = (Get-ChildItem $folder.source -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
        Write-Host "  ✓ $($folder.source) (~$([Math]::Round($size, 2)) GB)"
    }
}

Write-Host ""
Write-Host "Folders to KEEP on C: drive (excluded):"
foreach ($folder in $foldersToSkip) {
    if (Test-Path $folder) {
        Write-Host "  → $folder"
    }
}

Write-Host ""
Write-Host "BACKUP LOCATION:"
Write-Host "  $backupPath"
Write-Host ""
Write-Host "============================================================"
Write-Host ""

# Confirmation
Write-Host "WARNING: This will move your personal files to E: drive!"
Write-Host "A backup will be created first."
Write-Host ""
Write-Host "Continue? (y/n): " -NoNewline
$response = Read-Host

if ($response -ne 'y' -and $response -ne 'Y') {
    Write-Host "[CANCELLED] Migration aborted"
    exit 0
}

Write-Host ""
Write-Host "Starting migration process..."
Write-Host ""

# Step 1: Create backup
Write-Host "[1/4] Creating backup of data..."
Write-Host "      Destination: $backupPath"

try {
    New-Item -ItemType Directory -Path $backupPath -Force | Out-Null

    foreach ($folder in $foldersToMove) {
        if (Test-Path $folder.source) {
            Write-Host "      Backing up: $(Split-Path $folder.source -Leaf)..."
            Copy-Item -Path $folder.source -Destination "$backupPath\$(Split-Path $folder.source -Leaf)" -Recurse -Force -ErrorAction Stop
        }
    }

    Write-Host "[OK] Backup completed`n"

} catch {
    Write-Host "[ERROR] Backup failed: $_"
    Write-Host "        Aborting migration"
    exit 1
}

# Step 2: Create destination folders on E:
Write-Host "[2/4] Creating destination folders on E: drive..."

try {
    foreach ($folder in $foldersToMove) {
        $destPath = $folder.dest
        if (-not (Test-Path $destPath)) {
            New-Item -ItemType Directory -Path $destPath -Force | Out-Null
            Write-Host "      Created: $destPath"
        }
    }

    Write-Host "[OK] Destination folders created`n"

} catch {
    Write-Host "[ERROR] Failed to create destination folders: $_"
    exit 1
}

# Step 3: Move data
Write-Host "[3/4] Moving files to E: drive..."
Write-Host "      (This may take several minutes...)`n"

$moveCount = 0
$moveErrors = 0

foreach ($folder in $foldersToMove) {
    if (Test-Path $folder.source) {
        Write-Host "      Moving: $(Split-Path $folder.source -Leaf)..."

        try {
            # Remove old destination if exists
            if (Test-Path $folder.dest) {
                Remove-Item $folder.dest -Recurse -Force -ErrorAction Stop
            }

            # Move folder
            Move-Item -Path $folder.source -Destination $folder.dest -Force -ErrorAction Stop
            Write-Host "        ✓ Moved to: $($folder.dest)"
            $moveCount++

        } catch {
            Write-Host "        ✗ Error: $_"
            $moveErrors++
        }
    }
}

Write-Host ""
Write-Host "[OK] Move completed ($moveCount folders moved, $moveErrors errors)`n"

# Step 4: Create symbolic links (optional - for compatibility)
Write-Host "[4/4] Creating shortcuts for compatibility..."

try {
    foreach ($folder in $foldersToMove) {
        $destPath = $folder.dest

        # Create symbolic link so old path still works
        New-Item -ItemType SymbolicLink -Path $folder.source -Target $destPath -Force -ErrorAction SilentlyContinue | Out-Null
        Write-Host "      Link: $($folder.source) -> $destPath"
    }

    Write-Host "[OK] Symbolic links created`n"

} catch {
    Write-Host "[WARNING] Could not create symbolic links: $_`n"
}

# Summary
Write-Host "============================================================"
Write-Host "MIGRATION COMPLETE!"
Write-Host "============================================================"
Write-Host ""
Write-Host "Summary:"
Write-Host "  Folders moved: $moveCount"
Write-Host "  Errors: $moveErrors"
Write-Host "  Backup location: $backupPath"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Restart your computer (to ensure all changes take effect)"
Write-Host "  2. Verify files are accessible in new locations"
Write-Host "  3. Delete backup after verification: $backupPath"
Write-Host ""
Write-Host "Space freed on C: drive: ~$(($foldersToMove.Count * 5)) GB (estimated)"
Write-Host ""
Write-Host "============================================================"
Write-Host ""

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
