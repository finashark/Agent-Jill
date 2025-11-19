# 🤖 Auto Dashboard Generator - PowerShell Version
# One Click Solution for Creating Trading Dashboard

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "🤖 AUTO DASHBOARD GENERATOR - ONE CLICK SOLUTION" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "📅 Started at: $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')" -ForegroundColor Green
Write-Host ""

# Check Python installation
Write-Host "🔧 Checking Python installation..." -ForegroundColor Blue
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python first." -ForegroundColor Red
    Write-Host "💡 Download from: https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Check if CSV file exists
Write-Host "📁 Checking for CSV files..." -ForegroundColor Blue
$csvFiles = Get-ChildItem -Filter "*.csv" | Where-Object { $_.Name -like "*trade*" -or $_.Name -like "*closed*" }

if ($csvFiles.Count -eq 0) {
    $allCsvFiles = Get-ChildItem -Filter "*.csv"
    if ($allCsvFiles.Count -eq 0) {
        Write-Host "❌ No CSV files found in current directory!" -ForegroundColor Red
        Write-Host "💡 Please place your trading CSV file here and try again" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    } else {
        $csvFiles = $allCsvFiles
    }
}

$csvFile = $csvFiles[0].Name
Write-Host "✅ Found CSV file: $csvFile" -ForegroundColor Green
Write-Host ""

# Run the Python script
Write-Host "🚀 Running auto dashboard generator..." -ForegroundColor Magenta
Write-Host ""

try {
    python auto_dashboard_generator.py
    
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "🎉 AUTO DASHBOARD GENERATOR COMPLETED!" -ForegroundColor Green
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Check if files were created
    if (Test-Path "auto_generated_dashboard.html") {
        Write-Host "✅ Dashboard created: auto_generated_dashboard.html" -ForegroundColor Green
    }
    
    if (Test-Path "dashboard_screenshot.png") {
        Write-Host "✅ Screenshot created: dashboard_screenshot.png" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "📱 Next steps:" -ForegroundColor Yellow
    Write-Host "   1. ✅ Dashboard and screenshot should be open" -ForegroundColor White
    Write-Host "   2. ✅ Jill AI should be open at http://localhost:8502" -ForegroundColor White
    Write-Host "   3. 📷 Upload the screenshot to Jill AI" -ForegroundColor White
    Write-Host "   4. 🤖 Get automatic trading analysis!" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host "❌ Error running Python script: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Make sure all dependencies are installed" -ForegroundColor Yellow
}

Write-Host "Press Enter to finish..." -ForegroundColor Cyan
Read-Host