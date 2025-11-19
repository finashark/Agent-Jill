# Hướng Dẫn Sử Dụng Agent Jill - Phiên Bản Manual Entry

## 📝 Tổng Quan

Do giới hạn về tải file CSV trong môi trường deployment, Agent Jill đã được cập nhật với **workflow nhập liệu thủ công**. Quy trình mới gồm 2 bước:

1. **Tính toán metrics từ CSV** (sử dụng Python script)
2. **Nhập metrics vào Agent Jill** (qua form web)

---

## 🛠️ Công Cụ: Trading Metrics Calculator

### Cài Đặt

```bash
# Cài đặt thư viện cần thiết
pip install pandas openpyxl
```

### Sử Dụng

**Cách 1: Chạy trực tiếp**
```bash
python trading_metrics_calculator.py
```
Script sẽ hỏi đường dẫn folder chứa file CSV.

**Cách 2: Truyền đường dẫn qua tham số**
```bash
python trading_metrics_calculator.py "D:\Trading Data\CSV Files"
```

### Output

Script sẽ:
- ✅ Đọc và xử lý file CSV
- ✅ Tính toán tất cả metrics cần thiết
- ✅ Hiển thị kết quả trên console
- ✅ Xuất file Excel: `Trading_Metrics_Summary.xlsx`

### Ví Dụ Output

```
📊 KẾT QUẢ TÍNH TOÁN METRICS
============================================================

🔢 Tổng số giao dịch: 156
🎯 Tỷ lệ thắng: 58.3%
💰 Profit Factor: 1.45
💵 Net PnL: $2,345.67
📦 Tổng khối lượng: 24.50 lots
⏰ Thời gian nắm giữ TB: 3.2 giờ
⚡ Tỷ lệ Scalp: 65.4%
🏆 Tài sản chính: XAUUSD

🎭 PHONG CÁCH GIAO DỊCH:
   ⚡ SCALP (< 1h): 65.4%
   📊 INTRADAY (1-8h): 28.2%
   📈 SWING (8h-7d): 6.4%
   📉 POSITION (> 7d): 0.0%

📊 PHÂN BỔ TÀI SẢN TOP 3:
   1. XAUUSD: 52.6%
   2. EURUSD: 28.8%
   3. GBPUSD: 12.8%
```

---

## 📋 Quy Trình Sử Dụng Agent Jill

### Bước 1: Tính Toán Metrics

1. Chuẩn bị file CSV từ broker (MT4/MT5)
2. Chạy `trading_metrics_calculator.py`
3. Ghi nhận các giá trị metrics được hiển thị

### Bước 2: Nhập Vào Agent Jill

1. Mở Agent Jill web app
2. Tại **BƯỚC 1: Nhập Dữ Liệu Giao Dịch**, điền form:

   **📊 Các Chỉ Số Giao Dịch:**
   - Tổng số giao dịch
   - Tỷ lệ thắng (%)
   - Profit Factor
   - Net PnL (USD)
   - Thời gian nắm giữ TB (giờ)
   - Tỷ lệ Scalp (%)
   - Tổng khối lượng (lots)
   - Tài sản giao dịch chính

   **🎭 Phân Bố Phong Cách Giao Dịch:**
   - SCALP (< 1h) %
   - INTRADAY (1-8h) %
   - SWING (8h-7d) %
   - POSITION (> 7d) %
   
   ⚠️ **Lưu ý:** Tổng các tỷ lệ phải = 100%

   **📊 Phân Bố Top 3 Tài Sản:**
   - Tài sản #1 + % Giao dịch
   - Tài sản #2 + % Giao dịch
   - Tài sản #3 + % Giao dịch

3. Click **✅ Xử Lý Dữ Liệu**

### Bước 3-5: Tiếp Tục Như Bình Thường

- **Bước 2:** Xem phân tích hành vi (tự động hiển thị)
- **Bước 3:** Nhập thông tin khách hàng
- **Bước 4:** Xem báo cáo AI phân tích
- **Bước 5:** Tạo advisory letter

---

## 📁 Cấu Trúc File CSV Yêu Cầu

File CSV từ broker cần có các cột sau:

