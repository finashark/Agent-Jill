# 📊 Google Sheets Trading Dashboard Template

## 🎯 Mục đích
Template này được thiết kế để:
1. **Sheet Data** - Dán dữ liệu CSV từ broker
2. **Sheet Dashboard** - Hiển thị biểu đồ và metrics tự động
3. **Screenshot Dashboard** - Upload vào Jill AI cho phân tích

---

## 📋 Hướng dẫn Setup

### BƯỚC 1: Tạo Google Sheet mới
1. Truy cập [Google Sheets](https://sheets.google.com)
2. Tạo spreadsheet mới
3. Đổi tên thành "Trading Analysis Dashboard"

### BƯỚC 2: Tạo Sheet "Data"
1. Đổi tên Sheet1 thành "Data"
2. Copy dữ liệu CSV vào đây
3. Header row (A1:Q1):

```
TICKET	SYMBOL	ACTION	LOTS	OPEN TIME	CLOSE TIME	PROFIT	COMM	SWAP	COMMENT	T/P	S/L	OPEN PRICE	CLOSE PRICE	Net_PnL	Balance_In	Balance_Out
```

### BƯỚC 3: Tạo Sheet "Dashboard"
1. Thêm sheet mới tên "Dashboard"
2. Setup layout theo template dưới đây

---

## 📊 Sheet DASHBOARD - Layout & Formulas

### 🎯 Cell Layout:

#### **A1:F2 - HEADER**
```
==============================================
       TRADING PERFORMANCE DASHBOARD
==============================================
```

#### **A4:F8 - KEY METRICS**
```
A4: Net P&L:          B4: =SUMIF(Data!B:B,"<>Balance",Data!G:G)
A5: Total Trades:     B5: =COUNTIF(Data!B:B,"<>Balance")-COUNTIF(Data!B:B,"")
A6: Win Rate:         B6: =COUNTIFS(Data!B:B,"<>Balance",Data!G:G,">0")/COUNTIF(Data!B:B,"<>Balance")*100&"%"
A7: Profit Factor:    B7: =SUMIFS(Data!G:G,Data!B:B,"<>Balance",Data!G:G,">0")/ABS(SUMIFS(Data!G:G,Data!B:B,"<>Balance",Data!G:G,"<0"))
A8: Avg Trade:        B8: =SUMIF(Data!B:B,"<>Balance",Data!G:G)/COUNTIF(Data!B:B,"<>Balance")

C4: Total Lots:       D4: =SUMIF(Data!B:B,"<>Balance",Data!D:D)
C5: Winning Trades:   D5: =COUNTIFS(Data!B:B,"<>Balance",Data!G:G,">0")
C6: Losing Trades:    D6: =COUNTIFS(Data!B:B,"<>Balance",Data!G:G,"<0")
C7: Max Win:          D7: =MAXIFS(Data!G:G,Data!B:B,"<>Balance")
C8: Max Loss:         D8: =MINIFS(Data!G:G,Data!B:B,"<>Balance")
```

#### **A10:F14 - TRADING STYLE ANALYSIS**
```
A10: TRADING STYLE BREAKDOWN
A11: Scalp (< 1h):    B11: =(FORMULA_FOR_SCALP_COUNT)/TOTAL_TRADES*100&"%"
A12: Intraday (1-8h): B12: =(FORMULA_FOR_INTRADAY_COUNT)/TOTAL_TRADES*100&"%"  
A13: Swing (8h-7d):   B13: =(FORMULA_FOR_SWING_COUNT)/TOTAL_TRADES*100&"%"
A14: Position (>7d):  B14: =(FORMULA_FOR_POSITION_COUNT)/TOTAL_TRADES*100&"%"

C10: ASSET BREAKDOWN
C11: Forex:           D11: =COUNTIFS(Data!B:B,"*USD*",Data!B:B,"<>Balance")+COUNTIFS(Data!B:B,"*JPY*",Data!B:B,"<>Balance")+COUNTIFS(Data!B:B,"*EUR*",Data!B:B,"<>Balance")+COUNTIFS(Data!B:B,"*GBP*",Data!B:B,"<>Balance")
C12: Gold/Silver:     D12: =COUNTIFS(Data!B:B,"*XAU*",Data!B:B,"<>Balance")+COUNTIFS(Data!B:B,"*XAG*",Data!B:B,"<>Balance")
C13: Indices:         D13: =COUNTIFS(Data!B:B,"*US30*",Data!B:B,"<>Balance")+COUNTIFS(Data!B:B,"*SPX*",Data!B:B,"<>Balance")
C14: Others:          D14: =TOTAL_TRADES-D11-D12-D13
```

#### **H1:O15 - CHARTS AREA**
```
H1: [PIE CHART - Asset Distribution]
H8: [LINE CHART - Cumulative P&L]
```

### 🎨 Charts Setup:

#### **PIE CHART - Asset Distribution (H1:L7)**
1. Insert > Chart > Pie Chart
2. Data range: C11:D14 (Asset names và counts)
3. Title: "Asset Distribution"
4. Colors: Blue theme

#### **LINE CHART - Cumulative P&L (H8:O15)**
1. Insert > Chart > Line Chart  
2. Data range: Cumulative P&L over time
3. Title: "Cumulative P&L Over Time"
4. X-axis: Date
5. Y-axis: Cumulative Profit/Loss

#### **BAR CHART - Trading Style (A16:F22)**
1. Insert > Chart > Column Chart
2. Data range: A11:B14 (Trading styles)
3. Title: "Trading Style Distribution"

---

## 🔧 Advanced Formulas

### Calculate Trading Duration (Helper Column in Data sheet):
```
Column R (Duration Hours): 
=IF(B2="Balance","",IF(B2="","",HOUR(F2-E2)+DAY(F2-E2)*24))
```

### Scalp Count Formula:
```
=COUNTIFS(Data!B:B,"<>Balance",Data!R:R,"<1")
```

### Cumulative P&L (for line chart):
```
Column S: =IF(ROW()=2,G2,S1+G2)
```

---

## 🎨 Formatting Style

### Colors:
- Header: Dark Blue (#1f4e79)
- Metrics: Light Blue (#4285f4)  
- Positive values: Green (#34a853)
- Negative values: Red (#ea4335)
- Charts: Professional blue theme

### Fonts:
- Headers: Bold, 14pt
- Metrics: Bold, 12pt
- Values: Regular, 11pt

---

## 📱 Final Dashboard Layout

```
┌─────────────────────────────────────────────────────────────┐
│                TRADING PERFORMANCE DASHBOARD                │
├─────────────────────┬───────────────────┬───────────────────┤
│ Net P&L: -$1,112.60 │ Total Lots: 15.2  │  [PIE CHART]      │
│ Total Trades: 1,316 │ Win Rate: 39.7%   │  Asset Dist.      │
│ Profit Factor: 0.92 │ Max Win: $37.98   │                   │
│ Avg Trade: -$0.85   │ Max Loss: -$26.40 │                   │
├─────────────────────┴───────────────────┤                   │
│ TRADING STYLE BREAKDOWN                 │                   │
│ Scalp (< 1h): 97.7%                    │                   │
│ Intraday (1-8h): 2.0%                  ├───────────────────┤
│ Swing (8h-7d): 0.3%                    │  [LINE CHART]     │
│ Position (>7d): 0%                     │  Cumulative P&L   │
└─────────────────────────────────────────┤                   │
│ [BAR CHART - Trading Styles]           │                   │
└─────────────────────────────────────────┴───────────────────┘
```

---

## 📲 Cách sử dụng

### STEP 1: Setup Template
1. Copy layout và formulas vào Google Sheets
2. Format theo màu sắc chuyên nghiệp

### STEP 2: Import Data  
1. Copy CSV data vào sheet "Data"
2. Dashboard sẽ tự động update

### STEP 3: Screenshot cho Jill
1. Chụp ảnh màn hình Dashboard
2. Upload vào Jill AI để phân tích
3. Nhận script tư vấn tự động

---

## 🔗 Quick Links

- [Google Sheets Template](https://docs.google.com/spreadsheets/create)
- [Jill AI App](http://localhost:8502)

---

*📊 Template được thiết kế để tương thích hoàn hảo với Jill AI Analysis System*