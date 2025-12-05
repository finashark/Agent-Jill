# PDF Export Feature - Visual Guide

## 📍 Location in App

The PDF export feature is located at the **bottom of Tab 7 (Tư vấn)**

```
App Structure:
├── Tab 1: 📝 Hồ sơ người dùng
├── Tab 2: 📊 Dữ liệu giao dịch
├── Tab 3: 📈 Phân tích dữ liệu
├── Tab 4: 🎯 Performance Metrics
├── Tab 5: 📊 Trực quan hóa
├── Tab 6: 🏷️ Phân loại
└── Tab 7: 💡 Tư vấn
    ├── Trader Type Display
    ├── 💪 Điểm mạnh
    ├── ⚠️ Điểm yếu
    ├── 🎯 Khuyến nghị
    ├── 🚨 Cảnh báo rủi ro
    ├── 📝 Tóm tắt
    └── 📄 Xuất báo cáo ← NEW FEATURE HERE
        ├── Description text
        └── [📥 Xuất báo cáo PDF] Button
```

## 🖼️ UI Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                    📄 Xuất báo cáo                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Tải xuống báo cáo đầy đủ dưới dạng   ┌─────────────────────┐ │
│  PDF để lưu trữ hoặc chia sẻ.         │  📥 Xuất báo cáo    │ │
│                                        │      PDF            │ │
│                                        └─────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 User Flow

### Step 1: Initial State
```
User scrolls to bottom of Tư vấn tab
└── Sees "📄 Xuất báo cáo" section
    └── Button: [📥 Xuất báo cáo PDF]
```

### Step 2: Click Button
```
User clicks [📥 Xuất báo cáo PDF]
└── Shows spinner: "⏳ Đang tạo báo cáo PDF..."
    └── PDF generation in progress (1-2 seconds)
```

### Step 3: PDF Generated
```
✅ Success!
├── Shows new button: [⬇️ Tải xuống PDF]
└── Shows message: "✅ Báo cáo PDF đã được tạo thành công!"
```

### Step 4: Download
```
User clicks [⬇️ Tải xuống PDF]
└── Browser downloads file
    └── Filename: Trading_Report_{name}_{timestamp}.pdf
```

## 📄 PDF Output Preview

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║          BÁO CÁO TƯ VẤN GIAO DỊCH                        ║
║                                                           ║
║               Ngày tạo: 05/12/2024 16:14                 ║
║                                                           ║
║───────────────────────────────────────────────────────────║
║                                                           ║
║  1. THÔNG TIN HỒ SƠ NGƯỜI DÙNG                          ║
║                                                           ║
║  ┌─────────────────────┬────────────────────────┐       ║
║  │ Tên:                │ Nguyen Van A           │       ║
║  │ Tuổi:               │ 35                     │       ║
║  │ Giới tính:          │ Nam                    │       ║
║  │ Học vấn:            │ Đại học                │       ║
║  │ Thu nhập:           │ $50,000 - $100,000     │       ║
║  │ Vốn giao dịch:      │ $10,000.00             │       ║
║  │ Kinh nghiệm:        │ 2-5 năm                │       ║
║  │ Khả năng rủi ro:    │ 7/10                   │       ║
║  │ Thời gian:          │ 2-4 giờ/ngày           │       ║
║  │ Mục tiêu:           │ Tăng thu nhập          │       ║
║  └─────────────────────┴────────────────────────┘       ║
║                                                           ║
║  2. PHÂN LOẠI TRADER                                     ║
║                                                           ║
║  ┌─────────────────────┬────────────────────────┐       ║
║  │ Loại Trader:        │ Aggressive Trader      │       ║
║  │ Độ tin cậy:         │ 85.0%                  │       ║
║  │ Phong cách:         │ Day Trading            │       ║
║  │ Mức rủi ro:         │ High                   │       ║
║  └─────────────────────┴────────────────────────┘       ║
║                                                           ║
║  3. CHỈ SỐ HIỆU SUẤT                                     ║
║                                                           ║
║  ┌─────────────────────┬────────────────────────┐       ║
║  │ Tổng PnL:           │ $5,432.50              │       ║
║  │ Tỷ lệ thắng:        │ 65.50%                 │       ║
║  │ Tổng giao dịch:     │ 150                    │       ║
║  │ Giao dịch thắng:    │ 98                     │       ║
║  │ Giao dịch thua:     │ 52                     │       ║
║  │ Lợi nhuận TB:       │ $120.50                │       ║
║  │ Lỗ trung bình:      │ $-85.30                │       ║
║  │ Max Drawdown:       │ $-1,500.00             │       ║
║  │ Risk/Reward:        │ 1.41                   │       ║
║  │ Profit Factor:      │ 2.15                   │       ║
║  └─────────────────────┴────────────────────────┘       ║
║                                                           ║
║  4. BÁO CÁO TƯ VẤN                                       ║
║                                                           ║
║  Loại Trader: Aggressive Trader                          ║
║                                                           ║
║  4.1. ĐIỂM MẠNH                                          ║
║  • Tỷ lệ thắng cao (65.5%), cho thấy khả năng           ║
║    phân tích tốt                                         ║
║  • Risk/Reward ratio tích cực (1.41)                     ║
║  • Số lượng giao dịch đủ lớn để đánh giá                ║
║                                                           ║
║  4.2. ĐIỂM YẾU                                           ║
║  • Max drawdown cao (-$1,500), cần quản lý rủi ro       ║
║  • Thiếu kiên nhẫn trong việc chờ đợi setup tốt         ║
║  • Có xu hướng giao dịch quá nhiều                       ║
║                                                           ║
║  4.3. KHUYẾN NGHỊ                                        ║
║  1. Giảm kích thước vị thế xuống 1-2% mỗi giao dịch     ║
║  2. Thiết lập stop-loss cố định cho mọi giao dịch       ║
║  3. Tập trung vào 2-3 cặp tiền chính                     ║
║  4. Ghi nhật ký giao dịch để cải thiện                   ║
║                                                           ║
║  4.4. CẢNH BÁO RỦI RO                                    ║
║  ⚠ Mức độ rủi ro cao - chỉ phù hợp với nhà đầu tư       ║
║    có kinh nghiệm                                        ║
║  ⚠ Không sử dụng đòn bẩy quá cao (tối đa 1:10)          ║
║  ⚠ Luôn có kế hoạch quản lý vốn rõ ràng                 ║
║                                                           ║
║  4.5. TÓM TẮT                                            ║
║  Bạn là một trader năng động với phong cách giao dịch    ║
║  tích cực. Điểm mạnh của bạn là tỷ lệ thắng tốt và      ║
║  khả năng đọc thị trường. Tuy nhiên, cần cải thiện       ║
║  quản lý rủi ro để giảm drawdown và bảo vệ vốn.          ║
║                                                           ║
║───────────────────────────────────────────────────────────║
║                                                           ║
║     Báo cáo này được tạo tự động bởi Trading Advisor AI  ║
║   Thông tin chỉ mang tính chất tham khảo, không phải    ║
║                  lời khuyên đầu tư                       ║
║                                                           ║
║         © 2025 SharkMe AI. All rights reserved.          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

