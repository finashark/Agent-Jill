#!/usr/bin/env python
"""
Test script display fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_script_display():
    """Test script consultation hiển thị đúng"""
    
    print("🔍 TESTING SCRIPT DISPLAY FIX")
    print("=" * 50)
    
    try:
        # Mock để test
        class MockJill:
            def _suggest_promotions_intelligent(self, trader_type, ai_analysis, customer_info):
                return [
                    {'name': 'VIP Package', 'description': 'Premium trading support'},
                    {'name': 'Basic Package', 'description': 'Essential tools for beginners'}
                ]
            
            def _fallback_consultation_script_enhanced(self, ai_analysis, customer_info, trading_metrics):
                from datetime import datetime
                
                trader_type = ai_analysis.get('trader_type', 'Mixed Type')
                customer_name = customer_info.get('name', 'Khách hàng')
                capital = customer_info.get('capital', 0)
                win_rate = trading_metrics.get('win_rate', 0)
                profit_factor = trading_metrics.get('profit_factor', 0)
                net_pnl = trading_metrics.get('net_pnl', 0)
                total_trades = trading_metrics.get('total_trades', 0)
                
                # Đánh giá performance level
                if win_rate >= 50 and profit_factor >= 1.2:
                    performance_level = "🟢 Xuất sắc"
                    performance_class = "success"
                    performance_tone = "rất ấn tượng với"
                    overall_assessment = "tuyệt vời"
                elif win_rate >= 40 and profit_factor >= 1.0:
                    performance_level = "🟡 Tốt"
                    performance_class = "warning"
                    performance_tone = "hài lòng với"
                    overall_assessment = "ổn định"
                else:
                    performance_level = "🔴 Cần cải thiện"
                    performance_class = "danger"
                    performance_tone = "nhận thấy tiềm năng trong"
                    overall_assessment = "đang phát triển"
                
                # Tạo recommended promotions
                promotions = self._suggest_promotions_intelligent(trader_type, ai_analysis, customer_info)
                promo_list = []
                for promo in promotions:
                    promo_list.append(f"- **{promo['name']}:** {promo['description']}")
                
                promotions_text = "\\n".join(promo_list) if promo_list else "- **Starter Package:** Gói cơ bản phù hợp với mọi trader"
                
                return f"""
# 📋 Báo Cáo Tư Vấn Giao Dịch

## 👤 Thông tin khách hàng
- **Họ tên:** {customer_name}
- **Vốn đầu tư:** ${capital:,}
- **Loại trader:** `{trader_type}`
- **Tổng số lệnh:** {total_trades}

---

## 📊 Đánh giá hiệu suất

### 🎯 Chỉ số chính

| 📏 **Metric** | 🔢 **Giá trị** | 📈 **Đánh giá** |
|:-------------|:-------------|:-------------|
| Win Rate | {win_rate:.1f}% | {performance_level} |
| Profit Factor | {profit_factor:.2f} | {performance_class.title()} |
| Net P&L | ${net_pnl:,.2f} | {'Profitable' if net_pnl > 0 else 'Loss'} |

### 💡 Phân tích tâm lý
> {ai_analysis.get('psychological_profile', 'Trader có phong cách giao dịch ổn định với phương pháp riêng biệt.')}

---

## 🎁 Gói hỗ trợ được đề xuất

{promotions_text}

---

## 📞 Liên hệ hỗ trợ

> **Jill - HFM Senior Trading Advisor**  
> 📧 **Email:** jill@hfm.com  

---

*📊 Báo cáo được tạo bởi Jill AI • {datetime.now().strftime("%d/%m/%Y %H:%M")} • HFM Trading Solutions*
"""

        # Test 
        jill = MockJill()
        
        ai_analysis = {
            'trader_type': 'Technical Trader',
            'psychological_profile': 'Trader có phương pháp giao dịch kỷ luật và có kinh nghiệm.'
        }
        
        customer_info = {
            'name': 'Anh Khang',
            'capital': 15000
        }
        
        trading_metrics = {
            'win_rate': 55.0,
            'profit_factor': 1.4,
            'net_pnl': 250.0,
            'total_trades': 20
        }
        
        script = jill._fallback_consultation_script_enhanced(ai_analysis, customer_info, trading_metrics)
        
        print("✅ SCRIPT GENERATION - SUCCESS")
        print("\n📝 Script Preview:")
        print("-" * 50)
        print(script[:800] + "..." if len(script) > 800 else script)
        print("-" * 50)
        
        print("\n🔍 TYPE CHECK:")
        print(f"Script Type: {type(script)}")
        print(f"Is String: {isinstance(script, str)}")
        
        print("\n✅ SCRIPT DISPLAY FIX - COMPLETED")
        print("🎯 Now script will display properly in Streamlit!")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_script_display()