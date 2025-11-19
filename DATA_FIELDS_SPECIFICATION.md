# Đặc Tả Chi Tiết Các Trường Dữ Liệu - Agent Jill Manual Entry

## 📊 Tổng Quan

Hệ thống Manual Entry có **18 trường dữ liệu** được chia thành 3 nhóm chính:
1. **Metrics Chính** (8 trường)
2. **Phân Bố Phong Cách Giao Dịch** (4 trường)
3. **Phân Bố Tài Sản** (6 trường = 3 cặp)

---

## 📈 NHÓM 1: METRICS CHÍNH (8 trường)

### 1. 🔢 Tổng Số Giao Dịch
**Field Name:** `total_trades`
**Kiểu dữ liệu:** Integer (1 - 10,000)
**Mặc định:** 50

#### 📝 Định nghĩa:
Tổng số lệnh giao dịch đã **ĐÓNG** (closed trades) trong khoảng thời gian phân tích.

#### 🧮 Công thức tính:
```python
total_trades = COUNT(CLOSED_TRADES)

# Điều kiện:
# - Chỉ tính lệnh đã đóng (có CLOSE_TIME)
# - Loại bỏ Balance transactions
# - Loại bỏ Deposit/Withdrawal
# - Chỉ tính Buy/Sell orders
```

#### 📊 Cách tính từ CSV:
```python
# Đọc CSV
df = pd.read_csv('trades.csv')

# Lọc giao dịch hợp lệ
df = df[df['ACTION'].isin(['Buy', 'Sell', 'buy', 'sell'])]
df = df[df['CLOSE_TIME'].notna()]  # Chỉ lệnh đã đóng

# Đếm số lệnh
total_trades = len(df)
```

#### ✅ Validation:
- Min: 1 (ít nhất 1 giao dịch)
- Max: 10,000 (giới hạn hệ thống)
- Phải là số nguyên dương

#### 💡 Ý nghĩa phân tích:
- `< 20`: Trader mới hoặc part-time
- `20-100`: Trader tích cực
- `100-500`: Professional trader
- `> 500`: High-frequency trader hoặc scalper

---

### 2. 🎯 Tỷ Lệ Thắng (%)
**Field Name:** `win_rate`
**Kiểu dữ liệu:** Float (0.0 - 100.0%)
**Mặc định:** 55.0%
**Bước nhảy:** 0.1%

#### 📝 Định nghĩa:
Tỷ lệ phần trăm số lệnh có lãi (PROFIT > 0) so với tổng số lệnh.

#### 🧮 Công thức tính:
```python
win_rate = (winning_trades / total_trades) × 100

# Trong đó:
winning_trades = COUNT(trades WHERE PROFIT > 0)
total_trades = COUNT(all closed trades)
```

#### 📊 Cách tính từ CSV:
```python
# Đếm lệnh thắng
winning_trades = len(df[df['PROFIT'] > 0])

# Tính tỷ lệ
win_rate = (winning_trades / total_trades) * 100

# Ví dụ:
# 55 lệnh thắng / 100 lệnh = 55.0%
```

#### ✅ Validation:
- Min: 0.0% (tất cả lệnh thua)
- Max: 100.0% (tất cả lệnh thắng)
- Độ chính xác: 1 chữ số thập phân

#### 💡 Ý nghĩa phân tích:
- `< 40%`: RỦI RO CAO - Newbie Gambler
- `40-50%`: Cần cải thiện
- `50-60%`: Trader có kinh nghiệm
- `> 60%`: Technical Trader giỏi

#### ⚠️ Lưu ý quan trọng:
Win rate cao KHÔNG đồng nghĩa profitable! Phải xem kết hợp với Profit Factor và Net PnL.

---

### 3. 💰 Profit Factor
**Field Name:** `profit_factor`
**Kiểu dữ liệu:** Float (0.0 - 100.0)
**Mặc định:** 1.5
**Bước nhảy:** 0.01

