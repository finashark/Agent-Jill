@echo off
chcp 65001 >nul
title 🤖 Auto Dashboard Generator - One Click Solution

echo.
echo ================================================================
echo 🤖 AUTO DASHBOARD GENERATOR - ONE CLICK SOLUTION
echo ================================================================
echo 📅 Starting at %date% %time%
echo.

echo 🔧 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python first.
    echo 💡 Download from: https://python.org
    pause
    exit /b 1
)

echo ✅ Python found!
echo.

echo 🚀 Running auto dashboard generator...
echo.

python auto_dashboard_generator.py

echo.
echo ================================================================
echo 🎉 Auto Dashboard Generator Completed!
echo ================================================================
echo.

pause