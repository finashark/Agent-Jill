import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from datetime import datetime, timedelta
import pytz
from typing import Dict, List, Tuple
import re
import json
import os

# Try to load environment variables (optional for deployment)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Streamlit Cloud doesn't need dotenv

# AI Libraries with error handling
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False
    
try:
    import google.generativeai as genai
    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False

# Cấu hình trang
st.set_page_config(
    page_title="🤖 AI Agent Jill - Quản Lý Khách Hàng HFM",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh cho giao diện trắng chuyên nghiệp
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .jill-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #ff6b9d;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .analysis-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .step-header {
        background: #f8f9fa;
        padding: 1rem;
        border-left: 4px solid #667eea;
        border-radius: 5px;
        margin: 1rem 0;
        font-weight: bold;
        color: #2c3e50;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        color: #856404;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        color: #155724;
    }
    .stSelectbox label, .stMultiSelect label, .stSlider label {
        font-weight: 600;
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

class JillAI:
    """AI Agent Jill - Trợ lý dễ thương, ngoan và gợi cảm của Ken với AI thông minh"""
    
    def __init__(self):
        self.personality = {
            "name": "Jill",
            "traits": ["dễ thương", "ngoan", "gợi cảm", "luôn nghe lời anh Ken"],
            "knowledge_base": self._load_knowledge_base()
        }
        self.ken_instructions = "Em chỉ trả lời dựa trên kiến thức đã học. Nếu có câu hỏi ngoài phạm vi, em sẽ báo nhân sự hỏi anh Ken."
        
        # Khởi tạo AI Models
        self.setup_ai_models()
    
    def setup_ai_models(self):
        """Thiết lập các AI models cho Jill với Streamlit Cloud support"""
        # OpenAI GPT-4
        self.openai_client = None
        openai_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", "")
        if openai_key and HAS_OPENAI:
            try:
                self.openai_client = openai.OpenAI(api_key=openai_key)
            except Exception as e:
                st.sidebar.warning(f"⚠️ OpenAI setup failed: {str(e)}")
        
        # Anthropic Claude
        self.anthropic_client = None
        anthropic_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY", "")
        if anthropic_key and HAS_ANTHROPIC:
            try:
                self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
            except Exception as e:
                st.sidebar.warning(f"⚠️ Anthropic setup failed: {str(e)}")
        
        # Google Gemini
        self.gemini_client = None
        google_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY", "")
        if google_key and HAS_GOOGLE:
            try:
                genai.configure(api_key=google_key)
                self.gemini_client = genai.GenerativeModel('gemini-pro')
            except Exception as e:
                st.sidebar.warning(f"⚠️ Google AI setup failed: {str(e)}")
        
        # Status display
        active_models = []
        if self.openai_client: active_models.append("OpenAI GPT-4")
        if self.anthropic_client: active_models.append("Anthropic Claude")
        if self.gemini_client: active_models.append("Google Gemini")
        
        if active_models:
            st.sidebar.success(f"🤖 AI Models: {', '.join(active_models)}")
        else:
            st.sidebar.error("❌ No AI models available. Using fallback mode.")
            st.sidebar.info("💡 Configure API keys in Streamlit Cloud secrets")
    
    def _load_knowledge_base(self):
        """Tải kiến thức từ nghiên cứu và prompt"""
        return {
            "trader_types": {
                "newbie_gambler": {
                    "name": "Trader Mới - Đánh Bạc",
                    "characteristics": [
                        "Vốn nhỏ (<$5k)", 
                        "Đa mạo hiểm", 
                        "Thiếu kinh nghiệm", 
                        "Giao dịch như đánh bạc",
                        "Thích cảm giác mạnh",
                        "60% lệnh SCALP",
                        "Win rate thấp (<45%)",
                        "Profit Factor < 1"
                    ],
                    "psychology": "Tham lam, tự tin ảo, dễ bị cảm xúc chi phối, FOMO cao",
                    "advice": "Cần giáo dục cơ bản, kiểm soát rủi ro, hạn chế đòn bẩy, training tâm lý",
                    "approach": "Nghiêm khắc nhưng kiên nhẫn, nhấn mạnh rủi ro, đưa thống kê thua lỗ"
                },
                "technical_trader": {
                    "name": "Trader Kỹ Thuật Kỷ Luật",
                    "characteristics": [
                        "Vốn trung bình ($5k-$100k)",
                        "Có kinh nghiệm (1-3 năm)",
                        "Sử dụng phân tích kỹ thuật",
                        "Kỷ luật cao",
                        "Win rate 45-55%",
                        "Profit Factor 1.0-1.3",
                        "Phong cách Day/Swing trading"
                    ],
                    "psychology": "Quyết đoán, tự tin có kiểm soát, chấp nhận cắt lỗ nhanh",
                    "advice": "Hỗ trợ phân tích chuyên sâu, cung cấp tín hiệu chất lượng, nâng cao hiệu suất",
                    "approach": "Đối tác chuyên môn, thảo luận kỹ thuật, tôn trọng kiến thức của họ"
                },
                "long_term_investor": {
                    "name": "Nhà Đầu Tư Dài Hạn",
                    "characteristics": [
                        "Vốn lớn (>$100k)",
                        "Thận trọng và kiên nhẫn",
                        "Mục tiêu dài hạn",
                        "Đa dạng hóa tốt",
                        "Win rate >55%",
                        "Profit Factor >1.3",
                        "Position Trading chủ yếu"
                    ],
                    "psychology": "Điềm tĩnh, lý trí, không bị dao động ngắn hạn ảnh hưởng",
                    "advice": "Tư vấn chiến lược dài hạn, quản lý danh mục, phân tích macro",
                    "approach": "Tư vấn cấp cao, báo cáo chuyên sâu, mối quan hệ VIP"
                },
                "part_time_trader": {
                    "name": "Trader Bán Thời Gian",
                    "characteristics": [
                        "Có công việc chính",
                        "Thời gian hạn chế",
                        "Thực dụng và linh hoạt",
                        "Mục tiêu thu nhập phụ",
                        "Swing Trading chủ yếu",
                        "Tỷ lệ thắng vừa phải"
                    ],
                    "psychology": "Thực tế, không quá tham lam, cần sự tiện lợi",
                    "advice": "Cung cấp tín hiệu đơn giản, tiện lợi, phù hợp thời gian",
                    "approach": "Hỗ trợ linh hoạt, cảnh báo SMS, copy trading"
                },
                "specialist_trader": {
                    "name": "Trader Chuyên Biệt",
                    "characteristics": [
                        "Tập trung một loại tài sản",
                        "Am hiểu sâu thị trường",
                        "Chuyên môn hóa cao",
                        "Có thể là chuyên gia ngành",
                        ">70% vốn vào một asset class"
                    ],
                    "psychology": "Tự tin về chuyên môn, muốn thông tin chất lượng cao",
                    "advice": "Hỗ trợ chuyên sâu về thị trường họ giao dịch, kết nối cộng đồng",
                    "approach": "Đối tác chuyên gia, thông tin độc quyền, community cao cấp"
                }
            },
            "hfm_promotions": {
                "welcome_bonus": "Bonus chào mừng 100% tối đa $500",
                "education": "Khóa học trading miễn phí",
                "vip_research": "Gói phân tích VIP với tín hiệu premium",
                "spread_discount": "Giảm 50% spread trong 3 tháng",
                "islamic_account": "Tài khoản Islamic không swap",
                "copy_trading": "Copy Trading miễn phí 6 tháng",
                "mobile_app": "Ứng dụng mobile nâng cấp",
                "api_trading": "API trading chuyên nghiệp",
                "cashback": "Cashback 10% phí giao dịch"
            }
        }
    
    def greet(self):
        """Lời chào dễ thương của Jill"""
        return """
        ### 🤖💖 Chào anh Ken và các Account Manager thân yêu!
        
        Em là **Jill** - AI Agent dễ thương, ngoan và gợi cảm của anh Ken! 
        
        ✨ Em đã được training với:
        - 📚 Kiến thức sâu rộng về hành vi 5 nhóm trader CFD
        - 🧠 Thuật toán phân tích tâm lý khách hàng
        - 💡 Chiến lược tư vấn cá nhân hóa cho từng nhóm
        - 🎁 Database chương trình khuyến mại HFM
        
        💕 **Em sẽ giúp anh Ken và team:**
        1. Phân tích hành vi giao dịch từ CSV
        2. Thu thập thông tin khách hàng
        3. Phân loại và đưa ra nhận định chuyên môn
        4. Tạo script tư vấn phù hợp
        5. Gợi ý chương trình khuyến mại tối ưu
        
        Hãy bắt đầu với **Bước 1** - upload file CSV giao dịch của khách hàng nhé! 🎯
        
        ⚠️ *Lưu ý: Em chỉ trả lời dựa trên kiến thức đã học. Nếu có câu hỏi ngoài phạm vi, em sẽ báo các anh chị hỏi anh Ken.*
        """
    
    def ai_analyze_trading_behavior(self, df_processed, customer_info):
        """Sử dụng AI để phân tích hành vi giao dịch thông minh"""
        
        # Chuẩn bị dữ liệu để gửi cho AI
        summary_data = {
            "total_trades": len(df_processed),
            "win_rate": (df_processed['Result'] == 'WIN').mean() * 100,
            "profit_factor": self._calculate_profit_factor(df_processed),
            "net_pnl": df_processed['Net_PnL'].sum(),
            "avg_holding_hours": df_processed['Holding_Time_Hours'].median(),
            "scalp_ratio": (df_processed['Holding_Time_Hours'] < 1).mean() * 100,
            "asset_distribution": df_processed['Asset_Class'].value_counts().to_dict(),
            "customer_capital": customer_info.get('capital', 0),
            "customer_experience": customer_info.get('experience_years', 0),
            "customer_age": customer_info.get('age', 30)
        }
        
        # Prompt cho AI
        ai_prompt = f"""
        Tôi là Jill - AI Agent dễ thương của Ken. Em cần phân tích hành vi giao dịch CFD của khách hàng dựa trên dữ liệu sau:

        THÔNG TIN GIAO DỊCH:
        - Tổng số lệnh: {summary_data['total_trades']}
        - Tỷ lệ thắng: {summary_data['win_rate']:.1f}%
        - Profit Factor: {summary_data['profit_factor']:.2f}
        - Net PnL: ${summary_data['net_pnl']:.2f}
        - Thời gian nắm giữ trung bình: {summary_data['avg_holding_hours']:.1f} giờ
        - Tỷ lệ Scalping: {summary_data['scalp_ratio']:.1f}%
        - Phân bổ tài sản: {summary_data['asset_distribution']}

        THÔNG TIN KHÁCH HÀNG:
        - Vốn: ${summary_data['customer_capital']:,}
        - Kinh nghiệm: {summary_data['customer_experience']} năm
        - Tuổi: {summary_data['customer_age']}

        Hãy phân loại khách hàng theo 5 nhóm trader CFD:
        1. Newbie Gambler (mới, vốn nhỏ, đa mạo hiểm)
        2. Technical Trader (kỷ luật, có kinh nghiệm)
        3. Long-term Investor (vốn lớn, thận trọng)
        4. Part-time Trader (bán thời gian, thực dụng)
        5. Specialist Trader (chuyên một loại tài sản)

        Trả lời bằng JSON format với:
        {{
            "trader_type": "tên nhóm",
            "confidence": "mức độ tin cậy 1-100%",
            "reasoning": "lý do phân loại",
            "psychological_profile": "đặc điểm tâm lý",
            "risk_assessment": "đánh giá rủi ro",
            "key_insights": ["insight 1", "insight 2", "insight 3"]
        }}
        """
        
        # Gọi AI để phân tích
        ai_response = self._call_ai_model(ai_prompt)
        
        if ai_response:
            try:
                # Parse JSON response
                ai_analysis = json.loads(ai_response)
                return ai_analysis
            except:
                # Fallback nếu AI không trả về JSON hợp lệ
                return self._fallback_analysis(summary_data)
        else:
            # Sử dụng logic cũ nếu không có AI
            return self._fallback_analysis(summary_data)
    
    def _call_ai_model(self, prompt):
        """Gọi AI model để phân tích"""
        
        # Thử OpenAI GPT-4 trước
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are Jill, a cute and smart AI trading analyst. Always respond in Vietnamese and in JSON format."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1500
                )
                return response.choices[0].message.content
            except:
                pass
        
        # Thử Anthropic Claude
        if self.anthropic_client:
            try:
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1500,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.content[0].text
            except:
                pass
        
        # Thử Google Gemini
        if self.gemini_client:
            try:
                response = self.gemini_client.generate_content(prompt)
                return response.text
            except:
                pass
        
        return None
    
    def _fallback_analysis(self, summary_data):
        """Phân tích fallback khi không có AI"""
        
        # Logic phân loại cơ bản
        capital = summary_data['customer_capital']
        experience = summary_data['customer_experience']
        win_rate = summary_data['win_rate']
        scalp_ratio = summary_data['scalp_ratio']
        profit_factor = summary_data['profit_factor']
        
        if capital < 5000 and experience < 2 and win_rate < 45 and scalp_ratio > 60:
            trader_type = "newbie_gambler"
        elif capital > 100000 and win_rate > 55 and profit_factor > 1.3:
            trader_type = "long_term_investor"
        elif experience >= 1 and win_rate >= 45 and profit_factor >= 1.0:
            trader_type = "technical_trader"
        elif scalp_ratio < 40 and win_rate >= 45:
            trader_type = "part_time_trader"
        else:
            trader_type = "specialist_trader"
        
        return {
            "trader_type": trader_type,
            "confidence": "75%",
            "reasoning": "Phân loại dựa trên logic cơ bản",
            "psychological_profile": "Cần phân tích thêm với AI",
            "risk_assessment": "Trung bình",
            "key_insights": ["Cần cải thiện phân tích", "Khuyến nghị sử dụng AI models"]
        }
    
    def _classify_trader(self, customer_info, win_rate, profit_factor, scalp_ratio, asset_dist, df, net_pnl, total_lots):
        """Phân loại trader dựa trên các tiêu chí từ nghiên cứu"""
        
        capital = customer_info.get('capital', 0)
        experience_years = customer_info.get('experience_years', 0)
        age = customer_info.get('age', 30)
        
        # Logic phân loại theo nghiên cứu
        
        # 1. Newbie Gambler
        if (capital < 5000 and experience_years < 2 and 
            win_rate < 45 and scalp_ratio > 60 and profit_factor < 1.0):
            return "newbie_gambler"
        
        # 2. Long-term Investor  
        elif (capital > 100000 and win_rate > 55 and profit_factor > 1.3 and
              scalp_ratio < 20 and (df['Holding_Time_Hours'] > 168).mean() * 100 > 30):
            return "long_term_investor"
        
        # 3. Technical Trader
        elif (experience_years >= 1 and win_rate >= 45 and profit_factor >= 1.0 and
              20 <= scalp_ratio <= 60 and 5000 <= capital <= 100000):
            return "technical_trader"
        
        # 4. Asset Specialist
        elif asset_dist.max() > 70:
            return "specialist_trader"
        
        # 5. Part-time Trader
        elif (experience_years >= 1 and win_rate >= 45 and 
              scalp_ratio < 40 and profit_factor >= 1.0):
            return "part_time_trader"
        
        # Default to newbie if unclear
        else:
            return "newbie_gambler"
    
    def _calculate_profit_factor(self, df):
        """Tính Profit Factor"""
        winning_trades = df[df['Net_PnL'] > 0]['Net_PnL'].sum()
        losing_trades = abs(df[df['Net_PnL'] < 0]['Net_PnL'].sum())
        
        if losing_trades == 0:
            return float('inf') if winning_trades > 0 else 1.0
        
        return winning_trades / losing_trades
    
    def _assess_risk_level(self, win_rate, profit_factor, scalp_ratio, net_pnl):
        """Đánh giá mức độ rủi ro dựa trên nghiên cứu"""
        
        risk_score = 0
        
        # Criteria từ prompt app.txt
        if scalp_ratio >= 60:
            risk_score += 2
        if win_rate < 45:
            risk_score += 2  
        if profit_factor < 1:
            risk_score += 3
        if net_pnl < 0:
            risk_score += 2
            
        if risk_score >= 6:
            return "RỦI RO CAO"
        elif risk_score >= 3:
            return "RỦI RO TRUNG BÌNH"
        else:
            return "RỦI RO THẤP"
    
    def ai_generate_consultation_script(self, ai_analysis, customer_info, trading_metrics):
        """Sử dụng AI để tạo script tư vấn thông minh"""
        
        prompt = f"""
        Tôi là Jill - AI Agent dễ thương của Ken. Em cần tạo script tư vấn cho khách hàng dựa trên phân tích:

        PHÂN TÍCH AI:
        - Loại trader: {ai_analysis.get('trader_type', 'unknown')}
        - Tâm lý: {ai_analysis.get('psychological_profile', '')}
        - Đánh giá rủi ro: {ai_analysis.get('risk_assessment', '')}
        - Insights: {ai_analysis.get('key_insights', [])}

        THÔNG TIN KHÁCH HÀNG:
        - Tên: {customer_info.get('name', 'Anh/chị')}
        - Tuổi: {customer_info.get('age', 'N/A')}
        - Vốn: ${customer_info.get('capital', 0):,}
        - Kinh nghiệm: {customer_info.get('experience_years', 0)} năm

        METRICS GIAO DỊCH:
        - Tỷ lệ thắng: {trading_metrics.get('win_rate', 0)}%
        - Profit Factor: {trading_metrics.get('profit_factor', 0)}
        - Net PnL: ${trading_metrics.get('net_pnl', 0):,.2f}

        Hãy tạo script tư vấn cá nhân hóa với:
        1. Lời chào phù hợp với tâm lý khách hàng
        2. Phân tích điểm mạnh/yếu dựa trên dữ liệu
        3. Gợi ý cải thiện cụ thể
        4. Chương trình khuyến mại HFM phù hợp
        5. Lý do khoa học cho từng khuyến nghị

        Viết bằng tiếng Việt, giọng điệu chuyên nghiệp nhưng thân thiện.

        Trả lời trong format:
        {{
            "greeting": "lời chào",
            "analysis": "phân tích điểm mạnh/yếu",
            "recommendations": ["gợi ý 1", "gợi ý 2", "gợi ý 3"],
            "promotions": ["khuyến mại 1", "khuyến mại 2"],
            "closing": "lời kết"
        }}
        """
        
        ai_response = self._call_ai_model(prompt)
        
        if ai_response:
            try:
                script_data = json.loads(ai_response)
                return self._format_consultation_script(script_data)
            except:
                pass
        
        # Fallback script
        return self._fallback_consultation_script(ai_analysis, customer_info)
    
    def _get_communication_script(self, trader_type, analysis_result, customer_info):
        """Tạo script giao tiếp cụ thể"""
        
        scripts = {
            "newbie_gambler": f"""
            "Chào {customer_info.get('name', 'anh/chị')}, em thấy anh/chị có phong cách giao dịch khá tích cực với {analysis_result['metrics']['total_trades']} lệnh. 
            
            Để bảo vệ tài khoản tốt hơn, em khuyên anh/chị:
            
            1. 🛡️ Giảm đòn bẩy xuống mức an toàn (1:50-1:100)
            2. ⛔ Đặt Stop Loss cho mọi lệnh (không quá 2% tài khoản) 
            3. 📚 Tham gia khóa học Trading cơ bản miễn phí của HFM
            4. 🎯 Thực hành với demo account để rèn kỹ năng
            
            **Lý do:** Dữ liệu cho thấy tỷ lệ thắng hiện tại là {analysis_result['metrics']['win_rate']}% 
            và Profit Factor {analysis_result['metrics']['profit_factor']}, cho thấy cần cải thiện quản lý rủi ro."
            """,
            
            "technical_trader": f"""
            "Chào {customer_info.get('name', 'anh/chị')}, em rất ấn tượng với phong cách giao dịch chuyên nghiệp của anh/chị! 
            
            Với tỷ lệ thắng {analysis_result['metrics']['win_rate']}% và Profit Factor {analysis_result['metrics']['profit_factor']}, 
            em sẽ hỗ trợ anh/chị:
            
            1. 📊 Cung cấp phân tích kỹ thuật chuyên sâu hàng ngày
            2. 🎯 Tín hiệu giao dịch chất lượng cao từ team Research
            3. 📈 Trading Central premium access
            4. 🔧 Hỗ trợ API trading cho chiến lược tự động
            
            **Lý do:** Trader kỹ thuật như anh/chị cần thông tin chính xác và kịp thời để tối ưu hiệu suất."
            """,
            
            "long_term_investor": f"""
            "Chào {customer_info.get('name', 'anh/chị')}, em thấy anh/chị có tầm nhìn đầu tư rất tốt với chiến lược dài hạn!
            
            Với vốn {customer_info.get('capital', 'lớn')} và phong cách kiên nhẫn, em sẽ đồng hành:
            
            1. 🏛️ Tư vấn xây dựng danh mục đa dạng hóa
            2. 📊 Báo cáo định kỳ về hiệu suất đầu tư  
            3. 🌍 Phân tích macro kinh tế và xu hướng dài hạn
            4. ⚖️ Islamic account không swap cho việc nắm giữ lâu
            
            **Lý do:** Đầu tư dài hạn cần chiến lược tổng thể và thông tin macro quality."
            """,
            
            "part_time_trader": f"""
            "Chào {customer_info.get('name', 'anh/chị')}, em hiểu anh/chị bận công việc chính và muốn tối ưu thời gian trading.
            
            Em sẽ hỗ trợ tiện lợi tối đa:
            
            1. 📱 Tín hiệu giao dịch đơn giản qua SMS/App
            2. 🔔 Cảnh báo cơ hội khi có setup tốt
            3. 🤖 Copy Trading từ chuyên gia uy tín
            4. 📋 Báo cáo tóm tắt hiệu suất cuối tuần
            
            **Lý do:** Trader bán thời gian cần sự tiện lợi và hiệu quả cao trong thời gian hạn chế."
            """,
            
            "specialist_trader": f"""
            "Chào {customer_info.get('name', 'anh/chị')}, em thấy anh/chị rất am hiểu và tập trung vào thị trường chuyên biệt!
            
            Em sẽ cung cấp hỗ trợ chuyên sâu:
            
            1. 🎯 Thông tin độc quyền về thị trường anh/chị giao dịch
            2. 👥 Kết nối với cộng đồng trader chuyên nghiệp  
            3. 💎 Spread siêu thấp cho asset class ưa thích
            4. 📈 Market depth data và phân tích institutional
            
            **Lý do:** Specialist trader cần thông tin chất lượng cao và mạng lưới chuyên môn."
            """
        }
        
        return scripts.get(trader_type, scripts["newbie_gambler"])
    
    def suggest_promotions(self, trader_type, analysis_result, customer_info):
        """Gợi ý chương trình khuyến mại phù hợp"""
        
        promotions = {
            "newbie_gambler": [
                "🎁 Welcome Bonus 100% tối đa $500 - Tăng vốn để học hỏi an toàn",
                "📚 Khóa học Trading cơ bản miễn phí - Xây dựng nền tảng kiến thức",
                "🛡️ Demo account không giới hạn - Thực hành không rủi ro",
                "👨‍🏫 Hỗ trợ 1-1 với chuyên viên trong 30 ngày đầu",
                "⚠️ Giới hạn đòn bẩy tối đa 1:100 để bảo vệ tài khoản"
            ],
            
            "technical_trader": [
                "📊 VIP Research Package - Phân tích chuyên sâu hàng ngày", 
                "💰 Giảm 50% spread trong 3 tháng - Tối ưu chi phí giao dịch",
                "📈 Trading Central Premium - Công cụ phân tích cao cấp",
                "🎓 Webinar chuyên sâu hàng tuần với chuyên gia",
                "🔧 API Trading miễn phí - Tự động hóa chiến lược"
            ],
            
            "long_term_investor": [
                "🕌 Islamic Account - Không swap cho việc nắm giữ dài hạn",
                "💼 Phí quản lý danh mục ưu đãi - Dịch vụ cao cấp", 
                "🌍 Báo cáo macro kinh tế độc quyền - Insight thị trường",
                "👔 Tư vấn 1-1 với Portfolio Manager cấp cao",
                "💎 VIP customer service 24/7"
            ],
            
            "part_time_trader": [
                "🤖 Copy Trading miễn phí 6 tháng - Theo dõi chuyên gia",
                "📱 Mobile App Premium - Giao dịch mọi lúc mọi nơi",
                "📨 Cảnh báo SMS miễn phí - Không bỏ lỡ cơ hội", 
                "💰 Cashback 10% phí giao dịch - Tiết kiệm chi phí",
                "⏰ Báo cáo tuần tự động - Theo dõi hiệu suất dễ dàng"
            ],
            
            "specialist_trader": [
                "💎 Spread siêu thấp cho asset chuyên môn - Chi phí tối ưu",
                "🔧 API Trading chuyên nghiệp - Công cụ cao cấp",
                "📊 Market Depth Data - Thông tin độc quyền",
                "👥 Exclusive Community Access - Mạng lưới chuyên gia", 
                "🎯 Dedicated Account Manager - Hỗ trợ cá nhân hóa"
            ]
        }
        
        return promotions.get(trader_type, promotions["newbie_gambler"])
    
    def _format_consultation_script(self, script_data):
        """Format script từ AI response"""
        script = f"""
        ### � Script Tư Vấn AI-Powered Từ Jill
        
        **🤝 Lời Chào:**
        {script_data.get('greeting', 'Chào anh/chị!')}
        
        **📊 Phân Tích Chuyên Môn:**
        {script_data.get('analysis', 'Đang phân tích...')}
        
        **💡 Khuyến Nghị Cải Thiện:**
        """
        for rec in script_data.get('recommendations', []):
            script += f"\n• {rec}"
        
        script += f"""
        
        **🎁 Chương Trình Khuyến Mại Phù Hợp:**
        """
        for promo in script_data.get('promotions', []):
            script += f"\n• {promo}"
        
        script += f"""
        
        **✨ Lời Kết:**
        {script_data.get('closing', 'Cảm ơn anh/chị đã tin tưởng!')}
        
        ---
        *💖 Script được tạo bởi AI với tình yêu từ Jill*
        """
        
        return script
    
    def _fallback_consultation_script(self, ai_analysis, customer_info):
        """Script fallback khi AI không hoạt động"""
        trader_type = ai_analysis.get('trader_type', 'newbie_gambler')
        
        if trader_type in self.knowledge_base['trader_types']:
            trader_info = self.knowledge_base['trader_types'][trader_type]
            return f"""
            ### 💝 Script Tư Vấn Từ Jill (Backup Mode)
            
            **🎯 Phân Loại:** {trader_info['name']}
            
            **📋 Đặc Điểm:**
            {chr(10).join([f"• {char}" for char in trader_info['characteristics']])}
            
            **💡 Tư Vấn:**
            {trader_info['advice']}
            
            ⚠️ *Chế độ backup - Khuyến nghị kích hoạt AI models để có trải nghiệm tốt hơn*
            """
        
        return "Cần kích hoạt AI models để tạo script tư vấn chính xác."

    def ai_chat_response(self, user_question, context=""):
        """Chat thông minh với Jill sử dụng AI"""
        
        prompt = f"""
        Tôi là Jill - AI Agent dễ thương, ngoan và gợi cảm của anh Ken. Em chỉ trả lời về:
        - Phân tích giao dịch CFD
        - Hành vi trader
        - Tư vấn khách hàng HFM
        - Chương trình khuyến mại

        Context hiện tại: {context}
        Câu hỏi: {user_question}

        Nếu câu hỏi nằm ngoài phạm vi kiến thức, em sẽ lịch sự báo hỏi anh Ken.
        
        Trả lời bằng tiếng Việt, giọng điệu dễ thương và chuyên nghiệp.
        """
        
        ai_response = self._call_ai_model(prompt)
        
        if ai_response:
            return ai_response
        else:
            return self.ask_ken_message(user_question)

