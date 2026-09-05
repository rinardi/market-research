# Data Migration Guide - C: to E: Drive

Move personal data from C: drive to E: drive safely with automatic backup.

---

## ⚠️ IMPORTANT - READ FIRST

- **Backup:** Automatic backup created before any files are moved
- **Time:** Migration may take 30-60 minutes depending on data size
- **Restart:** Computer will need to restart after migration
- **Space:** Frees up ~5-15 GB on C: drive

---

## 🚀 STEP-BY-STEP GUIDE

### Step 1: Verify Space on E: Drive

Before starting, check E: drive has enough space:

```powershell
# Check E: drive space
Get-Volume -DriveLetter E | Select-Object Size, SizeRemaining
```

**Minimum required:** 20 GB free on E: drive

---

### Step 2: Run Migration Script

**Option A: Via File Explorer (Recommended)**

1. Open File Explorer
2. Navigate to: `D:\market-research\`
3. Find: `move_user_data.ps1`
4. Right-click → "Run with PowerShell"
5. Click "Run anyway" if prompted

**Option B: Via PowerShell (Advanced)**

```powershell
# Open PowerShell as Administrator
# Right-click Start Menu → Windows PowerShell (Admin)

cd D:\market-research
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\move_user_data.ps1
```

---

### Step 3: Confirm Migration

Script will show:

```
MIGRATION PLAN:
============================================================

Folders to MOVE to E: drive:
  ✓ C:\Users\Rinardi Rusman\Desktop (~2.50 GB)
  ✓ C:\Users\Rinardi Rusman\Pictures (~3.20 GB)
  ✓ C:\Users\Rinardi Rusman\Music (~1.80 GB)
  ✓ C:\Users\Rinardi Rusman\Videos (~5.60 GB)
  ✓ C:\Users\Rinardi Rusman\Favorites (~0.05 GB)

Folders to KEEP on C: drive (excluded):
  → C:\Users\Rinardi Rusman\Documents
  → C:\Users\Rinardi Rusman\Downloads
  → C:\Users\Rinardi Rusman\AppData

Continue? (y/n):
```

**Type `y` and press Enter to proceed**

---

### Step 4: Wait for Completion

Script will do:

1. **[1/4] Backup** - Creates backup of all data (~15 GB)
   - Destination: `E:\Backup_C_Drive_[timestamp]`
   - Time: 10-20 minutes

2. **[2/4] Create Folders** - Creates destination folders on E:
   - Time: < 1 minute

3. **[3/4] Move Files** - Moves files from C: to E:
   - Time: 10-30 minutes
   - Shows progress for each folder

4. **[4/4] Create Links** - Creates shortcuts for compatibility
   - Time: < 1 minute

---

### Step 5: Restart Computer

After script completes:

```
Next steps:
  1. Restart your computer
  2. Verify files are accessible
  3. Delete backup after verification
```

**Restart now:**
```powershell
Restart-Computer
```

Or manually: Start Menu → Power → Restart

---

## ✅ AFTER MIGRATION

### Verify Everything Works

1. **Check C: drive space:**
   ```powershell
   Get-Volume -DriveLetter C | Select-Object Size, SizeRemaining
   ```
   Should show ~10-15 GB more free space

2. **Verify files on E: drive:**
   - Open File Explorer
   - Check E: drive contains:
     - Desktop folder
     - Pictures folder
     - Music folder
     - Videos folder
     - Favorites folder

3. **Test file access:**
   - Click Desktop icon → Should work
   - Click Pictures → Should work
   - etc.

4. **Check backup:**
   - Location: `E:\Backup_C_Drive_[timestamp]`
   - Contains copies of all moved files

### Delete Backup (When Confident)

After verifying everything works for 1-2 days:

```powershell
# Delete backup to free space
Remove-Item -Path "E:\Backup_C_Drive_*" -Recurse -Force
```

Or manually delete via File Explorer.

---

## 🐛 TROUBLESHOOTING

### "Not enough space on E: drive"
- Free up space on E: (delete unnecessary files)
- Minimum needed: Total size of moved folders + 10 GB

### "Access Denied" when moving files
- Some files might be in use
- Close all applications
- Try again or restart and run script

### Files not accessible after migration
- Computer might need restart
- Run: `Restart-Computer`
- Check symbolic links were created

### Need to undo migration
1. Delete files on E: drive
2. Restore from backup: `E:\Backup_C_Drive_*`
3. Move back to C: drive

---

## 📊 EXPECTED RESULTS

**Before Migration:**
- C: drive: 96% full (~105 GB used)
- E: drive: Some free space

**After Migration:**
- C: drive: ~85% full (~85 GB used) ← 20 GB freed
- E: drive: Used space + backup + moved folders

---

## 🔒 SAFETY CHECKLIST

- [ ] Backup created automatically
- [ ] E: drive has 20+ GB free
- [ ] All applications closed
- [ ] Restart after migration
- [ ] Verify files accessible
- [ ] Keep backup for 1-2 days
- [ ] Delete backup after confirmation

---

## 📞 IF SOMETHING GOES WRONG

1. **Script crashes:**
   - Don't panic - backup is safe on E:
   - Run script again or restore manually

2. **Files not found:**
   - Check E: drive backup location
   - Or restore from backup
   - Or contact support

3. **Computer won't start:**
   - Restart in Safe Mode
   - Check symbolic links created properly
   - Restore from backup if needed

---

## ✨ NEXT STEPS

After successful migration:

1. **Free space on C: drive:**
   - Run Disk Cleanup
   - Run Disk Defragmentation

2. **Optimize E: drive:**
   - Move more data if needed
   - Keep backup folder

3. **Monitor:**
   - Check disk space regularly
   - Adjust if C: fills up again

---

**Ready? Run the script!** 🚀

```powershell
D:\market-research\move_user_data.ps1
```
