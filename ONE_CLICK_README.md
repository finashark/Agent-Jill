# 🤖 ONE CLICK DASHBOARD GENERATOR

## 🎯 Mục đích
Tạo dashboard trading và chụp ảnh tự động chỉ với **1 CLICK** để upload vào Jill AI.

---

## ⚡ QUICK START (30 giây)

### Phương án 1: Double-click file BAT (Windows)
```
🖱️ Double-click: "🤖 One Click Dashboard.bat"
```

### Phương án 2: PowerShell
```powershell
.\OneClickDashboard.ps1
```

### Phương án 3: Command Line
```bash
python auto_dashboard_generator.py
```

---

## 📋 Yêu cầu

### ✅ Cần có:
- **Python 3.7+** (tự động check)
- **File CSV** trading data trong cùng thư mục
- **Internet connection** (để tải packages)

### 🔧 Packages tự động cài:
- `pandas` - Xử lý dữ liệu
- `selenium` - Chụp ảnh tự động  
- `webdriver-manager` - Chrome driver
- `pillow` - Xử lý ảnh

---

## 🚀 Workflow hoàn toàn tự động

### Input: 
- 📁 File CSV trading data

### Process (tự động):
1. ✅ **Install packages** cần thiết
2. ✅ **Detect CSV file** trong thư mục
3. ✅ **Process data** và tính metrics  
4. ✅ **Generate HTML** dashboard đẹp
5. ✅ **Screenshot** tự động với Selenium
6. ✅ **Open files** (dashboard + ảnh + Jill AI)

### Output:
- 📄 `auto_generated_dashboard.html` - Dashboard đẹp
- 🖼️ `dashboard_screenshot.png` - Ảnh ready upload
- 🚀 Browser tự động mở Jill AI

---

## 📊 Dashboard Features

### 🎯 Key Metrics
- **Net P&L** với color coding
- **Total Trades** và win/loss count
- **Win Rate** percentage
- **Profit Factor** 
- **Total Lots** traded
- **Average Trade** size
- **Max Win/Loss** amounts

### 📈 Charts (tự động)
- **Pie Chart** - Asset distribution
- **Bar Chart** - Trading styles  
- **Color-coded** metrics

### 🎨 Professional Design
- **Responsive** layout
- **Gradient** backgrounds
- **Modern** typography
- **Chart.js** interactive charts

---

## 🔄 Supported CSV Formats

### ✅ Cột bắt buộc:
```
TICKET, SYMBOL, ACTION, LOTS, OPEN TIME, CLOSE TIME, PROFIT
```

### ✅ Auto-detect:
- **MetaTrader 4/5** exports
- **cTrader** reports  
- **Broker** statements
- **Custom** CSV formats

### 🧹 Auto-cleanup:
- Loại bỏ Balance transactions
- Clean datetime formats
- Handle missing data
- Calculate derived metrics

---

## 📱 Integration với Jill AI

### 🔄 Workflow:
1. **Run script** → Generate dashboard + screenshot
2. **Upload screenshot** vào Jill AI (http://localhost:8502)
3. **Automatic analysis** từ Jill
4. **Get consultation script** + promotions

### 🎯 Perfect cho:
- **Account Managers** - Quick client analysis
- **Sales Team** - Visual presentations  
- **Traders** - Performance review
- **Management** - Reporting dashboards

---

## 🛠️ Troubleshooting

### ❌ Python not found:
```bash
# Download và install Python từ:
https://python.org/downloads/
```

### ❌ No CSV files:
```
📁 Đặt file CSV trading data trong cùng thư mục với script
✅ File name có chứa "trade" hoặc "closed" được ưu tiên
```

### ❌ Screenshot failed:
```
⚠️ Chrome not installed or outdated
💡 Script sẽ tạo HTML dashboard, manual screenshot OK
```

### ❌ Jill AI not opening:
```bash
# Đảm bảo Jill AI đang chạy:
cd "path\to\jill\ai"
streamlit run app.py --server.port 8502
```

---

## 📁 File Structure

```
📂 Project Folder/
├── 🤖 One Click Dashboard.bat     # Windows batch file
├── OneClickDashboard.ps1          # PowerShell script  
├── auto_dashboard_generator.py    # Main Python script
├── closed_trades_*.csv            # Your CSV data
├── auto_generated_dashboard.html  # Output dashboard
└── dashboard_screenshot.png       # Output screenshot
```

---

## 🎨 Customization Options

### 🔧 Modify script để:
- **Change colors** - Edit CSS trong HTML template
- **Add metrics** - Modify dashboard_data dict
- **Chart types** - Update Chart.js configs
- **Screenshot size** - Change Selenium window size

### 📊 Example customizations:
```python
# Thay đổi màu sắc
'background': 'linear-gradient(135deg, #your-color1, #your-color2)'

# Thêm metrics mới  
dashboard_data['your_metric'] = your_calculation

# Resize screenshot
driver.set_window_size(1920, 1200)  # Custom size
```

---

## 📞 Support

### 🐛 Bug reports:
- Check console output for errors
- Verify CSV file format
- Test with sample data first

### 💡 Feature requests:
- Suggest improvements
- Custom chart types  
- Additional metrics
- Integration options

---

## 🎉 Success Checklist

✅ **Script runs** without errors  
✅ **Dashboard** opens in browser  
✅ **Screenshot** file created  
✅ **Jill AI** opens automatically  
✅ **Upload** screenshot to Jill  
✅ **Get analysis** from Jill AI  

---

## 🚀 Advanced Usage

### 🔄 Batch processing:
```python
# Process multiple CSV files
for csv_file in csv_files:
    generate_dashboard(csv_file)
```

### 📊 Custom metrics:
```python
# Add your own calculations
dashboard_data['custom_metric'] = your_formula
```

### 🎨 Brand customization:
```css
/* Company colors */
:root {
    --primary-color: #your-brand-color;
    --secondary-color: #your-accent-color;
}
```

---

*🤖 Powered by Jill AI System - One Click Solution for Trading Analysis*