#### 📝 Định nghĩa:
Tỷ lệ giữa tổng lợi nhuận của các lệnh thắng và tổng thua lỗ của các lệnh thua.

#### 🧮 Công thức tính:
```python
profit_factor = total_profit / abs(total_loss)

# Trong đó:
total_profit = SUM(PROFIT WHERE PROFIT > 0)
total_loss = ABS(SUM(PROFIT WHERE PROFIT < 0))
```

#### 📊 Cách tính từ CSV:
```python
# Tính tổng lãi
total_profit = df[df['PROFIT'] > 0]['PROFIT'].sum()

# Tính tổng lỗ (giá trị tuyệt đối)
total_loss = abs(df[df['PROFIT'] < 0]['PROFIT'].sum())

# Profit Factor
if total_loss > 0:
    profit_factor = total_profit / total_loss
else:
    profit_factor = 999.99  # Infinity (không có lệnh thua)

# Ví dụ:
# Total Profit: $5,000
# Total Loss: $3,000
# PF = 5000 / 3000 = 1.67
```

#### ✅ Validation:
- Min: 0.0 (tất cả lệnh thua)
- Max: 100.0 (giới hạn hệ thống, thực tế có thể = ∞)
- Độ chính xác: 2 chữ số thập phân

#### 💡 Ý nghĩa phân tích:
- `< 1.0`: LOSING TRADER - Tổng lỗ > Tổng lãi
- `1.0 - 1.3`: Break-even hoặc lãi nhẹ
- `1.3 - 2.0`: PROFITABLE - Trader có kinh nghiệm
- `> 2.0`: EXCELLENT - Professional trader

#### 🎯 Mục tiêu:
- Minimum: > 1.0 (profitable)
- Target: 1.5 - 2.0 (sustainable)
- Elite: > 2.5

---

### 4. 💵 Net PnL (USD)
**Field Name:** `net_pnl`
**Kiểu dữ liệu:** Float (-1,000,000.0 to +1,000,000.0)
**Mặc định:** 0.0
**Bước nhảy:** 0.01

#### 📝 Định nghĩa:
Tổng lãi/lỗ RÒNG sau khi trừ mọi chi phí (commission, swap, taxes).

#### 🧮 Công thức tính:
```python
net_pnl = SUM(PROFIT + COMMISSION + SWAP + TAXES)

# Trong đó:
# PROFIT: Lãi/lỗ từ giá
# COMMISSION: Phí giao dịch (thường âm)
# SWAP: Phí qua đêm (có thể âm hoặc dương)
# TAXES: Thuế (nếu có, thường âm)
```

#### 📊 Cách tính từ CSV:
```python
# Đảm bảo các cột tồn tại
df['COMM'] = df.get('COMM', 0).fillna(0)
df['SWAP'] = df.get('SWAP', 0).fillna(0)
df['TAXES'] = df.get('TAXES', 0).fillna(0)

# Tính Net PnL cho từng lệnh
df['Net_PnL'] = df['PROFIT'] + df['COMM'] + df['SWAP'] + df['TAXES']

# Tổng Net PnL
net_pnl = df['Net_PnL'].sum()

# Ví dụ 1 lệnh:
# PROFIT: +$100
# COMM: -$2
# SWAP: -$0.5
# TAXES: $0
# Net_PnL = 100 - 2 - 0.5 = $97.5
```

#### ✅ Validation:
- Min: -$1,000,000 (thua lỗ lớn)
- Max: +$1,000,000 (lãi lớn)
- Độ chính xác: 2 chữ số thập phân
- Có thể âm (thua lỗ)

#### 💡 Ý nghĩa phân tích:
- `< 0`: THUA LỖ - Cần can thiệp ngay
- `0 - $1000`: Break-even, lãi nhẹ
- `$1000 - $10000`: Profitable trader
- `> $10000`: Professional/Institutional

#### ⚠️ Lưu ý:
Net PnL phải tính cả commission và swap, không chỉ PROFIT!

---

