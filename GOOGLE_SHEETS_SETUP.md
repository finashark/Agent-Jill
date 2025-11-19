# 🔗 GOOGLE SHEETS TEMPLATE - SETUP TRỰC TIẾP

## 📋 **Template Link (Sẽ cập nhật sau)**

**Link Google Sheets Template:** `[Đang tạo template...]`

## 🚀 **Cách sử dụng Template:**

### **Bước 1: Copy Template**
1. Click vào link Google Sheets template ở trên
2. Chọn "File" → "Make a copy" 
3. Đặt tên cho bản copy của bạn

### **Bước 2: Import dữ liệu CSV**
1. Mở file CSV trading data của bạn
2. Copy toàn bộ dữ liệu (Ctrl+A, Ctrl+C)
3. Vào sheet "Data" trong Google Sheets template
4. Paste dữ liệu vào cell A1 (Ctrl+V)

### **Bước 3: Chụp screenshot Dashboard**
1. Chuyển sang sheet "Dashboard"
2. Đợi biểu đồ tự động cập nhật (2-3 giây)
3. Chụp screenshot toàn bộ dashboard
4. Save ảnh với tên dễ nhận biết

### **Bước 4: Upload vào Agent Jill**
1. Mở Agent Jill: http://localhost:8502
2. Ở Bước 1: Upload ảnh dashboard vừa chụp
3. Jill sẽ tự động chuyển sang Bước 2 để phân tích

## 📊 **Cấu trúc dữ liệu yêu cầu:**

Template sẽ tự động nhận diện các cột:
- `TICKET` - Mã giao dịch
- `OPEN_TIME` - Thời gian mở lệnh  
- `TYPE` - Loại lệnh (buy/sell)
- `SIZE` - Khối lượng
- `ITEM` - Cặp tiền tệ/symbol
- `PRICE` - Giá mở lệnh
- `S_L` - Stop Loss
- `T_P` - Take Profit
- `CLOSE_TIME` - Thời gian đóng lệnh
- `PRICE_CLOSE` - Giá đóng lệnh
- `COMMISSION` - Phí giao dịch
- `SWAP` - Phí swap
- `PROFIT` - Lợi nhuận

## 🎯 **Dashboard sẽ hiển thị:**

### **Metrics chính:**
- 💰 Total P&L
- 📈 Win Rate (%)
- 📉 Max Drawdown
- 🔢 Total Trades
- ⏱️ Avg Trade Duration

### **Biểu đồ:**
- 🥧 Asset Class Distribution
- 📊 Trading Style Breakdown
- 📈 P&L Over Time
- 🎯 Win/Loss Distribution

## ⚡ **Auto-calculation Features:**

Template tự động tính:
- **Asset Classes:** Major, Minor, Exotic, Crypto, Indices, Commodities
- **Trading Styles:** SCALP, INTRADAY, SWING, POSITION (dựa trên thời gian giữ lệnh)
- **Performance Metrics:** Sharpe ratio, Max consecutive losses, Profit factor

---

### 📝 **Lưu ý quan trọng:**
- Template hỗ trợ tối đa 10,000 giao dịch
- Tự động format tiền tệ và phần trăm
- Responsive design cho screenshot đẹp
- Có thể tùy chỉnh màu sắc và layout

---

### 🆘 **Hỗ trợ:**
Nếu gặp vấn đề:
1. Kiểm tra format dữ liệu CSV đúng chuẩn
2. Đảm bảo không có dòng trống trong data
3. Refresh sheet nếu biểu đồ không cập nhật