## 💻 Code Flow Diagram

```
User Action                   System Response
────────────────────────────────────────────────────────────

Click Button
    │
    ├─→ Validate Data
    │       │
    │       ├─→ Check profile_data
    │       ├─→ Check classification
    │       ├─→ Check metrics
    │       └─→ Check advisory
    │
    ├─→ Initialize PDFReportGenerator
    │
    ├─→ Generate PDF
    │       │
    │       ├─→ Add Header
    │       ├─→ Add Profile Section
    │       ├─→ Add Classification Section
    │       ├─→ Add Metrics Section
    │       ├─→ Add Advisory Section
    │       └─→ Add Footer
    │
    ├─→ Generate Filename
    │   (Trading_Report_{name}_{timestamp}.pdf)
    │
    ├─→ Create Download Button
    │
    └─→ Show Success Message

Download Button Click
    │
    └─→ Browser Downloads PDF
```

## 🎯 Data Flow

```
Session State Data                 PDF Sections
──────────────────────────────────────────────────────

st.session_state.profile_data  →  1. User Profile
  ├─ name                           ├─ Basic Info
  ├─ age                            ├─ Financial Info
  ├─ gender                         ├─ Experience
  ├─ education                      └─ Goals
  ├─ income
  ├─ capital
  ├─ experience
  ├─ risk_tolerance
  ├─ available_time
  └─ goals

st.session_state.classification →  2. Classification
  ├─ trader_type                    ├─ Trader Type
  ├─ confidence_score               ├─ Confidence %
  ├─ trading_style                  ├─ Style
  └─ risk_level                     └─ Risk Level

st.session_state.metrics        →  3. Metrics
  ├─ total_pnl                      ├─ PnL
  ├─ win_rate                       ├─ Win Rate
  ├─ total_trades                   ├─ Trades
  ├─ winning_trades                 ├─ Winning
  ├─ losing_trades                  ├─ Losing
  ├─ avg_profit                     ├─ Avg Profit
  ├─ avg_loss                       ├─ Avg Loss
  ├─ max_drawdown                   ├─ Drawdown
  ├─ risk_reward_ratio              ├─ RR Ratio
  └─ profit_factor                  └─ PF

st.session_state.advisory       →  4. Advisory
  ├─ trader_type                    ├─ Type
  ├─ strengths                      ├─ Strengths
  ├─ weaknesses                     ├─ Weaknesses
  ├─ recommendations                ├─ Recommendations
  ├─ risk_warnings                  ├─ Warnings
  └─ summary                        └─ Summary
```

## ⚠️ Error Scenarios

### Scenario 1: Missing reportlab
```
❌ ModuleNotFoundError: No module named 'reportlab'
└── Solution: pip install reportlab
```

### Scenario 2: Missing Data
```
❌ Data not available
└── Ensure all previous tabs are completed
    ├── Tab 1: Profile filled
    ├── Tab 2: Data uploaded
    ├── Tab 6: Classification done
    └── Tab 7: Advisory generated
```

### Scenario 3: Generation Error
```
❌ Lỗi khi tạo báo cáo PDF: [error message]
└── Check logs for details
    └── Error logged with full traceback
```

## ✅ Success Indicators

1. ✅ Button appears in Tab 7
2. ✅ Spinner shows during generation
3. ✅ Download button appears after generation
4. ✅ Success message displays
5. ✅ PDF file downloads with correct filename
6. ✅ PDF opens and displays correctly
7. ✅ Vietnamese text renders properly
8. ✅ All sections present and formatted

## 🔧 Developer Notes

**Key Components:**
- `PDFReportGenerator` class handles all PDF logic
- `reportlab` library provides PDF generation
- `BytesIO` buffer for memory-efficient generation
- `st.download_button` for browser download
- Error handling catches all exceptions

**Testing Checklist:**
- [x] Imports work correctly
- [x] PDF generates without errors
- [x] Vietnamese characters display
- [x] All sections render properly
- [x] Tables format correctly
- [x] Filename includes timestamp
- [x] Download works in browser
- [x] Error messages display properly

---

**Last Updated**: December 5, 2025
**Status**: ✅ Production Ready