### 5. ⏰ Thời Gian Nắm Giữ Trung Bình (giờ)
**Field Name:** `avg_holding_hours`
**Kiểu dữ liệu:** Float (0.0 - 720.0 giờ)
**Mặc định:** 2.5 giờ
**Bước nhảy:** 0.1 giờ

#### 📝 Định nghĩa:
Thời gian trung bình từ lúc mở lệnh (OPEN_TIME) đến lúc đóng lệnh (CLOSE_TIME).

#### 🧮 Công thức tính:
```python
holding_time_hours = (CLOSE_TIME - OPEN_TIME) / 3600  # Convert to hours

avg_holding_hours = MEAN(holding_time_hours for all trades)
```

#### 📊 Cách tính từ CSV:
```python
# Chuyển đổi sang datetime
df['OPEN_TIME'] = pd.to_datetime(df['OPEN_TIME'])
df['CLOSE_TIME'] = pd.to_datetime(df['CLOSE_TIME'])

# Tính holding time (giây)
df['Holding_Seconds'] = (df['CLOSE_TIME'] - df['OPEN_TIME']).dt.total_seconds()

# Chuyển sang giờ
df['Holding_Hours'] = df['Holding_Seconds'] / 3600

# Trung bình
avg_holding_hours = df['Holding_Hours'].mean()

# Ví dụ:
# Open: 2024-01-15 09:00:00
# Close: 2024-01-15 11:30:00
# Holding = 2.5 giờ
```

#### ✅ Validation:
- Min: 0.0 giờ (lý thuyết, thực tế > 0.01)
- Max: 720.0 giờ (30 ngày)
- Độ chính xác: 1 chữ số thập phân

#### 💡 Ý nghĩa phân tích:
- `< 1h`: SCALPER
- `1-8h`: DAY TRADER
- `8h-7 ngày (168h)`: SWING TRADER
- `> 7 ngày`: POSITION TRADER

#### 🎯 Phân loại theo thời gian:
| Thời gian | Loại | Đặc điểm |
|-----------|------|----------|
| < 5 phút | Ultra Scalper | Rủi ro cực cao |
| 5-60 phút | Scalper | Tần suất cao |
| 1-4 giờ | Intraday | Trong ngày |
| 4-24 giờ | Day Trader | Không qua đêm |
| 1-7 ngày | Swing | Nắm sóng |
| > 7 ngày | Position | Dài hạn |

---

### 6. ⚡ Tỷ Lệ Scalp (%)
**Field Name:** `scalp_ratio`
**Kiểu dữ liệu:** Float (0.0 - 100.0%)
**Mặc định:** 60.0%
**Bước nhảy:** 0.1%

#### 📝 Định nghĩa:
Tỷ lệ phần trăm số lệnh có thời gian nắm giữ < 1 giờ.

#### 🧮 Công thức tính:
```python
scalp_ratio = (scalp_trades / total_trades) × 100

# Trong đó:
scalp_trades = COUNT(trades WHERE holding_hours < 1)
```

#### 📊 Cách tính từ CSV:
```python
# Đếm lệnh scalp
scalp_count = len(df[df['Holding_Hours'] < 1])

# Tính tỷ lệ
scalp_ratio = (scalp_count / total_trades) * 100

# Ví dụ:
# 65 lệnh < 1h / 100 lệnh = 65.0%
```

#### ✅ Validation:
- Min: 0.0% (không có scalp)
- Max: 100.0% (tất cả đều scalp)
- Độ chính xác: 1 chữ số thập phân

#### 💡 Ý nghĩa phân tích:
- `> 70%`: HIGH-FREQUENCY SCALPER
- `50-70%`: SCALPER
- `30-50%`: MIX (Scalp + Day)
- `< 30%`: SWING/POSITION TRADER

#### ⚠️ Lưu ý:
Scalp ratio cao thường đi kèm:
- Chi phí commission cao
- Stress cao
- Cần margin lớn
- Rủi ro overtrading

---

### 7. 📦 Tổng Khối Lượng (lots)
**Field Name:** `total_lots`
**Kiểu dữ liệu:** Float (0.0 - 100,000.0)
**Mặc định:** 10.0
**Bước nhảy:** 0.01