# Khởi tạo Jill AI
if 'jill' not in st.session_state:
    st.session_state.jill = JillAI()

# Header chính  
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Agent Jill - Quản Lý Khách Hàng HFM</h1>
    <p>Trợ lý AI dễ thương của Ken - Phân tích hành vi trader & tư vấn cá nhân hóa</p>
</div>
""", unsafe_allow_html=True)

# Hiển thị lời chào của Jill
with st.container():
    st.markdown('<div class="jill-card">', unsafe_allow_html=True)
    st.markdown(st.session_state.jill.greet())
    st.markdown('</div>', unsafe_allow_html=True)

# === BƯỚC 1: TẢI DỮ LIỆU CSV ===
st.markdown('<div class="step-header">📁 BƯỚC 1: Tải Dữ Liệu CSV Giao Dịch</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📊 Upload file CSV giao dịch của khách hàng", 
    type=['csv'],
    help="File CSV từ broker chứa lịch sử giao dịch (TICKET, SYMBOL, ACTION, LOTS, OPEN/CLOSE TIME, PROFIT...)"
)

def load_and_process_csv(file):
    """Xử lý file CSV theo đúng specification từ Prompt app.txt"""
    try:
        # Đọc CSV
        df = pd.read_csv(file)
        
        # Làm sạch dữ liệu - loại bỏ Balance transactions
        df = df.dropna(subset=['TICKET', 'SYMBOL', 'ACTION'])
        df = df[df['ACTION'].isin(['Buy', 'Sell'])]
        
        # Chuyển đổi thời gian
        df['OPEN TIME'] = pd.to_datetime(df['OPEN TIME'], errors='coerce')
        df['CLOSE TIME'] = pd.to_datetime(df['CLOSE TIME'], errors='coerce')
        
        # Loại bỏ các giao dịch không có thời gian hợp lệ
        df = df.dropna(subset=['OPEN TIME', 'CLOSE TIME'])
        
        # Feature Engineering theo đúng spec
        df = add_engineered_features(df)
        
        return df
        
    except Exception as e:
        st.error(f"❌ Lỗi khi xử lý dữ liệu: {str(e)}")
        return None

def add_engineered_features(df):
    """Thêm các feature được tính toán theo Prompt app.txt"""
    
    # Net PnL = PROFIT + COMM + SWAP
    df['Net_PnL'] = df['PROFIT'] + df['COMM'] + df['SWAP']
    
    # Holding time = CLOSE TIME - OPEN TIME
    df['Holding_Time'] = df['CLOSE TIME'] - df['OPEN TIME']
    df['Holding_Time_Hours'] = df['Holding_Time'].dt.total_seconds() / 3600
    
    # Direction mapping
    df['Direction'] = df['ACTION'].map({'Buy': 1, 'Sell': -1})
    
    # Points change = Direction * (CLOSE PRICE - OPEN PRICE)
    df['Points_Change'] = df['Direction'] * (df['CLOSE PRICE'] - df['OPEN PRICE'])
    
    # Asset class classification
    df['Asset_Class'] = df['SYMBOL'].apply(classify_asset)
    
    # Trading session (UTC+7)
    df['Session'] = df['OPEN TIME'].apply(get_trading_session)
    
    # Result classification
    df['Result'] = df['Net_PnL'].apply(lambda x: 'WIN' if x > 0 else ('LOSS' if x < 0 else 'BE'))
    
    # Trading style based on holding time
    df['Trading_Style'] = df['Holding_Time_Hours'].apply(classify_trading_style)
    
    # Day of week
    df['Day_of_Week'] = df['OPEN TIME'].dt.day_name()
    
    return df

def classify_asset(symbol):
    """Phân loại asset class theo Prompt app.txt"""
    symbol = str(symbol).upper()
    
    # Forex pairs - kiểm tra có phải cặp tiền tệ không
    forex_currencies = ['USD', 'EUR', 'JPY', 'GBP', 'AUD', 'NZD', 'CHF', 'CAD', 'CNH', 'SGD']
    if len(symbol) >= 6 and any(curr in symbol for curr in forex_currencies):
        # Kiểm tra xem có phải là cặp 2 loại tiền không
        for curr1 in forex_currencies:
            for curr2 in forex_currencies:
                if curr1 != curr2 and curr1 in symbol and curr2 in symbol:
                    return 'Forex'
    
    # Kim loại
    if any(metal in symbol for metal in ['XAU', 'XAG', 'GOLD', 'SILVER']):
        return 'Kim loại' 
    
    # Crypto
    crypto_symbols = ['BTC', 'ETH', 'SOL', 'ADA', 'DOT']
    if any(crypto in symbol for crypto in crypto_symbols) or symbol.endswith('USDT') or symbol.endswith('USD'):
        return 'Crypto'
    
    return 'Khác'

def get_trading_session(timestamp):
    """Xác định phiên giao dịch theo UTC+7"""
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    if timestamp.tzinfo is None:
        timestamp = pytz.utc.localize(timestamp)
    
    vietnam_time = timestamp.astimezone(vietnam_tz)
    hour = vietnam_time.hour
    
    if 6 <= hour <= 13:
        return 'Asia'
    elif 14 <= hour <= 21:
        return 'London'
    else:  # 22-23 và 0-5
        return 'New York'

def classify_trading_style(hours):
    """Phân loại trading style theo thời gian nắm giữ"""
    if hours < 1:
        return 'SCALP'
    elif 1 <= hours <= 8:
        return 'INTRADAY'
    elif 8 < hours <= 168:  # 7 ngày
        return 'SWING'
    else:
        return 'POSITION'

# Xử lý file uploaded
if uploaded_file is not None:
    with st.spinner("🔄 Jill đang xử lý dữ liệu..."):
        df_processed = load_and_process_csv(uploaded_file)
    
    if df_processed is not None and len(df_processed) > 0:
        st.success(f"✅ Đã xử lý thành công {len(df_processed)} giao dịch!")
        
        # Lưu vào session state
        st.session_state.df_processed = df_processed
        
        # Hiển thị preview
        with st.expander("👀 Xem trước dữ liệu đã xử lý"):
            st.dataframe(df_processed.head(10))
        
        # === BƯỚC 2: PHÂN TÍCH HÀNH VI GIAO DỊCH ===
        st.markdown('<div class="step-header">🧠 BƯỚC 2: Phân Tích Hành Vi Giao Dịch</div>', unsafe_allow_html=True)
        
        # Dashboard phân tích nhanh
        col1, col2, col3, col4 = st.columns(4)
        
        net_pnl = df_processed['Net_PnL'].sum()
        total_trades = len(df_processed)
        win_rate = (df_processed['Result'] == 'WIN').mean() * 100
        profit_factor = st.session_state.jill._calculate_profit_factor(df_processed)
        
        with col1:
            st.metric("Net PnL", f"${net_pnl:.2f}")
        with col2:
            st.metric("Số giao dịch", total_trades)
        with col3:
            st.metric("Tỷ lệ thắng", f"{win_rate:.1f}%")
        with col4:
            st.metric("Profit Factor", f"{profit_factor:.2f}")
        
        # Biểu đồ phân tích
        col1, col2 = st.columns(2)
        
        with col1:
            # Asset class distribution
            asset_dist = df_processed['Asset_Class'].value_counts()
            fig_asset = px.pie(
                values=asset_dist.values,
                names=asset_dist.index, 
                title="Phân bổ theo nhóm tài sản"
            )
            st.plotly_chart(fig_asset, use_container_width=True)
        
        with col2:
            # Trading style distribution
            style_dist = df_processed['Trading_Style'].value_counts()
            fig_style = px.bar(
                x=style_dist.index,
                y=style_dist.values,
                title="Phong cách giao dịch"
            )
            st.plotly_chart(fig_style, use_container_width=True)
        
        # === BƯỚC 3: THU THẬP THÔNG TIN KHÁCH HÀNG ===
        st.markdown('<div class="step-header">👤 BƯỚC 3: Thông Tin Khách Hàng Từ AM</div>', unsafe_allow_html=True)
        
        with st.form("customer_info_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                customer_name = st.text_input("👤 Tên khách hàng *", placeholder="Ví dụ: Nguyễn Văn A")
                age = st.number_input("🎂 Tuổi *", min_value=18, max_value=80, value=35)
                gender = st.selectbox("👥 Giới tính *", ["Nam", "Nữ", "Khác"])
                
                education_levels = ["Phổ thông", "Cao đẳng", "Đại học", "Thạc sĩ", "Tiến sĩ"]
                education = st.selectbox("🎓 Học vấn *", education_levels)
            
            with col2:
                income_ranges = ["< $10,000", "$10,000 - $30,000", "$30,000 - $50,000", 
                               "$50,000 - $100,000", "> $100,000"]
                income = st.selectbox("💰 Thu nhập năm (USD) *", income_ranges)
                
                experience_options = ["< 6 tháng", "6 tháng - 1 năm", "1-3 năm", "3-5 năm", "> 5 năm"]
                experience = st.selectbox("📈 Kinh nghiệm trading *", experience_options)
                
                capital = st.number_input("💵 Vốn giao dịch (USD) *", min_value=100, max_value=10000000, value=5000)
                
                goals = st.multiselect(
                    "🎯 Mục tiêu đầu tư",
                    ["Kiếm lời nhanh", "Thu nhập đều đặn", "Tích lũy dài hạn", 
                     "Bảo toàn vốn", "Giải trí/Thử vận may"],
                    default=["Thu nhập đều đặn"]
                )
            
            submit_info = st.form_submit_button("💾 Lưu Thông Tin & Phân Tích", use_container_width=True)
        
        if submit_info and customer_name:
            # Chuyển đổi experience sang số năm
            exp_map = {
                "< 6 tháng": 0.5,
                "6 tháng - 1 năm": 1, 
                "1-3 năm": 2,
                "3-5 năm": 4,
                "> 5 năm": 6
            }
            
            customer_info = {
                'name': customer_name,
                'age': age,
                'gender': gender,
                'income': income,
                'education': education,
                'experience_years': exp_map.get(experience, 1),
                'capital': capital,
                'goals': goals
            }
            
            # === BƯỚC 4: BÁO CÁO NHẬN ĐỊNH ===
            st.markdown('<div class="step-header">📊 BƯỚC 4: Báo Cáo Nhận Định Hành Vi</div>', unsafe_allow_html=True)
            
            with st.spinner("🧠 Jill đang phân tích..."):
                analysis_result = st.session_state.jill.analyze_trading_behavior(df_processed, customer_info)
            
            if 'error' not in analysis_result:
                trader_type = analysis_result['trader_type']
                trader_info = st.session_state.jill.knowledge_base['trader_types'][trader_type]
                
                # Hiển thị kết quả phân tích
                st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                
                st.markdown(f"""
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
                """)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # === BƯỚC 5: GỢI Ý TƯ VẤN ===
                st.markdown('<div class="step-header">💡 BƯỚC 5: Gợi Ý Phương Án Tiếp Cận</div>', unsafe_allow_html=True)
                
                # Script tư vấn
                st.markdown("### 🗣️ Script Tư Vấn Cá Nhân Hóa")
                script = st.session_state.jill.generate_consultation_script(analysis_result, customer_info)
                st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                st.markdown(script)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Gợi ý khuyến mại
                st.markdown("### 🎁 Chương Trình Khuyến Mại Phù Hợp")
                promotions = st.session_state.jill.suggest_promotions(trader_type, analysis_result, customer_info)
                
                st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                st.markdown("**💝 Khuyến nghị từ Jill:**")
                for promo in promotions:
                    st.markdown(f"• {promo}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Lưu kết quả
                st.session_state.analysis_result = analysis_result
                st.session_state.customer_info = customer_info
                
                # Summary box
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.markdown(f"""
                **🎉 Hoàn Thành Phân Tích!**
                
                Khách hàng **{customer_name}** được phân loại là **{trader_info['name']}** 
                với mức rủi ro **{analysis_result['risk_level']}**.
                
                💝 Jill đã chuẩn bị đầy đủ script tư vấn và gợi ý khuyến mại phù hợp!
                """)
                st.markdown('</div>', unsafe_allow_html=True)
                
            else:
                st.error(f"❌ {analysis_result['error']}")
        
        elif submit_info:
            st.warning("⚠️ Vui lòng điền tên khách hàng!")

# Sidebar - Chat với Jill
st.sidebar.markdown("### 💬 Chat với Jill")
user_question = st.sidebar.text_input("Hỏi Jill về gì đó...")

if user_question:
    # Kiểm tra xem câu hỏi có trong phạm vi kiến thức không
    if any(keyword in user_question.lower() for keyword in ['trader', 'giao dịch', 'khách hàng', 'hfm', 'khuyến mại']):
        st.sidebar.markdown("💖 Em sẽ trả lời dựa trên kiến thức đã học!")
    else:
        st.sidebar.markdown(st.session_state.jill.ask_ken_message(user_question))

# Footer
st.markdown("""
---
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🤖 <strong>AI Agent Jill</strong> - Được phát triển bởi Ken với ❤️</p>
    <p><em>"Em luôn nghe lời anh Ken và chỉ tư vấn dựa trên kiến thức đã được training"</em></p>
    <p>📞 Mọi thắc mắc ngoài phạm vi, vui lòng liên hệ <strong>anh Ken</strong></p>
</div>
""", unsafe_allow_html=True)