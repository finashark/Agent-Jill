# Trading Advisor Streamlit App

Ứng dụng phân tích hành vi giao dịch và đưa ra lời tư vấn cá nhân hóa dựa trên dữ liệu thực tế và hồ sơ người dùng.

## 🎯 Tính năng chính

- **Thu thập thông tin người dùng**: Form nhập liệu chi tiết về hồ sơ, tài chính, kinh nghiệm
- **Phân tích dữ liệu giao dịch**: Hỗ trợ copy/paste CSV hoặc upload file
- **Dashboard trực quan**: 15+ biểu đồ và metrics chi tiết
- **Phân loại trader**: 5 loại trader dựa trên thuật toán scoring kết hợp
- **Tư vấn cá nhân hóa**: Điểm mạnh, điểm yếu, khuyến nghị, cảnh báo rủi ro

## 📋 Yêu cầu hệ thống

- Python 3.9+
- 4GB RAM khả dụng
- Trình duyệt web hiện đại (Chrome, Firefox, Edge)

## 🚀 Cài đặt

### 1. Clone repository

```bash
git clone <repository-url>
cd trading-advisor-app
```

### 2. Tạo môi trường ảo (khuyến nghị)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

## 📊 Chạy ứng dụng

```bash
streamlit run app.py
```

Ứng dụng sẽ mở tại `http://localhost:8501`

## 📁 Cấu trúc thư mục

```
trading-advisor-app/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── src/                        # Source code modules
│   ├── __init__.py
│   ├── user_profile.py         # User profile collection
│   ├── data_loader.py          # CSV data loading & parsing
│   ├── metrics_calculator.py  # Performance metrics calculation
│   ├── trader_classifier.py   # Trader type classification
│   ├── advisor.py              # Advisory generation
│   └── visualizations.py       # Plotting functions
│
├── config/                     # Configuration files
│   ├── form_fields.yaml        # Form field definitions
│   ├── trader_profiles.yaml   # Trader type profiles
│   └── advisory_rules.yaml    # Advisory rules by type
│
├── data/                       # Data directory
│   └── sample_trades.csv       # Sample trading data
│
└── assets/                     # Static assets (logos, etc.)
```

## 🎓 Hướng dẫn sử dụng

### Bước 1: Điền hồ sơ người dùng

1. Chọn tab **"👤 Hồ sơ người dùng"**
2. Điền đầy đủ các thông tin:
   - Thông tin cơ bản (tên, tuổi, giới tính, học vấn)
   - Thông tin tài chính (thu nhập, vốn giao dịch)
   - Kinh nghiệm & mục tiêu
   - Tự đánh giá (rủi ro, thời gian)
3. Nhấn **"💾 Lưu hồ sơ"**

### Bước 2: Tải dữ liệu giao dịch

1. Chọn tab **"📊 Dữ liệu giao dịch"**
2. Chọn phương thức:
   - **Copy/Paste**: Copy từ Excel/CSV và paste vào ô
   - **Upload File**: Upload file .csv
3. Nhấn **"🔄 Phân tích dữ liệu"**

**Định dạng CSV yêu cầu:**
```csv
TICKET,SYMBOL,ACTION,LOTS,OPEN TIME,CLOSE TIME,PROFIT,COMM,SWAP,COMMENT,T/P,S/L,OPEN PRICE,CLOSE PRICE
123456,EURUSD,BUY,0.1,2024-10-01 09:30,2024-10-01 15:45,25.50,-0.50,-1.20,,,1.1050,1.1075
```

### Bước 3: Xem phân tích

1. **Dashboard (📈)**: Tổng quan metrics và biểu đồ chính
2. **Phân tích chi tiết (🔍)**: Heatmap, holding time, top symbols
3. **Phân loại (🎯)**: Xác định trader type với radar chart
4. **Tư vấn (💡)**: Nhận khuyến nghị cá nhân hóa

## 🏷️ 5 Loại Trader

1. **Newbie Gambler** 🎲
   - Mới bắt đầu, mạo hiểm cao
   - Thiếu kỷ luật, overtrading
   - Cần học quản lý rủi ro

2. **Technical Day/Swing Trader** 📈
   - Có kinh nghiệm, kỷ luật tốt
   - Sử dụng phân tích kỹ thuật
   - Win rate ổn định 50-60%

3. **Long-term Value Investor** 💰
   - Đầu tư dài hạn, thận trọng
   - Tầm nhìn xa, kiên nhẫn
   - Đa dạng hóa tốt

4. **Part-time Opportunist** ⏰
   - Bán thời gian, cân bằng tốt
   - Trading song song công việc
   - Thực dụng, linh hoạt

5. **Asset Specialist** 🎯
   - Chuyên sâu một loại tài sản
   - Hiểu rõ thị trường chuyên môn
   - Rủi ro tập trung cao

## 🔧 Cấu hình nâng cao

### Tùy chỉnh classification weights

Chỉnh sửa `config/trader_profiles.yaml`:

```yaml
classification_weights:
  profile_data: 0.4      # 40% từ form người dùng
  trading_behavior: 0.6  # 60% từ dữ liệu CSV
```

### Tùy chỉnh advisory rules

Chỉnh sửa `config/advisory_rules.yaml` để thay đổi khuyến nghị cho từng trader type.

## 📊 Metrics được tính toán

- **Performance**: Total P&L, Win Rate, Profit Factor, Max Drawdown
- **Risk**: Risk/Reward Ratio, Stop Loss Usage
- **Trading Behavior**: Avg Trades/Day, Holding Time, Trading Frequency
- **Symbol Analysis**: Top symbols, diversification score

## 🐛 Troubleshooting

### Lỗi import CSV

- Kiểm tra encoding file (UTF-8 khuyến nghị)
- Đảm bảo header có đầy đủ các cột cần thiết
- Định dạng ngày tháng: `YYYY-MM-DD HH:MM` hoặc `YYYY-MM-DD HH:MM:SS`

### Lỗi visualization

```bash
# Cài đặt lại Plotly
pip uninstall plotly
pip install plotly==5.17.0
```

### Lỗi YAML config

- Kiểm tra indentation (dùng spaces, không dùng tabs)
- Validate YAML tại [yamllint.com](https://www.yamllint.com/)

## 🔒 Bảo mật & Privacy

- Dữ liệu chỉ được xử lý cục bộ trên máy bạn
- Không có dữ liệu nào được gửi lên server
- Session state được xóa khi đóng trình duyệt

## 🚀 Tính năng tương lai

- [ ] Xuất báo cáo PDF
- [ ] So sánh nhiều periods
- [ ] Machine Learning predictions
- [ ] Multi-language support
- [ ] Mobile responsive UI
- [ ] Integration với broker APIs

## 📝 License

MIT License - Xem file LICENSE để biết chi tiết

## 🤝 Đóng góp

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Liên hệ

- Email: support@sharkmeai.com
- GitHub: [github.com/sharkmeai](https://github.com/sharkmeai)
- Website: [sharkmeai.com](https://sharkmeai.com)

## 🙏 Credits

Dựa trên nghiên cứu:
- "Phân tích hành vi giao dịch Forex" (nghiên cứu 01.txt)
- Psychology of Trading by Brett Steenbarger
- Trading in the Zone by Mark Douglas

---

**Developed with ❤️ by SharkMe AI Team**