#### 📝 Định nghĩa:
Tổng khối lượng (volume) của tất cả các lệnh đã giao dịch.

#### 🧮 Công thức tính:
```python
total_lots = SUM(LOTS for all trades)
```

#### 📊 Cách tính từ CSV:
```python
# Tổng lots
total_lots = df['LOTS'].sum()

# Ví dụ:
# Trade 1: 0.1 lots
# Trade 2: 0.5 lots
# Trade 3: 1.0 lots
# Total: 1.6 lots
```

#### ✅ Validation:
- Min: 0.0 (không có giao dịch)
- Max: 100,000.0 (giới hạn hệ thống)
- Độ chính xác: 2 chữ số thập phân

#### 💡 Ý nghĩa phân tích:
- `< 5 lots`: Trader nhỏ lẻ
- `5-50 lots`: Retail trader bình thường
- `50-500 lots`: Professional trader
- `> 500 lots`: Institutional/High volume

#### 🎯 Average Lot Size:
```python
avg_lot_size = total_lots / total_trades

# Ví dụ:
# 50 lots / 100 trades = 0.5 lots/trade (average)
```

---

### 8. 🏆 Tài Sản Giao Dịch Chính
**Field Name:** `dominant_asset`
**Kiểu dữ liệu:** String (Text)
**Mặc định:** "XAUUSD"

#### 📝 Định nghĩa:
Symbol (mã tài sản) được giao dịch nhiều nhất.

#### 🧮 Công thức tính:
```python
dominant_asset = MODE(SYMBOL)
# Symbol xuất hiện nhiều nhất trong danh sách giao dịch
```

#### 📊 Cách tính từ CSV:
```python
# Đếm tần suất mỗi symbol
symbol_counts = df['SYMBOL'].value_counts()

# Lấy symbol đứng đầu
dominant_asset = symbol_counts.index[0]

# Ví dụ CSV:
# XAUUSD: 45 lệnh
# EURUSD: 30 lệnh
# GBPUSD: 25 lệnh
# → Dominant = "XAUUSD"
```

#### ✅ Validation:
- Không có ký tự đặc biệt (ngoại trừ dấu /)
- Uppercase recommended
- Độ dài: 3-10 ký tự

#### 💡 Các symbol phổ biến:
- **FOREX:** EURUSD, GBPUSD, USDJPY, AUDUSD
- **METALS:** XAUUSD (Gold), XAGUSD (Silver)
- **INDICES:** US30, NAS100, SPX500
- **CRYPTO:** BTCUSD, ETHUSD
- **COMMODITIES:** USOIL, UKOIL

#### 🎯 Asset Classes:
```python
def classify_asset(symbol):
    if 'XAU' in symbol or 'XAG' in symbol:
        return 'Metals'
    elif 'USD' in symbol and len(symbol) == 6:
        return 'Forex'
    elif any(x in symbol for x in ['US30', 'NAS', 'SPX']):
        return 'Indices'
    elif 'BTC' in symbol or 'ETH' in symbol:
        return 'Crypto'
    elif 'OIL' in symbol:
        return 'Commodities'
    else:
        return 'Other'
```

---

## 🎭 NHÓM 2: PHÂN BỐ PHONG CÁCH GIAO DỊCH (4 trường)

**⚠️ QUAN TRỌNG:** Tổng 4 trường này phải = 100.0%

### 9. ⚡ SCALP (< 1h) %
**Field Name:** `style_scalp`
**Kiểu dữ liệu:** Float (0.0 - 100.0%)
**Mặc định:** 60.0%

#### 📝 Định nghĩa:
Phần trăm giao dịch có holding time < 1 giờ.

#### 🧮 Công thức:
```python
style_scalp = (COUNT(trades WHERE holding_hours < 1) / total_trades) × 100
```

---

### 10. 📊 INTRADAY (1-8h) %
**Field Name:** `style_intraday`
**Kiểu dữ liệu:** Float (0.0 - 100.0%)
**Mặc định:** 30.0%

