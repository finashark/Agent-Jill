# Test bước 4 riêng biệt
analysis_result = {
    'trader_type': 'newbie_gambler',
    'metrics': {
        'total_trades': 100,
        'win_rate': 45.5,
        'profit_factor': 0.8,
        'avg_holding_hours': 2.5,
        'net_pnl': -150.25,
        'total_lots': 25.5
    },
    'trading_style': {
        'scalp': 60,
        'intraday': 30,
        'swing': 10,
        'position': 0
    },
    'risk_level': 'CAO'
}

trader_info = {'name': 'Newbie Gambler'}

# Test f-string như trong app
test_markdown = f"""
### 🎯 Kết Quả Phân Loại: **{trader_info['name']}**

**📊 Các Chỉ Số Quan Trọng:**
- 🔢 Tổng số giao dịch: {analysis_result['metrics']['total_trades']}
- 🎯 Tỷ lệ thắng: {analysis_result['metrics']['win_rate']}%
- 💰 Profit Factor: {analysis_result['metrics']['profit_factor']}
- ⏰ Thời gian nắm giữ trung bình: {analysis_result['metrics']['avg_holding_hours']:.1f} giờ
- 💵 Net PnL: ${analysis_result['metrics']['net_pnl']:,.2f}
- 📦 Tổng khối lượng: {analysis_result['metrics']['total_lots']} lots

**🎭 Phong Cách Giao Dịch:**
- SCALP (< 1h): {analysis_result['trading_style']['scalp']}%
- INTRADAY (1-8h): {analysis_result['trading_style']['intraday']}%
- SWING (8h-7d): {analysis_result['trading_style']['swing']}%
- POSITION (>7d): {analysis_result['trading_style']['position']}%

**⚠️ Đánh Giá Rủi Ro: {analysis_result['risk_level']}**
"""

print("Test thành công!")
print(test_markdown)