### Cột Bắt Buộc:
- `TICKET` / `Ticket` / `ticket` - Mã lệnh
- `SYMBOL` / `Symbol` / `Item` - Mã tài sản (XAUUSD, EURUSD, etc.)
- `ACTION` / `Type` / `Action` - Buy/Sell
- `LOTS` / `Volume` - Khối lượng giao dịch
- `OPEN_TIME` / `Open Time` - Thời gian mở lệnh
- `CLOSE_TIME` / `Close Time` - Thời gian đóng lệnh
- `PROFIT` / `Profit` - Lãi/lỗ

### Cột Tùy Chọn:
- `COMM` / `Commission` - Phí giao dịch
- `SWAP` / `Swap` - Phí qua đêm
- `TAXES` / `Taxes` - Thuế

⚠️ **Lưu ý:** Script tự động nhận diện và chuẩn hóa tên cột, hỗ trợ nhiều format khác nhau.

---

## ❓ Khắc Phục Sự Cố

### Lỗi: "Không tìm thấy file CSV"
- Kiểm tra đường dẫn folder có đúng không
- Đảm bảo file có đúng extension `.csv`

### Lỗi: "Thiếu các cột bắt buộc"
- Kiểm tra file CSV có đầy đủ các cột cần thiết
- Xem danh sách cột hiện có trong output
- So sánh với yêu cầu ở trên

### Lỗi: "Không có dữ liệu giao dịch hợp lệ"
- File CSV chỉ chứa Balance transactions
- Không có giao dịch Buy/Sell thực tế
- Dữ liệu thời gian không hợp lệ

### Lỗi: Encoding
- Script tự động thử nhiều encoding (UTF-8, Latin-1, CP1252)
- Nếu vẫn lỗi, thử mở CSV bằng Excel và Save As với UTF-8 encoding

### Lỗi: "cannot import pandas"
```bash
pip install pandas openpyxl
```

---

## 🎯 Tips & Best Practices

### Tổ Chức File
```
📁 Trading Data/
   📁 2024-01/
      📄 account_12345_jan.csv
   📁 2024-02/
      📄 account_12345_feb.csv
   📄 Trading_Metrics_Summary.xlsx (output)
```

### Kiểm Tra Nhanh
Trước khi nhập vào Agent Jill, kiểm tra:
- ✅ Tổng % phong cách = 100%
- ✅ Net PnL khớp với broker statement
- ✅ Tổng số giao dịch hợp lý
- ✅ Win rate trong khoảng 0-100%
- ✅ Profit Factor > 0

### Xử Lý Nhiều File
Nếu có nhiều file CSV (nhiều tháng), có 2 cách:

**Cách 1:** Gộp CSV trước khi xử lý
```bash
# Windows
copy *.csv merged.csv

# Linux/Mac
cat *.csv > merged.csv
```

**Cách 2:** Chạy script cho từng file, sau đó tổng hợp metrics thủ công

---

## 🔄 So Sánh: CSV Upload vs Manual Entry

| Tính Năng | CSV Upload (Cũ) | Manual Entry (Mới) |
|-----------|-----------------|-------------------|
| Upload trực tiếp | ✅ | ❌ |
| Hoạt động trên mọi deployment | ❌ | ✅ |
| Phân tích trade-by-trade | ✅ | ❌ |
| Biểu đồ chi tiết | ✅ | ⚠️ Giới hạn |
| Tốc độ nhập liệu | Nhanh | Trung bình |
| Độ chính xác | Cao | Cao (nếu dùng script) |
| Offline processing | ❌ | ✅ |

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra phần "Khắc Phục Sự Cố" ở trên
2. Xem log output của script
3. Kiểm tra format file CSV
4. Đảm bảo đã cài đặt đầy đủ dependencies

---

## 📝 Changelog

### Version 2.0 (Current)
- ✅ Thêm manual entry form
- ✅ Tạo Python calculator script
- ✅ Hỗ trợ Excel export
- ✅ Tương thích với cả CSV và manual mode
- ✅ Cập nhật UI và workflow

### Version 1.0 (Legacy)
- CSV upload trực tiếp
- Full trade-by-trade analysis
- Biểu đồ chi tiết

---

## 🔮 Tương Lai

Đang phát triển:
- 📊 Excel Calculator với VBA (tự động hóa hoàn toàn)
- 🌐 Web-based calculator (không cần Python)
- 📱 Mobile-friendly input form
- 🔄 Batch processing nhiều file
- 💾 Lưu trữ metrics history

---

**Cập nhật:** 2024-01-30  
**Phiên bản:** 2.0.0  
**Tác giả:** Agent Jill Development Team