#### 📝 Định nghĩa:
Phần trăm giao dịch có holding time từ 1-8 giờ.

#### 🧮 Công thức:
```python
style_intraday = (COUNT(trades WHERE 1 ≤ holding_hours < 8) / total_trades) × 100
```

---

### 11. 📈 SWING (8h-7d) %
**Field Name:** `style_swing`
**Kiểu dữ liệu:** Float (0.0 - 100.0%)
**Mặc định:** 10.0%

#### 📝 Định nghĩa:
Phần trăm giao dịch có holding time từ 8 giờ đến 7 ngày (168 giờ).

#### 🧮 Công thức:
```python
style_swing = (COUNT(trades WHERE 8 ≤ holding_hours < 168) / total_trades) × 100
```

---

### 12. 📉 POSITION (> 7d) %
**Field Name:** `style_position`
**Kiểu dữ liệu:** Float (0.0 - 100.0%)
**Mặc định:** 0.0%

#### 📝 Định nghĩa:
Phần trăm giao dịch có holding time > 7 ngày (> 168 giờ).

#### 🧮 Công thức:
```python
style_position = (COUNT(trades WHERE holding_hours ≥ 168) / total_trades) × 100
```

---

### 📊 Cách tính đầy đủ từ CSV:

```python
# Phân loại từng lệnh
def classify_style(hours):
    if hours < 1:
        return 'SCALP'
    elif hours < 8:
        return 'INTRADAY'
    elif hours < 168:
        return 'SWING'
    else:
        return 'POSITION'

df['Style'] = df['Holding_Hours'].apply(classify_style)

# Đếm số lượng
scalp_count = len(df[df['Style'] == 'SCALP'])
intraday_count = len(df[df['Style'] == 'INTRADAY'])
swing_count = len(df[df['Style'] == 'SWING'])
position_count = len(df[df['Style'] == 'POSITION'])

# Tính phần trăm
style_scalp = (scalp_count / total_trades) * 100
style_intraday = (intraday_count / total_trades) * 100
style_swing = (swing_count / total_trades) * 100
style_position = (position_count / total_trades) * 100

# Validation
total_style = style_scalp + style_intraday + style_swing + style_position
assert abs(total_style - 100.0) < 0.1, "Total must be 100%"
```

### ✅ Validation Tổng Thể:
```python
total = style_scalp + style_intraday + style_swing + style_position

if abs(total - 100.0) > 0.1:
    raise ValueError(f"Tổng phải = 100%, hiện tại = {total}%")
```

---

## 📊 NHÓM 3: PHÂN BỐ TÀI SẢN TOP 3 (6 trường = 3 cặp)

### 13-14. Tài Sản #1
**Field Names:** `asset1_symbol`, `asset1_pct`

#### 📝 Định nghĩa:
Symbol được giao dịch nhiều nhất và phần trăm của nó.

#### 🧮 Công thức:
```python
asset_dist = df['SYMBOL'].value_counts(normalize=True) * 100

asset1_symbol = asset_dist.index[0]
asset1_pct = asset_dist.iloc[0]
```

#### Ví dụ:
```
asset1_symbol = "XAUUSD"
asset1_pct = 50.0%  # 50 lệnh XAUUSD / 100 lệnh
```

---

### 15-16. Tài Sản #2
**Field Names:** `asset2_symbol`, `asset2_pct`

#### 📝 Định nghĩa:
Symbol được giao dịch nhiều thứ 2.

#### 🧮 Công thức:
```python
asset2_symbol = asset_dist.index[1]
asset2_pct = asset_dist.iloc[1]
```

---

### 17-18. Tài Sản #3
**Field Names:** `asset3_symbol`, `asset3_pct`

#### 📝 Định nghĩa:
Symbol được giao dịch nhiều thứ 3.

#### 🧮 Công thức:
```python
asset3_symbol = asset_dist.index[2]
asset3_pct = asset_dist.iloc[2]
```

---

