"""
Module tư vấn và tạo script sử dụng Google Gemini API
"""

import google.generativeai as genai
import streamlit as st
import json
from datetime import datetime
import os

class AdvisoryScriptGenerator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
        
        # HFM Promotion data (mẫu - có thể cập nhật từ nguồn khác)
        self.hfm_promotions = {
            "welcome_bonus": {
                "name": "Welcome Bonus 20%",
                "description": "Nhận thưởng 20% số tiền nạp đầu tiên, tối đa $2,000",
                "conditions": "Nạp tối thiểu $200, trading volume 2 lots/USD",
                "target": ["Newbie Gambler", "Technical Trader"],
                "benefits": "Tăng vốn giao dịch ban đầu"
            },
            "deposit_bonus": {
                "name": "Deposit Bonus 50%",
                "description": "Bonus 50% cho mỗi lần nạp tiền",
                "conditions": "Nạp tối thiểu $500, không rút được trong 30 ngày",
                "target": ["Technical Trader", "Part-time Trader"],
                "benefits": "Tăng đòn bẩy và khả năng giao dịch"
            },
            "cashback": {
                "name": "Daily Cashback",
                "description": "Hoàn tiền hàng ngày dựa trên volume giao dịch",
                "conditions": "Trade tối thiểu 1 lot/ngày",
                "target": ["Technical Trader", "Asset Specialist"],
                "benefits": "Giảm chi phí giao dịch"
            },
            "vip_program": {
                "name": "VIP Trading Program",
                "description": "Chương trình VIP với spread thấp và hỗ trợ 1:1",
                "conditions": "Deposit tối thiểu $10,000 hoặc volume > 100 lots/tháng",
                "target": ["Long-term Investor", "Asset Specialist"],
                "benefits": "Chi phí thấp, dịch vụ cao cấp"
            },
            "education": {
                "name": "Free Trading Education",
                "description": "Khóa học trading miễn phí và webinar hàng tuần",
                "conditions": "Mở tài khoản live và nạp tối thiểu $100",
                "target": ["Newbie Gambler", "Part-time Trader"],
                "benefits": "Nâng cao kiến thức và kỹ năng"
            },
            "copy_trading": {
                "name": "Copy Trading Platform",
                "description": "Copy giao dịch từ các trader chuyên nghiệp",
                "conditions": "Tài khoản tối thiểu $500",
                "target": ["Part-time Trader", "Long-term Investor"],
                "benefits": "Tiết kiệm thời gian, học hỏi kinh nghiệm"
            }
        }
    
    def generate_advisory_script(self, analysis_result, customer_info, promotions_filter=None):
        """
        Tạo script tư vấn cá nhân hóa dựa trên phân tích và thông tin khách hàng
        """
        if not self.model:
            return self._fallback_script(analysis_result, customer_info)
        
        try:
            # Chuẩn bị dữ liệu cho AI
            context = self._prepare_context(analysis_result, customer_info)
            
            # Tạo prompt cho Gemini
            prompt = self._create_advisory_prompt(context, promotions_filter)
            
            # Gọi Gemini API
            response = self.model.generate_content(prompt)
            
            # Xử lý response
            script_content = response.text
            
            # Bổ sung thông tin khuyến mại
            recommended_promotions = self._recommend_promotions(analysis_result['primary_trader_type'])
            
            return {
                "script": script_content,
                "promotions": recommended_promotions,
                "trader_type": analysis_result['primary_trader_type'],
                "key_points": self._extract_key_points(analysis_result),
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            st.error(f"Lỗi khi tạo script: {str(e)}")
            return self._fallback_script(analysis_result, customer_info)
    
    def _prepare_context(self, analysis_result, customer_info):
        """Chuẩn bị context cho AI"""
        primary_type = analysis_result['primary_trader_type']
        profile = analysis_result['trader_profile']
        insights = analysis_result['insights']
        metrics = analysis_result['metrics']
        
        context = {
            "trader_type": primary_type,
            "trader_name": profile['name'],
            "customer_info": {
                "age": customer_info.get('age'),
                "gender": customer_info.get('gender'),
                "experience": customer_info.get('experience_years'),
                "income": customer_info.get('income_range'),
                "capital": customer_info.get('capital_level'),
                "goal": customer_info.get('investment_goal'),
                "risk_tolerance": customer_info.get('risk_tolerance'),
                "time_available": customer_info.get('available_time'),
                "has_other_job": customer_info.get('has_other_job')
            },
            "trading_metrics": {
                "total_trades": metrics.get('total_trades'),
                "win_rate": round(metrics.get('win_rate', 0) * 100, 1),
                "profit_factor": round(metrics.get('profit_factor', 0), 2),
                "net_pnl": round(metrics.get('net_pnl', 0), 2),
                "avg_holding_hours": round(metrics.get('avg_holding_hours', 0), 1),
                "trades_per_day": round(metrics.get('trades_per_day', 0), 1)
            },
            "key_characteristics": insights.get('key_characteristics', []),
            "risk_level": insights.get('risk_assessment', {}).get('risk_level', 'UNKNOWN'),
            "recommendations": profile.get('advice', []),
            "risks": profile.get('risks', [])
        }
        
        return context
    
    def _create_advisory_prompt(self, context, promotions_filter=None):
        """Tạo prompt cho Gemini AI"""
        
        prompt = f"""
Bạn là Jill - một chuyên gia tư vấn tài chính thông minh và chuyên nghiệp tại HFM. 
Hãy tạo một script tư vấn cá nhân hóa cho khách hàng dựa trên thông tin sau:

THÔNG TIN KHÁCH HÀNG:
- Loại trader: {context['trader_type']} ({context['trader_name']})
- Tuổi: {context['customer_info']['age']}
- Giới tính: {context['customer_info']['gender']}
- Kinh nghiệm: {context['customer_info']['experience']}
- Thu nhập: {context['customer_info']['income']}
- Vốn đầu tư: {context['customer_info']['capital']}
- Mục tiêu: {context['customer_info']['goal']}
- Khẩu vị rủi ro: {context['customer_info']['risk_tolerance']}
- Thời gian có thể trading: {context['customer_info']['time_available']}
- Có công việc khác: {context['customer_info']['has_other_job']}

KỂT QUẢ PHÂN TÍCH GIAO DỊCH:
- Tổng số lệnh: {context['trading_metrics']['total_trades']}
- Win rate: {context['trading_metrics']['win_rate']}%
- Profit factor: {context['trading_metrics']['profit_factor']}
- Net PnL: ${context['trading_metrics']['net_pnl']}
- Thời gian nắm giữ TB: {context['trading_metrics']['avg_holding_hours']} giờ
- Tần suất giao dịch: {context['trading_metrics']['trades_per_day']} lệnh/ngày
- Mức độ rủi ro: {context['risk_level']}

ĐẶC ĐIỂM ĐƯỢC XÁC ĐỊNH:
{chr(10).join(['- ' + char for char in context['key_characteristics']])}

KHUYẾN NGHỊ CHÍNH:
{chr(10).join(['- ' + rec for rec in context['recommendations']])}

RỦI RO CẦN LƯU Ý:
{chr(10).join(['- ' + risk for risk in context['risks']])}

YÊU CẦU TẠO SCRIPT:
1. Tạo script tư vấn bằng tiếng Việt, thân thiện và chuyên nghiệp
2. Bắt đầu bằng lời chào và giới thiệu bản thân là Jill từ HFM
3. Tóm tắt phân tích hành vi giao dịch của khách hàng một cách tích cực
4. Đưa ra lời khuyên cụ thể dựa trên loại trader và đặc điểm
5. Đề xuất cách cải thiện hiệu quả giao dịch
6. Nhấn mạnh quản lý rủi ro phù hợp
7. Kết thúc bằng lời mời hợp tác và hỗ trợ tiếp theo
8. Script nên dài khoảng 300-500 từ
9. Sử dụng tone friendly, confident và supportive
10. Tránh sử dụng thuật ngữ quá chuyên môn

Hãy tạo script tư vấn hấp dẫn và thuyết phục, thể hiện sự hiểu biết sâu sắc về khách hàng.
"""
        
        return prompt
    
    def _recommend_promotions(self, trader_type):
        """Đề xuất chương trình khuyến mại phù hợp"""
        recommended = []
        
        for promo_id, promo_data in self.hfm_promotions.items():
            if trader_type in promo_data.get('target', []):
                recommended.append({
                    'id': promo_id,
                    'name': promo_data['name'],
                    'description': promo_data['description'],
                    'conditions': promo_data['conditions'],
                    'benefits': promo_data['benefits'],
                    'relevance_score': self._calculate_relevance_score(trader_type, promo_id)
                })
        
        # Sort by relevance score
        recommended.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return recommended[:3]  # Top 3 recommendations
    
    def _calculate_relevance_score(self, trader_type, promo_id):
        """Tính điểm phù hợp của chương trình khuyến mại"""
        score_map = {
            "Newbie Gambler": {
                "welcome_bonus": 95,
                "education": 90,
                "deposit_bonus": 70,
                "cashback": 60,
                "copy_trading": 50,
                "vip_program": 20
            },
            "Technical Trader": {
                "cashback": 95,
                "deposit_bonus": 85,
                "welcome_bonus": 75,
                "vip_program": 60,
                "education": 50,
                "copy_trading": 30
            },
            "Long-term Investor": {
                "vip_program": 95,
                "copy_trading": 80,
                "cashback": 70,
                "deposit_bonus": 50,
                "education": 40,
                "welcome_bonus": 30
            },
            "Part-time Trader": {
                "copy_trading": 95,
                "education": 85,
                "deposit_bonus": 75,
                "cashback": 65,
                "welcome_bonus": 55,
                "vip_program": 40
            },
            "Asset Specialist": {
                "vip_program": 90,
                "cashback": 85,
                "deposit_bonus": 70,
                "copy_trading": 60,
                "education": 50,
                "welcome_bonus": 40
            }
        }
        
        return score_map.get(trader_type, {}).get(promo_id, 50)
    
    def _extract_key_points(self, analysis_result):
        """Trích xuất các điểm chính để nhấn mạnh"""
        insights = analysis_result['insights']
        metrics = analysis_result['metrics']
        
        key_points = []
        
        # Win rate analysis
        win_rate = metrics.get('win_rate', 0) * 100
        if win_rate >= 60:
            key_points.append(f"Win rate tốt ({win_rate:.1f}%) - duy trì và cải thiện")
        elif win_rate >= 45:
            key_points.append(f"Win rate ổn định ({win_rate:.1f}%) - có thể tối ưu thêm")
        else:
            key_points.append(f"Win rate cần cải thiện ({win_rate:.1f}%) - tập trung vào chất lượng lệnh")
        
        # Profit factor analysis
        pf = metrics.get('profit_factor', 0)
        if pf >= 1.5:
            key_points.append("Profit factor xuất sắc - chiến lược hiệu quả")
        elif pf >= 1.0:
            key_points.append("Profit factor khả quan - cần tối ưu risk/reward")
        else:
            key_points.append("Profit factor cần cải thiện - xem xét lại strategy")
        
        # Risk level
        risk_level = insights.get('risk_assessment', {}).get('risk_level', 'UNKNOWN')
        if risk_level == 'CAO':
            key_points.append("Cần giảm mức độ rủi ro và quản lý vốn chặt chẽ")
        elif risk_level == 'TRUNG BÌNH':
            key_points.append("Mức rủi ro hợp lý - duy trì kỷ luật")
        else:
            key_points.append("Quản lý rủi ro tốt - có thể tối ưu lợi nhuận")
        
        return key_points
    
    def _fallback_script(self, analysis_result, customer_info):
        """Script dự phòng khi không thể dùng AI"""
        primary_type = analysis_result['primary_trader_type']
        profile = analysis_result['trader_profile']
        metrics = analysis_result['metrics']
        
        script = f"""
Xin chào! Tôi là Jill từ HFM, rất vui được hỗ trợ bạn.

Sau khi phân tích lịch sử giao dịch của bạn, tôi nhận thấy bạn thuộc nhóm "{profile['name']}".

📊 Tóm tắt hiệu quả:
- Tổng số lệnh: {metrics.get('total_trades', 0):,}
- Tỷ lệ thắng: {metrics.get('win_rate', 0)*100:.1f}%
- Profit Factor: {metrics.get('profit_factor', 0):.2f}
- Net PnL: ${metrics.get('net_pnl', 0):.2f}

🎯 Khuyến nghị cho bạn:
{chr(10).join(['• ' + advice for advice in profile.get('advice', [])])}

⚠️ Lưu ý quan trọng:
{chr(10).join(['• ' + risk for risk in profile.get('risks', [])])}

Tôi sẵn sàng hỗ trợ bạn tối ưu chiến lược giao dịch và đạt được mục tiêu đầu tư. 
Hãy liên hệ để được tư vấn chi tiết hơn!

Trân trọng,
Jill - HFM Trading Advisor
"""
        
        return {
            "script": script,
            "promotions": self._recommend_promotions(primary_type),
            "trader_type": primary_type,
            "key_points": self._extract_key_points(analysis_result),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def explain_promotion_selection(self, trader_type, selected_promotions):
        """Giải thích lý do chọn chương trình khuyến mại"""
        if not self.model:
            return self._fallback_explanation(trader_type, selected_promotions)
        
        try:
            promo_details = []
            for promo in selected_promotions:
                promo_details.append(f"- {promo['name']}: {promo['description']}")
            
            prompt = f"""
Bạn là chuyên gia tư vấn HFM. Hãy giải thích ngắn gọn tại sao các chương trình khuyến mại sau 
phù hợp với trader thuộc nhóm "{trader_type}":

{chr(10).join(promo_details)}

Yêu cầu:
1. Giải thích bằng tiếng Việt
2. Ngắn gọn, súc tích (100-150 từ)
3. Tập trung vào lợi ích cụ thể cho loại trader này
4. Tone chuyên nghiệp, thuyết phục
"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return self._fallback_explanation(trader_type, selected_promotions)
    
    def _fallback_explanation(self, trader_type, selected_promotions):
        """Giải thích dự phòng"""
        explanations = {
            "Newbie Gambler": "Các chương trình này giúp tăng vốn ban đầu và cung cấp kiến thức cần thiết cho trader mới.",
            "Technical Trader": "Các ưu đãi này tối ưu chi phí giao dịch và hỗ trợ strategy giao dịch tích cực.",
            "Long-term Investor": "Chương trình VIP và copy trading phù hợp với mục tiêu đầu tư dài hạn.",
            "Part-time Trader": "Các dịch vụ này giúp tiết kiệm thời gian và học hỏi hiệu quả.",
            "Asset Specialist": "Ưu đãi chuyên biệt dành cho trader có chuyên môn sâu."
        }
        
        return explanations.get(trader_type, "Các chương trình được chọn phù hợp với đặc điểm giao dịch của bạn.")

# Export
__all__ = ['AdvisoryScriptGenerator']