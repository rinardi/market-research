@echo off
REM Daily Market Analysis Automation Script
REM Run this every morning at 09:00 AM via Windows Task Scheduler

echo.
echo ============================================================
echo SWING TRADING - DAILY ANALYSIS
echo ============================================================
echo Starting at: %date% %time%
echo.

REM Change to project directory
cd /d D:\market-research

REM Activate virtual environment
call D:\hpc-env\Scripts\activate.bat

REM Run analysis
echo [1/3] Running market analysis...
python main_analysis.py
if errorlevel 1 (
    echo [ERROR] Analysis failed
    exit /b 1
)

echo.
echo [2/3] Syncing dashboard with real data...
python sync_dashboard.py
if errorlevel 1 (
    echo [WARNING] Dashboard sync failed (continuing...)
)

echo.
echo [3/3] Sending Telegram notifications...
python update_dashboard.py
if errorlevel 1 (
    echo [WARNING] Telegram notifications skipped (Telegram not configured)
)

echo.
echo ============================================================
echo ANALYSIS COMPLETE
echo ============================================================
echo Dashboard: file:///D:/market-research/dashboard.html
echo Completed at: %date% %time%
echo ============================================================
echo.

REM Keep window open to see output (remove this for silent mode)
pause
