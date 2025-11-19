# 📊 GOOGLE SHEETS DASHBOARD SETUP - COPY & PASTE

## 🎯 **Sheet "Dashboard" Layout:**

### **A1-F10: Key Metrics Section**

```
A1: TRADING PERFORMANCE DASHBOARD
A3: Total P&L:        B3: =SUMPRODUCT(Data.M:M)
A4: Total Trades:     B4: =COUNTA(Data.A:A)-1
A5: Win Rate:         B5: =COUNTIF(Data.M:M,">0")/(COUNTA(Data.M:M)-1)
A6: Max Drawdown:     B6: =MIN(Data.M:M)
A7: Avg Trade:        B7: =AVERAGE(Data.M:M)
A8: Best Trade:       B8: =MAX(Data.M:M)
A9: Worst Trade:      B9: =MIN(Data.M:M)
```

### **H1-O10: Asset Distribution**

```
H1: ASSET BREAKDOWN
H3: Major Pairs:    I3: =COUNTIFS(Data.E:E,"EUR*")+COUNTIFS(Data.E:E,"GBP*")+COUNTIFS(Data.E:E,"USD*")+COUNTIFS(Data.E:E,"JPY*")
H4: Minor Pairs:    I4: =COUNTIFS(Data.E:E,"AUD*")+COUNTIFS(Data.E:E,"NZD*")+COUNTIFS(Data.E:E,"CAD*")-I3
H5: Commodities:    I5: =COUNTIFS(Data.E:E,"XAU*")+COUNTIFS(Data.E:E,"XAG*")+COUNTIFS(Data.E:E,"OIL*")
H6: Indices:        I6: =COUNTIFS(Data.E:E,"SPX*")+COUNTIFS(Data.E:E,"NAS*")+COUNTIFS(Data.E:E,"DOW*")
H7: Crypto:         I7: =COUNTIFS(Data.E:E,"BTC*")+COUNTIFS(Data.E:E,"ETH*")+COUNTIFS(Data.E:E,"*USD")
```

### **A12-F20: Trading Style Analysis**

```
A12: TRADING STYLES
A14: Scalp (<1h):     B14: =COUNTIFS(Data.B:B,"<"&Data.I:I+TIME(1,0,0))
A15: Intraday (1-24h): B15: =COUNTIFS(Data.B:B,">="&Data.I:I+TIME(1,0,0),Data.B:B,"<"&Data.I:I+1)
A16: Swing (1-7d):    B16: =COUNTIFS(Data.B:B,">="&Data.I:I+1,Data.B:B,"<"&Data.I:I+7)
A17: Position (>7d):  B17: =COUNTIFS(Data.B:B,">="&Data.I:I+7)
```

## 📈 **Tạo Charts:**

### **Chart 1: P&L Pie Chart (A22-F35)**
1. Select range H3:I7 (Asset data)
2. Insert → Chart → Pie Chart
3. Title: "Asset Distribution"
4. Colors: Blue palette

### **Chart 2: Trading Style Bar Chart (H22-O35)**
1. Select range A14:B17 (Style data)
2. Insert → Chart → Bar Chart  
3. Title: "Trading Styles"
4. Colors: Green palette

### **Chart 3: P&L Over Time (A37-O50)**
1. Select Data.B:B (dates) and Data.M:M (profits)
2. Insert → Chart → Line Chart
3. Title: "P&L Progression"
4. Colors: Red/Green

## 🎨 **Formatting:**

### **Headers (A1, H1, A12):**
- Font: Arial Bold 14pt
- Background: Dark Blue
- Text: White
- Merge cells horizontally

### **Metrics (B3:B9):**
- Format: Currency ($)
- B5: Format as Percentage
- Conditional formatting: Green if >0, Red if <0

### **Percentages:**
- B5: Format → Number → Percent
- Add sparklines for visual appeal

## 🔄 **Auto-refresh Setup:**

1. **Data Validation:** Data → Data validation on sheet "Data"
2. **Conditional Formatting:** Format → Conditional formatting
   - Green: Profit > 0
   - Red: Profit < 0
3. **Auto-resize:** Right-click columns → Resize columns A-Z

## 📸 **Screenshot Tips:**

1. **Zoom:** Set to 75-85% for full view
2. **Hide:** Gridlines (View → Gridlines off)
3. **Print area:** File → Print → Custom scale
4. **Format:** Landscape orientation

## 🔗 **Sharing Template:**

1. **Share settings:** Anyone with link can view
2. **Template mode:** File → Publish to web
3. **Copy link:** Share → Copy link

---

### **📋 Formula Quick Reference:**

```
Total P&L: =SUMPRODUCT(Data.M:M)
Win Rate: =COUNTIF(Data.M:M,">0")/(COUNTA(Data.M:M)-1)
Asset Count: =COUNTIFS(Data.E:E,"criteria")
Date Range: =Data.I:I-Data.B:B
Running P&L: =SUM(Data.$M$2:M2)
```

---

**💡 Pro Tip:** Sau khi setup xong, tạo template bằng cách "File → Make a copy" và share link copy đó cho team!