### 📊 Cách tính đầy đủ từ CSV:

```python
# Đếm và tính phần trăm
symbol_counts = df['SYMBOL'].value_counts()
total_trades = len(df)

# Top 3
top3 = symbol_counts.head(3)

# Asset 1
asset1_symbol = top3.index[0]
asset1_pct = (top3.iloc[0] / total_trades) * 100

# Asset 2
asset2_symbol = top3.index[1] if len(top3) > 1 else ""
asset2_pct = (top3.iloc[1] / total_trades) * 100 if len(top3) > 1 else 0

# Asset 3
asset3_symbol = top3.index[2] if len(top3) > 2 else ""
asset3_pct = (top3.iloc[2] / total_trades) * 100 if len(top3) > 2 else 0

# Ví dụ output:
# Asset 1: XAUUSD - 50.0%
# Asset 2: EURUSD - 30.0%
# Asset 3: GBPUSD - 20.0%
```

### ✅ Validation:
- Tổng 3 asset có thể < 100% (vì có thể có assets khác)
- Mỗi % phải >= 0
- asset1_pct >= asset2_pct >= asset3_pct (thứ tự giảm dần)

---

## 📋 BẢNG TỔNG HỢP TẤT CẢ TRƯỜNG

| # | Tên Trường | Field Name | Kiểu | Range | Mặc định | Bước |
|---|------------|------------|------|-------|----------|------|
| 1 | Tổng số giao dịch | `total_trades` | Integer | 1-10000 | 50 | 1 |
| 2 | Tỷ lệ thắng (%) | `win_rate` | Float | 0-100 | 55.0 | 0.1 |
| 3 | Profit Factor | `profit_factor` | Float | 0-100 | 1.5 | 0.01 |
| 4 | Net PnL (USD) | `net_pnl` | Float | -1M to 1M | 0.0 | 0.01 |
| 5 | Thời gian nắm giữ TB (h) | `avg_holding_hours` | Float | 0-720 | 2.5 | 0.1 |
| 6 | Tỷ lệ Scalp (%) | `scalp_ratio` | Float | 0-100 | 60.0 | 0.1 |
| 7 | Tổng khối lượng (lots) | `total_lots` | Float | 0-100k | 10.0 | 0.01 |
| 8 | Tài sản chính | `dominant_asset` | String | - | XAUUSD | - |
| 9 | SCALP (%) | `style_scalp` | Float | 0-100 | 60.0 | 0.1 |
| 10 | INTRADAY (%) | `style_intraday` | Float | 0-100 | 30.0 | 0.1 |
| 11 | SWING (%) | `style_swing` | Float | 0-100 | 10.0 | 0.1 |
| 12 | POSITION (%) | `style_position` | Float | 0-100 | 0.0 | 0.1 |
| 13 | Tài sản #1 | `asset1_symbol` | String | - | XAUUSD | - |
| 14 | % Tài sản #1 | `asset1_pct` | Float | 0-100 | 50.0 | 0.1 |
| 15 | Tài sản #2 | `asset2_symbol` | String | - | EURUSD | - |
| 16 | % Tài sản #2 | `asset2_pct` | Float | 0-100 | 30.0 | 0.1 |
| 17 | Tài sản #3 | `asset3_symbol` | String | - | GBPUSD | - |
| 18 | % Tài sản #3 | `asset3_pct` | Float | 0-100 | 20.0 | 0.1 |

---

## 🔗 MỐI QUAN HỆ GIỮA CÁC TRƯỜNG

### 1. Win Rate ↔ Profit Factor
```
Không tương quan trực tiếp!

Win Rate cao nhưng PF thấp:
- Thắng nhiều nhưng ít tiền
- Thua ít nhưng thua to
- Example: WR=70%, PF=0.8 → LOSING!

Win Rate thấp nhưng PF cao:
- Thắng ít nhưng thắng to
- Thua nhiều nhưng thua nhỏ
- Example: WR=35%, PF=2.5 → PROFITABLE!
```

