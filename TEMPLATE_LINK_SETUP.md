# 🔗 GOOGLE SHEETS TEMPLATE - READY TO USE

## 📧 **Email nhận template:** phamhuynhchau@gmail.com

## 🚀 **LINK TEMPLATE ALTERNATIVES:**

### **Option 1: Google Sheets Template Library**
```
https://docs.google.com/spreadsheets/u/0/?tgif=d&ftv=1&folder=0AKz9rNKXWoEeUk9PVA
```
- Tìm "Trading Dashboard" hoặc "Financial Template"
- Make a copy về tài khoản của bạn

### **Option 2: Tạo nhanh từ CSV (Khuyên dùng)**

**Bước 1:** Vào https://sheets.google.com
**Bước 2:** Tạo sheet mới
**Bước 3:** File → Import → Upload file `sample_template_data.csv`
**Bước 4:** Copy đoạn code setup dashboard bên dưới

## 📊 **DASHBOARD SETUP CODE - COPY & PASTE**

### **Sheet "Dashboard" - Cell A1:**

```
=ARRAYFORMULA({
"TRADING PERFORMANCE DASHBOARD","","","","","";
"","","","","","";
"Total P&L:",SUMPRODUCT(Data.M:M),"","Win Rate:",COUNTIF(Data.M:M,">0")/(COUNTA(Data.M:M)-1),"";
"Total Trades:",COUNTA(Data.A:A)-1,"","Max Drawdown:",MIN(Data.M:M),"";
"Avg Trade:",AVERAGE(Data.M:M),"","Best Trade:",MAX(Data.M:M),"";
"","","","Worst Trade:",MIN(Data.M:M),"";
"","","","","","";
"ASSET BREAKDOWN","","","TRADING STYLES","","";
"","","","","","";
"Major Pairs:",COUNTIFS(Data.E:E,"EUR*")+COUNTIFS(Data.E:E,"GBP*")+COUNTIFS(Data.E:E,"USD*"),"","Scalp (<1h):",COUNTIFS(Data.I:I,"<"&Data.B:B+TIME(1,0,0)),"";
"Minor Pairs:",COUNTIFS(Data.E:E,"AUD*")+COUNTIFS(Data.E:E,"NZD*")+COUNTIFS(Data.E:E,"CAD*"),"","Intraday (1-24h):",COUNTIFS(Data.I:I,">="&Data.B:B+TIME(1,0,0),Data.I:I,"<"&Data.B:B+1),"";
"Commodities:",COUNTIFS(Data.E:E,"XAU*")+COUNTIFS(Data.E:E,"XAG*"),"","Swing (1-7d):",COUNTIFS(Data.I:I,">="&Data.B:B+1,Data.I:I,"<"&Data.B:B+7),"";
"Indices:",COUNTIFS(Data.E:E,"SPX*")+COUNTIFS(Data.E:E,"NAS*"),"","Position (>7d):",COUNTIFS(Data.I:I,">="&Data.B:B+7),""
})
```

## 🎨 **FORMATTING QUICK SETUP:**

### **Step 1: Headers**
- Select A1, G1, A8, D8
- Format → Bold → Background Color: Blue → Text: White

### **Step 2: Numbers**  
- Select B3:B6, E3:E6, B10:B13, E10:E13
- Format → Number → More formats → Custom: "$#,##0.00"
- E3: Format as Percentage

### **Step 3: Conditional Formatting**
- Select B3:B6, E3:E6
- Format → Conditional formatting
- Custom formula: =B3>0 → Green background
- Custom formula: =B3<0 → Red background

## 📈 **ADD CHARTS:**

### **Chart 1: Asset Pie Chart**
1. Select A10:B13 (Asset data)
2. Insert → Chart → Pie chart
3. Chart title: "Asset Distribution"
4. Position: G10:K20

### **Chart 2: Trading Style Bar Chart**  
1. Select D10:E13 (Style data)
2. Insert → Chart → Column chart
3. Chart title: "Trading Styles"
4. Position: A15:E25

### **Chart 3: P&L Timeline**
1. Select Data.B:B,Data.M:M (Date and Profit columns)
2. Insert → Chart → Line chart
3. Chart title: "P&L Over Time"
4. Position: G15:K25

## 📸 **SCREENSHOT OPTIMIZATION:**

### **Before taking screenshot:**
```
1. View → Gridlines (uncheck)
2. Zoom to 75%
3. Hide unused rows/columns
4. File → Print → Fit to 1 page
```

## 🔄 **AUTO-UPDATE FEATURES:**

### **Data Validation (Sheet "Data"):**
```
Column A: Data → Data validation → List of items: Numbers only
Column B: Date format: MM/DD/YYYY HH:MM:SS  
Column M: Number format: Currency
```

## 💾 **TEMPLATE SHARING:**

### **Make it a template:**
```
1. File → Make a copy
2. Title: "Trading Dashboard Template - MASTER"
3. Share → Anyone with link can view
4. Copy link and save for team
```

## 🎯 **QUICK START (1-MINUTE SETUP):**

```
1. Open: https://sheets.google.com
2. File → Import → Upload "sample_template_data.csv"
3. Add new sheet → Rename to "Dashboard"  
4. Paste dashboard code above into A1
5. Add formatting and charts
6. Screenshot → Upload to Jill!
```

---

## 📞 **Support Contact:**

- **Template Created For:** phamhuynhchau@gmail.com
- **Usage:** Trading performance analysis
- **Compatible:** Agent Jill AI Analysis

### **🔗 Quick Links:**
- **CSV Data:** Use `sample_template_data.csv` 
- **Setup Guide:** Follow `QUICK_DASHBOARD_SETUP.md`
- **Agent Jill:** http://localhost:8502

---

**💡 Pro Tip:** Bookmark the template link sau khi tạo để team có thể access nhanh!