### 2. Scalp Ratio ↔ Avg Holding Hours
```
Tương quan nghịch:

Scalp Ratio cao → Avg Holding Hours thấp
- SR=80% → AHH ≈ 0.5-1.5h

Scalp Ratio thấp → Avg Holding Hours cao
- SR=20% → AHH ≈ 10-50h
```

### 3. Trading Style Percentages
```
Phải tuân thủ:
SCALP + INTRADAY + SWING + POSITION = 100%

Ví dụ hợp lệ:
60% + 30% + 10% + 0% = 100% ✅

Ví dụ KHÔNG hợp lệ:
60% + 30% + 20% + 5% = 115% ❌
```

### 4. Total Lots ↔ Total Trades
```
Average Lot Size = Total Lots / Total Trades

Ví dụ:
- 100 lots / 100 trades = 1.0 lot/trade (heavy trader)
- 10 lots / 100 trades = 0.1 lot/trade (conservative)
```

---

## 🧮 SCRIPT PYTHON TÍNH TOÁN HOÀN CHỈNH

```python
import pandas as pd

def calc(f):
    d=pd.read_csv(f,encoding='utf-8-sig')
    d=standardize(d);d=clean(d)
    d['O']=pd.to_datetime(d['OPEN_TIME']);d['C']=pd.to_datetime(d['CLOSE_TIME'])
    d['H']=(d['C']-d['O']).dt.total_seconds()/3600
    d['NP']=d['PROFIT']+d.get('COMM',0).fillna(0)+d.get('SWAP',0).fillna(0)+d.get('TAXES',0).fillna(0)
    n=len(d);w=(len(d[d['PROFIT']>0])/n)*100
    pf=d[d['PROFIT']>0]['PROFIT'].sum()/abs(d[d['PROFIT']<0]['PROFIT'].sum()) if abs(d[d['PROFIT']<0]['PROFIT'].sum())>0 else 999
    sc=(len(d[d.H<1])/n)*100;intr=(len(d[(d.H>=1)&(d.H<8)])/n)*100
    sw=(len(d[(d.H>=8)&(d.H<168)])/n)*100;ps=(len(d[d.H>=168])/n)*100
    a=d['SYMBOL'].value_counts(normalize=True)*100
    return {'total_trades':int(n),'win_rate':round(w,1),'profit_factor':round(pf,2),
            'net_pnl':round(d.NP.sum(),2),'avg_holding_hours':round(d.H.mean(),1),
            'scalp_ratio':round(sc,1),'total_lots':round(d['LOTS'].sum(),2),
            'dominant_asset':d['SYMBOL'].value_counts().index[0],'style_scalp':round(sc,1),
            'style_intraday':round(intr,1),'style_swing':round(sw,1),'style_position':round(ps,1),
            'asset1_symbol':a.index[0] if len(a)>0 else "",'asset1_pct':round(a.iloc[0],1) if len(a)>0 else 0,
            'asset2_symbol':a.index[1] if len(a)>1 else "",'asset2_pct':round(a.iloc[1],1) if len(a)>1 else 0,
            'asset3_symbol':a.index[2] if len(a)>2 else "",'asset3_pct':round(a.iloc[2],1) if len(a)>2 else 0}
```

**Validation:** style_scalp+intraday+swing+position=100% | PF<1→PnL<0 | PF>1→PnL>0 | scalp>80%→avg_h<2h

---

## 📚 THAM KHẢO NHANH

### Giá trị "Tốt" cho mỗi metric:

| Metric | Newbie | Average | Good | Excellent |
|--------|--------|---------|------|-----------|
| Win Rate | <40% | 40-50% | 50-60% | >60% |
| Profit Factor | <1.0 | 1.0-1.3 | 1.3-2.0 | >2.0 |
| Scalp Ratio | >80% | 60-80% | 40-60% | <40% |
| Avg Holding | <0.5h | 0.5-2h | 2-24h | >24h |

---

**Tạo bởi:** GitHub Copilot  
**Ngày:** 2025-11-18  
**Version:** 1.0.0
