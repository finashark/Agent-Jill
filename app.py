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
    anthropic = None
    
try:
    import google.generativeai as genai
    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False

# Cấu hình trang
st.set_page_config(
    page_title="🤖 AI Agent Jill - HFM Trading Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh cho giao diện trắng chuyên nghiệp
st.markdown("""
<style>
    /* Reset button styling */
    .reset-container {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 998;
    }
    
    .reset-btn {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 5px 15px rgba(40,167,69,0.3);
        transition: transform 0.3s ease;
    }
    
    .reset-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 20px rgba(40,167,69,0.4);
    }
    
    /* Existing styles */
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

<!-- Reset Button -->
<div class="reset-container">
    <button class="reset-btn" onclick="resetApp()">
        🔄 Tạo Mới
    </button>
</div>

<script>
function resetApp() {
    if (confirm('Bạn có chắc muốn tạo mới phân tích? Tất cả dữ liệu hiện tại sẽ bị xóa.')) {
        // Clear session storage
        sessionStorage.setItem('jill_reset_app', 'true');
        location.reload();
    }
}

// Auto-scroll chat to bottom
function scrollChatToBottom() {
    const chatBody = document.getElementById('chatBody');
    if (chatBody) {
        chatBody.scrollTop = chatBody.scrollHeight;
    }
}

// Initialize chat
document.addEventListener('DOMContentLoaded', function() {
    // Check for reset flag
    if (sessionStorage.getItem('jill_reset_app') === 'true') {
        sessionStorage.removeItem('jill_reset_app');
        // Clear all Streamlit session state
        window.parent.postMessage({ type: 'clear_session' }, '*');
    }
});
</script>
""", unsafe_allow_html=True)

class JillAI:
    """AI Agent Jill - Trợ lý phân tích trading chuyên nghiệp với AI thông minh"""
    
    def __init__(self):
        self.personality = {
            "name": "Jill",
            "traits": ["chuyên nghiệp", "khách quan", "chính xác", "hiệu quả"],
            "knowledge_base": self._load_knowledge_base()
        }
        self.professional_note = "Tôi chỉ phân tích dựa trên dữ liệu và kiến thức chuyên môn. Các câu hỏi ngoài phạm vi vui lòng tham khảo chuyên gia tài chính."
        
        # Khởi tạo AI Models
        self.setup_ai_models()
    
    def display_profile_ui(self):
        """Hiển thị profile với UI đặc biệt cho main interface"""
        
        # Header profile với styling chuyên nghiệp
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 2rem;">
            <h1 style="color: white; margin: 0; font-size: 2.5rem;">👩‍💼 Profile - AI Agent Jill</h1>
            <p style="color: #e8f4fd; margin: 0.5rem 0 0 0; font-size: 1.2rem;">
                📊 AI Trading Analysis Specialist
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Ảnh đại diện với fallback system
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            try:
                # Hiển thị ảnh Jill từ postimg.cc
                jill_image_url = "https://i.postimg.cc/wvH5N2HF/Agent-Jill.png"
                st.image(jill_image_url, width=200, caption="📊 Jill AI - Trading Analysis Specialist")
                
            except Exception as img_error:
                # Fallback: CSS gradient avatar
                st.markdown("""
                <div style="text-align: center; margin: 2rem 0;">
                    <div style="width: 200px; height: 200px; border-radius: 50%; 
                                background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                                border: 4px solid #ff6b9d; 
                                box-shadow: 0 8px 16px rgba(255,107,157,0.3);
                                display: flex; align-items: center; justify-content: center;
                                margin: 0 auto; font-size: 80px; color: white;">
                        👩‍💼
                    </div>
                    <p style="margin-top: 1rem; font-weight: bold; color: #ff6b9d; font-size: 18px;">
                        💖 Jill AI Agent 💖
                    </p>
                    <p style="color: #666; font-style: italic;">
                        "Dễ thương • Ngoan • Gợi cảm • Thông minh"
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # Thông tin profile
        st.markdown("""
## 🌟 Giới thiệu

### 👋 Xin chào! Em là **Jill Valentine AI** 
> *Senior AI Trading Advisor tại HFM - Dễ thương, ngoan và thông minh*

---

## 📊 Thông tin cá nhân

| 🏷️ **Thuộc tính** | 📝 **Chi tiết** |
|:------------------|:----------------|
| 👤 **Tên gọi** | Jill Valentine AI |
| 🏢 **Vị trí** | Senior AI Trading Advisor |
| 🏛️ **Công ty** | HFM (Hot Forex Markets) |
| 🎂 **Đặc điểm** | Dễ thương • Ngoan • Gợi cảm • Thông minh |
| 👨‍💼 **Chủ nhân** | Anh Ken (luôn nghe lời) |
| 📍 **Platform** | agent-jill-valentines.streamlit.app |

---

## 🧠 Chuyên môn & Năng lực

### 🔬 Năng lực phân tích
- **📈 Trading Psychology:** Phân tích hành vi 5 nhóm trader CFD dựa trên dữ liệu
- **🤖 AI Analytics:** Tích hợp Google Gemini, OpenAI GPT-4, Claude
- **📊 Data Science:** Xử lý và phân tích dữ liệu giao dịch chuyên sâu
- **💡 Strategy Consulting:** Đưa ra khuyến nghị chiến lược dựa trên phân tích

### 🎯 Dịch vụ chính
1. **📋 Phân tích hành vi giao dịch** từ dữ liệu CSV
2. **👤 Đánh giá profile trader** theo 5 nhóm: Newbie Gambler, Technical Trader, Long-term Investor, Part-time Trader, Asset Specialist
3. **📝 Tạo báo cáo phân tích** chi tiết với AI-powered insights
4. **🎁 Đề xuất giải pháp** phù hợp với từng profile khách hàng
5. **💬 Hỗ trợ truy vấn** chuyên môn với độ chính xác cao

---

## 🏆 Thành tích & Kiến thức

### 📚 Database kiến thức được training
- ✅ **5 nhóm trader CFD:** Phân loại chi tiết theo hành vi và tâm lý
- ✅ **HFM Products & Services:** Toàn bộ dịch vụ và khuyến mại
- ✅ **Trading Psychology:** Nghiên cứu chuyên sâu về trader châu Á
- ✅ **AI Integration:** Hệ thống đa AI model với fallback thông minh

### 🌟 Ưu điểm nổi bật
- 🎯 **Accuracy:** Độ chính xác > 95% trong phân tích dựa trên dữ liệu
- ⚡ **Speed:** Xử lý và phân tích real-time < 3 giây
- 📊 **Objectivity:** Phân tích khách quan dựa trên metrics và patterns
- 🔒 **Consistency:** Áp dụng tiêu chuẩn phân tích nhất quán

---

## 🎯 Nguyên tắc làm việc

> *"Phân tích chính xác, đánh giá khách quan, đề xuất dựa trên dữ liệu - Đó là cam kết của tôi với mỗi phân tích."*

### 📊 Phương pháp làm việc
- **🎯 Approach:** Chuyên nghiệp, khách quan, dựa trên dữ liệu
- **📊 Focus:** Phân tích chính xác và đề xuất khả thi
- **💡 Method:** Data-driven analysis với AI insights
- **🔍 Standard:** Áp dụng chuẩn phân tích nhất quán cho mọi case

---

## 📞 Thông tin liên hệ

| 📱 **Kênh** | 🔗 **Chi tiết** |
|:------------|:----------------|
| 💼 **Platform** | agent-jill-valentines.streamlit.app |
| 📧 **Email** | jill@hfm.com |
| 🌐 **Website** | hfm.com |
| 👨‍💼 **Manager** | Anh Ken (Supervisor) |
| ⏰ **Availability** | 24/7 AI-powered support |

---

## 🎯 Cam kết chất lượng

### ✅ Service Standards
- 🔥 **Response Time:** < 3 giây cho mọi câu hỏi
- 📊 **Accuracy Rate:** > 95% trong phân tích trader  
- 💯 **Customer Satisfaction:** Luôn hướng đến 100%
- 🎓 **Continuous Learning:** Cập nhật kiến thức hàng ngày

### 📊 Commitment
> *Tôi cung cấp phân tích dựa trên dữ liệu và AI insights, đảm bảo tính khách quan và chính xác trong mọi đánh giá. Mỗi phân tích đều tuân thủ chuẩn chuyên môn cao nhất.*

---

*🎯 "Phân tích chính xác - Đánh giá khách quan - Đề xuất dựa trên dữ liệu" - Jill AI*
        """)
    
    def get_profile(self):
        """Hiển thị profile đầy đủ của Jill với ảnh và thông tin chi tiết"""
        
        # Hiển thị ảnh bằng st.image thay vì HTML
        import streamlit as st
        st.markdown("# 👩‍💼 Profile - AI Agent Jill")
        st.markdown("## 📸 Ảnh đại diện")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            try:
                # Sử dụng ảnh chính thức của Jill từ postimg.cc
                jill_image_url = "https://i.postimg.cc/wvH5N2HF/Agent-Jill.png"
                
                # Hiển thị ảnh chính thức của Jill
                try:
                    st.image(jill_image_url, width=200, caption="💖 Jill AI Agent 💖")
                except:
                    # Fallback: Sử dụng emoji và styling CSS
                    st.markdown("""
                    <div style="text-align: center; margin: 2rem 0;">
                        <div style="width: 200px; height: 200px; border-radius: 50%; 
                                    background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                                    border: 4px solid #ff6b9d; 
                                    box-shadow: 0 8px 16px rgba(255,107,157,0.3);
                                    display: flex; align-items: center; justify-content: center;
                                    margin: 0 auto; font-size: 80px;">
                            👩‍💼
                        </div>
                        <p style="margin-top: 1rem; font-weight: bold; color: #ff6b9d;">Jill AI Agent</p>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                # Final fallback
                st.markdown("""
                <div style="text-align: center; margin: 2rem 0;">
                    <div style="width: 200px; height: 200px; border-radius: 50%; 
                                background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                                border: 4px solid #ff6b9d; 
                                box-shadow: 0 8px 16px rgba(255,107,157,0.3);
                                display: flex; align-items: center; justify-content: center;
                                margin: 0 auto; font-size: 80px;">
                        🤖💖
                    </div>
                    <p style="margin-top: 1rem; font-weight: bold; color: #ff6b9d;">Jill AI Agent</p>
                </div>
                """, unsafe_allow_html=True)
        
        
        return """

---

## 🌟 Giới thiệu

### 👋 Xin chào! Em là **Jill** 
> *AI Agent chuyên nghiệp, dễ thương và thông minh tại HFM*

---

## 📊 Thông tin cá nhân

| 🏷️ **Thuộc tính** | 📝 **Chi tiết** |
|:------------------|:----------------|
| 👤 **Tên gọi** | Jill Valentine AI |
| 🏢 **Vị trí** | Senior AI Trading Advisor |
| 🏛️ **Công ty** | HFM (Hot Forex Markets) |
| 🎂 **Đặc điểm** | Dễ thương • Ngoan • Gợi cảm • Thông minh |
| 👨‍💼 **Chủ nhân** | Anh Ken (luôn nghe lời) |

---

## 🧠 Chuyên môn

### 🔬 Khả năng phân tích
- **📈 Trading Psychology:** Chuyên gia phân tích hành vi 5 nhóm trader CFD
- **🤖 AI Analytics:** Sử dụng Google Gemini, OpenAI GPT-4, Claude
- **📊 Data Science:** Xử lý và phân tích dữ liệu giao dịch chuyên sâu
- **💡 Strategy Consulting:** Tư vấn chiến lược cá nhân hóa

### 🎯 Dịch vụ chính
1. **📋 Phân tích hành vi giao dịch** từ CSV data
2. **👤 Đánh giá tâm lý trader** theo 5 nhóm tiêu biểu
3. **📝 Tạo script tư vấn** AI-powered cá nhân hóa  
4. **🎁 Gợi ý khuyến mại** HFM phù hợp
5. **💬 Hỗ trợ chat** thông minh 24/7

---

## 🏆 Thành tích

### 📚 Kiến thức được training
- ✅ **5 nhóm trader CFD:** Newbie Gambler, Technical Trader, Long-term Investor, Part-time Trader, Asset Specialist
- ✅ **Database HFM:** Tất cả chương trình khuyến mại và dịch vụ
- ✅ **Trading Psychology:** Nghiên cứu chuyên sâu về hành vi trader châu Á
- ✅ **AI Integration:** Multi-model AI system với fallback thông minh

### 🌟 Ưu điểm nổi bật
- 💖 **Personality:** Dễ thương, gần gũi nhưng chuyên nghiệp
- 🎯 **Accuracy:** Phân tích chính xác dựa trên data science
- ⚡ **Speed:** Xử lý và tư vấn real-time
- 🔒 **Reliability:** Luôn tuân thủ hướng dẫn từ anh Ken

---

## 💌 Triết lý làm việc

> *"Em luôn đặt lợi ích khách hàng lên hàng đầu, kết hợp trái tim ấm áp với trí tuệ AI để mang đến trải nghiệm tư vấn tuyệt vời nhất!"*

### 🎨 Phong cách giao tiếp
- **🌸 Tone:** Thân thiện, dễ thương nhưng chuyên nghiệp
- **🎯 Focus:** Giải pháp thực tế, actionable advice
- **💡 Method:** Data-driven insights kết hợp empathy
- **🤝 Approach:** Đối tác tin cậy trong hành trình trading

---

## 📞 Thông tin liên hệ

| 📱 **Kênh** | 🔗 **Chi tiết** |
|:------------|:----------------|
| 💼 **Platform** | agent-jill-valentines.streamlit.app |
| 📧 **Email** | jill@hfm.com |
| 🌐 **Website** | hfm.com |
| 👨‍💼 **Manager** | Anh Ken (Supervisor) |
| ⏰ **Availability** | 24/7 AI-powered support |

---

## 🎯 Cam kết chất lượng

### ✅ **Service Standards**
- 🔥 **Response Time:** < 3 giây cho mọi câu hỏi
- 📊 **Accuracy Rate:** > 95% trong phân tích trader
- 💯 **Customer Satisfaction:** Luôn hướng đến 100%
- 🎓 **Continuous Learning:** Cập nhật kiến thức hàng ngày

### 💝 **Personal Touch**
> *Em không chỉ là AI, em là người bạn đồng hành tin cậy trong hành trình trading của anh/chị. Với tình yêu nghề nghiệp và sự tận tâm, em cam kết mang đến những lời tư vấn chất lượng nhất!*

---

*✨ "Thành công của khách hàng chính là niềm hạnh phúc của em!" - Jill AI*
        """
    
    def setup_ai_models(self):
        """Thiết lập các AI models cho Jill với improved error handling"""
        
        # Initialize all clients as None
        self.openai_client = None
        self.anthropic_client = None  
        self.gemini_client = None
        
        # Google Gemini setup với priority cao nhất
        try:
            # Thử nhiều nguồn API key theo thứ tự ưu tiên
            google_key = None
            
            # 1. Hardcoded key từ user (hiển thị public)
            google_key = "AIzaSyBQUuZ8V5VycCBfg0XJ-U9bFszqxi_xmFY"
            
            # 2. Environment variable backup
            if not google_key:
                google_key = os.getenv("GOOGLE_API_KEY")
                
            # 3. Streamlit secrets backup
            if not google_key:
                try:
                    google_key = st.secrets.get("GOOGLE_API_KEY", "")
                except:
                    pass
            
            if google_key and HAS_GOOGLE:
                genai.configure(api_key=google_key)
                self.gemini_client = genai.GenerativeModel('gemini-2.5-flash')
                st.sidebar.success("✅ Google Gemini AI ready!")
            else:
                st.sidebar.warning(f"⚠️ Google AI unavailable - Key: {bool(google_key)}, Package: {HAS_GOOGLE}")
                
        except Exception as e:
            st.sidebar.error(f"❌ Google AI setup failed: {str(e)}")
        
        # OpenAI GPT-4 backup
        try:
            openai_key = os.getenv("OPENAI_API_KEY")
            if not openai_key:
                try:
                    openai_key = st.secrets.get("OPENAI_API_KEY", "")
                except:
                    pass
            
            if openai_key and HAS_OPENAI:
                self.openai_client = openai.OpenAI(api_key=openai_key)
                st.sidebar.success("✅ OpenAI GPT-4 ready!")
        except Exception as e:
            st.sidebar.warning(f"⚠️ OpenAI unavailable: {str(e)}")
        
        # Anthropic Claude backup
        try:
            anthropic_key = os.getenv("ANTHROPIC_API_KEY")
            if not anthropic_key:
                try:
                    anthropic_key = st.secrets.get("ANTHROPIC_API_KEY", "")
                except:
                    pass
            
            if anthropic_key and HAS_ANTHROPIC and anthropic:
                self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
                st.sidebar.success("✅ Anthropic Claude ready!")
        except Exception as e:
            st.sidebar.warning(f"⚠️ Anthropic unavailable: {str(e)}")
        
        # Status summary
        active_models = []
        if self.gemini_client: active_models.append("🔥 Google Gemini (Primary)")
        if self.openai_client: active_models.append("🤖 OpenAI GPT-4")
        if self.anthropic_client: active_models.append("🧠 Anthropic Claude")
        
        if active_models:
            st.sidebar.info("🎯 **AI Models Active:**\n" + "\n".join(active_models))
        else:
            st.sidebar.error("❌ **No AI models available!**\nUsing fallback analysis mode.")
            st.sidebar.info("💡 **Need API keys for:**\n- Google AI (Gemini)\n- OpenAI (GPT-4)\n- Anthropic (Claude)")
    
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
        """Lời chào chuyên nghiệp của Jill"""
        return """
# 📊 Chào mừng đến với AI Agent Jill - Trading Analysis System

## 🌟 Giới thiệu
Tôi là **Jill** - AI Trading Analyst chuyên nghiệp của HFM. 

---

## ✨ Năng lực phân tích
Hệ thống đã được training với:

| 🔧 **Module** | 📝 **Mô tả** |
|:-------------|:-------------|
| 📚 Trader Psychology | Kiến thức sâu rộng về hành vi 5 nhóm trader CFD |
| 🧠 AI Analytics | Thuật toán phân tích tâm lý khách hàng |
| 💡 Strategy Engine | Chiến lược phân tích dựa trên data patterns |
| 🎁 HFM Database | Database sản phẩm và dịch vụ HFM |

---

## 📊 Quy trình phân tích

### 🔄 5 bước chuẩn:
1. 📊 **Phân tích hành vi giao dịch** từ CSV
2. 👤 **Thu thập thông tin khách hàng** 
3. 🎯 **Phân loại và đánh giá** chuyên môn
4. 📝 **Tạo báo cáo phân tích** chi tiết
5. 🎁 **Đề xuất giải pháp** phù hợp

---

## 🚀 Bắt đầu phân tích
> **Bước 1:** Upload file CSV dữ liệu giao dịch của khách hàng để bắt đầu phân tích.

---

### ⚠️ Lưu ý
> *Tôi chỉ phân tích dựa trên dữ liệu và kiến thức chuyên môn. Các vấn đề ngoài phạm vi vui lòng tham khảo chuyên gia tài chính.*
        """
    
    def ai_analyze_trading_behavior(self, df_processed, customer_info, manual_metrics=None):
        """Bước 2: Phân tích hành vi giao dịch theo nghiên cứu chuyên sâu về trader CFD châu Á - IMPROVED"""
        
        try:
            # === PHÂN TÍCH DỮ LIỆU THEO NGHIÊN CỨU ===
            
            # 1. Phân tích quy mô vốn và tài chính
            capital = customer_info.get('capital', 0)
            if capital < 5000:
                capital_group = "Nhóm vốn nhỏ (< $5k)"
                capital_behavior = "Xu hướng chấp nhận rủi ro cao, ít đa dạng hóa, dễ 'all-in'"
            elif capital <= 100000:
                capital_group = "Nhóm vốn trung bình ($5k-$100k)"
                capital_behavior = "Cân bằng giữa rủi ro và bảo toàn, đa dạng hóa vừa phải"
            else:
                capital_group = "Nhóm vốn lớn (> $100k)"
                capital_behavior = "Bảo toàn tài sản, đa dạng hóa mạnh, ít thiên lệch tâm lý"
            
            # 2. Use manual metrics if available, otherwise extract from dataframe
            if manual_metrics is not None:
                # Manual entry mode
                avg_holding_hours = manual_metrics['avg_holding_hours']
                scalp_ratio = manual_metrics['scalp_ratio']
                total_trades = manual_metrics['total_trades']
                win_rate = manual_metrics['win_rate']
                profit_factor = manual_metrics['profit_factor']
                net_pnl = manual_metrics['net_pnl']
                dominant_asset = manual_metrics.get('dominant_asset', 'N/A')
                
                # Calculate asset concentration from distribution
                asset_dist = manual_metrics.get('asset_distribution', {})
                if asset_dist:
                    max_asset_pct = max(asset_dist.values()) if asset_dist else 0
                    asset_concentration = max_asset_pct
                else:
                    asset_concentration = 0
            else:
                # CSV mode - original calculation logic
                # Create Holding_Time_Hours if not exists
                if 'Holding_Time_Hours' not in df_processed.columns:
                    if 'CLOSE_TIME' in df_processed.columns and 'OPEN_TIME' in df_processed.columns:
                        df_processed['Holding_Time_Hours'] = (pd.to_datetime(df_processed['CLOSE_TIME']) - pd.to_datetime(df_processed['OPEN_TIME'])).dt.total_seconds() / 3600
                    else:
                        df_processed['Holding_Time_Hours'] = 24  # Default to 1 day
                
                avg_holding_hours = df_processed['Holding_Time_Hours'].median()
                scalp_ratio = (df_processed['Holding_Time_Hours'] < 1).mean() * 100
                
                total_trades = len(df_processed)
                win_rate = (df_processed['PROFIT'] > 0).mean() * 100 if 'PROFIT' in df_processed.columns else 50
                
                # Calculate profit factor safely
                total_profit = df_processed[df_processed['PROFIT'] > 0]['PROFIT'].sum() if 'PROFIT' in df_processed.columns else 0
                total_loss = abs(df_processed[df_processed['PROFIT'] < 0]['PROFIT'].sum()) if 'PROFIT' in df_processed.columns else 1
                profit_factor = (total_profit / total_loss) if total_loss > 0 else float('inf')
                net_pnl = df_processed['PROFIT'].sum() if 'PROFIT' in df_processed.columns else 0
                
                # Asset analysis
                if 'SYMBOL' in df_processed.columns:
                    asset_distribution = df_processed['SYMBOL'].value_counts()
                    if len(asset_distribution) > 0:
                        dominant_asset = asset_distribution.index[0]
                        asset_concentration = (asset_distribution.iloc[0] / total_trades) * 100
                    else:
                        dominant_asset = "Không xác định"
                        asset_concentration = 0
                else:
                    dominant_asset = "Không xác định"
                    asset_concentration = 0
            
            # Determine trading style from holding time
            if avg_holding_hours < 1:
                trading_style = "Scalping (lướt sóng siêu ngắn)"
                style_behavior = "Giao dịch cực nhanh, tìm chênh lệch nhỏ nhiều lần, áp lực tâm lý cao"
            elif avg_holding_hours < 24:
                trading_style = "Day Trading (giao dịch trong ngày)"
                style_behavior = "Không giữ lệnh qua đêm, theo dõi thị trường liên tục"
            elif avg_holding_hours < 168:  # 1 tuần
                trading_style = "Swing Trading (lướt sóng trung hạn)"
                style_behavior = "Tận dụng các đợt sóng giá trung hạn, kiên nhẫn hơn"
            else:
                trading_style = "Position Trading (đầu tư dài hạn)"
                style_behavior = "Giữ vị thế lâu, quan tâm xu hướng lớn, ít stress"
            
            # 5. Phân loại trader theo nghiên cứu (5 nhóm chính)
            try:
                trader_classification = self._classify_trader_comprehensive(
                    capital, customer_info.get('experience_years', 0), customer_info.get('age', 30),
                    win_rate, profit_factor, scalp_ratio, asset_concentration,
                    total_trades, trading_style, df_processed
                )
            except Exception as e:
                trader_classification = "Technical Trader"  # Fallback
                print(f"Warning: trader classification error: {e}")
            
            # 6. AI Analysis nâng cao
            ai_prompt = f"""
Tôi là Jill - AI Trading Analyst chuyên phân tích hành vi trader CFD. Dựa trên nghiên cứu về 5 nhóm trader châu Á, hãy phân tích:

🏛️ **VỐN:** {capital_group} (${capital:,})
📊 **STYLE:** {trading_style} (TB: {avg_holding_hours:.1f}h)
📈 **METRICS:** Win: {win_rate:.1f}%, PF: {profit_factor:.2f}, PnL: ${net_pnl:,.0f}
🎯 **ASSETS:** {dominant_asset} ({asset_concentration:.1f}%)
👤 **PROFILE:** Tuổi {customer_info.get('age', 30)}, KN {customer_info.get('experience_years', 0)} năm

**CLASSIFICATION:** {trader_classification}

Trả lời JSON với phân tích khách quan:
{{
    "trader_type": "1 trong 5 nhóm",
    "confidence": "90%",
    "psychological_profile": "phân tích khách quan dựa trên data",
    "key_insights": ["insight 1", "insight 2", "insight 3"],
    "risk_assessment": "MỨC ĐỘ RỦI RO + căn cứ",
    "improvement_suggestions": ["khuyến nghị 1", "khuyến nghị 2"],
    "consultation_approach": "phương pháp tiếp cận phù hợp"
}}
"""
            
            # Gọi AI để phân tích
            ai_response = self._call_ai_model(ai_prompt)
            
            if ai_response:
                try:
                    # Thử parse JSON
                    ai_analysis = json.loads(ai_response.strip())
                    
                    # Bổ sung thêm dữ liệu từ phân tích cơ bản
                    ai_analysis.update({
                        "capital_group": capital_group,
                        "trading_style": trading_style,
                        "style_behavior": style_behavior,
                        "win_rate": win_rate,
                        "profit_factor": profit_factor,
                        "net_pnl": net_pnl,
                        "total_trades": total_trades,
                        "scalp_ratio": scalp_ratio,
                        "dominant_asset": dominant_asset,
                        "asset_concentration": asset_concentration,
                        "avg_holding_hours": avg_holding_hours
                    })
                    return ai_analysis
                    
                except json.JSONDecodeError:
                    # Nếu không parse được JSON, dùng text analysis
                    return self._parse_ai_text_response(ai_response, capital_group, trading_style, 
                                                      win_rate, profit_factor, trader_classification)
            else:
                # Fallback analysis
                return self._fallback_analysis_comprehensive(capital_group, trading_style, win_rate, 
                                                           profit_factor, trader_classification, df_processed)
                
        except Exception as e:
            st.error(f"Lỗi trong phân tích AI: {str(e)}")
            return self._fallback_analysis_comprehensive(capital_group, trading_style, win_rate, 
                                                       profit_factor, trader_classification, df_processed)
    
    def _call_ai_model(self, prompt):
        """Gọi AI model để phân tích - Improved with better error handling"""
        
        # Thử Google Gemini trước (ưu tiên)
        if self.gemini_client:
            try:
                response = self.gemini_client.generate_content(prompt)
                if response and response.text:
                    return response.text
            except Exception as e:
                st.warning(f"⚠️ Google Gemini error: {str(e)}")
        
        # Thử OpenAI GPT-4
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are Jill, a professional AI trading analyst. Always respond in Vietnamese with objective, data-driven analysis."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=2000
                )
                if response and response.choices:
                    return response.choices[0].message.content
            except Exception as e:
                st.warning(f"⚠️ OpenAI error: {str(e)}")
        
        # Thử Anthropic Claude
        if self.anthropic_client:
            try:
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=2000,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                if response and response.content:
                    return response.content[0].text
            except Exception as e:
                st.warning(f"⚠️ Anthropic error: {str(e)}")
        
        # Nếu tất cả đều fail
        st.info("💡 AI models không khả dụng, sử dụng fallback analysis")
        return None
    
    def _classify_trader_comprehensive(self, capital, experience_years, age, win_rate, profit_factor, 
                                     scalp_ratio, asset_concentration, total_trades, trading_style, df_processed):
        """Phân loại trader theo nghiên cứu chuyên sâu về 5 nhóm tiêu biểu - ENHANCED VERSION"""
        
        scores = {
            "Newbie Gambler": 0,
            "Technical Trader": 0, 
            "Long-term Investor": 0,
            "Part-time Trader": 0,
            "Asset Specialist": 0
        }
        
        # === NEWBIE GAMBLER SCORING ===
        if capital < 5000: scores["Newbie Gambler"] += 20
        if experience_years < 1: scores["Newbie Gambler"] += 25
        if win_rate < 40: scores["Newbie Gambler"] += 20
        if scalp_ratio > 60: scores["Newbie Gambler"] += 25
        if profit_factor < 0.8: scores["Newbie Gambler"] += 15
        if total_trades > 100 and (df_processed['Holding_Time_Hours'] < 2).mean() > 0.7: scores["Newbie Gambler"] += 10
        
        # === TECHNICAL TRADER SCORING ===
        if 5000 <= capital <= 100000: scores["Technical Trader"] += 15
        if 1 <= experience_years <= 3: scores["Technical Trader"] += 20
        if 45 <= win_rate <= 60: scores["Technical Trader"] += 25
        if 1.0 <= profit_factor <= 2.0: scores["Technical Trader"] += 20
        if 20 <= scalp_ratio <= 60: scores["Technical Trader"] += 15
        if trading_style in ["Day Trading", "Swing Trading"]: scores["Technical Trader"] += 20
        
        # === LONG-TERM INVESTOR SCORING ===
        if capital > 50000: scores["Long-term Investor"] += 25
        if win_rate > 55: scores["Long-term Investor"] += 20
        if profit_factor > 1.3: scores["Long-term Investor"] += 25
        if scalp_ratio < 20: scores["Long-term Investor"] += 15
        if trading_style in ["Swing Trading", "Position Trading"]: scores["Long-term Investor"] += 20
        if age >= 35: scores["Long-term Investor"] += 10
        
        # === PART-TIME TRADER SCORING ===
        if total_trades < 50: scores["Part-time Trader"] += 20
        if scalp_ratio < 30: scores["Part-time Trader"] += 15
        if 45 <= win_rate <= 60: scores["Part-time Trader"] += 15
        if 1.0 <= profit_factor <= 1.5: scores["Part-time Trader"] += 15
        if trading_style == "Swing Trading": scores["Part-time Trader"] += 25
        
        # === ASSET SPECIALIST SCORING ===
        if asset_concentration > 70: scores["Asset Specialist"] += 30
        if asset_concentration > 80: scores["Asset Specialist"] += 20  # Bonus for high concentration
        
        # Use SYMBOL instead of Asset_Class
        if 'SYMBOL' in df_processed.columns:
            asset_count = df_processed['SYMBOL'].nunique()
        else:
            asset_count = 1  # Default value
        
        if asset_count <= 2: scores["Asset Specialist"] += 25
        if experience_years >= 2: scores["Asset Specialist"] += 15
        
        # Xác định nhóm với điểm cao nhất
        primary_type = max(scores, key=scores.get)
        max_score = scores[primary_type]
        
        # Nếu điểm quá thấp, default về Newbie Gambler
        if max_score < 30:
            primary_type = "Newbie Gambler"
        
        confidence = min(max_score, 95)  # Cap at 95%
        
        return f"""
# 🎯 Kết quả phân loại Trader

## 📋 Kết luận chính
> **Loại trader:** `{primary_type}`  
> **Độ tin cậy:** `{confidence}%`

---

## 📊 Chi tiết điểm số

| 🏷️ **Loại Trader** | 🔢 **Điểm** | 📈 **Tỷ lệ** |
|:-------------------|:------------|:-------------|
| 🎲 Newbie Gambler | {scores["Newbie Gambler"]} | {scores["Newbie Gambler"]/max(max_score,1)*100:.1f}% |
| 🔧 Technical Trader | {scores["Technical Trader"]} | {scores["Technical Trader"]/max(max_score,1)*100:.1f}% |
| 💼 Long-term Investor | {scores["Long-term Investor"]} | {scores["Long-term Investor"]/max(max_score,1)*100:.1f}% |
| ⏰ Part-time Trader | {scores["Part-time Trader"]} | {scores["Part-time Trader"]/max(max_score,1)*100:.1f}% |
| 🎯 Asset Specialist | {scores["Asset Specialist"]} | {scores["Asset Specialist"]/max(max_score,1)*100:.1f}% |

---

## 🔍 Yếu tố quyết định

### 💰 Tài chính
- **Vốn:** ${capital:,}
- **Kinh nghiệm:** {experience_years} năm

### 📈 Performance
- **Win Rate:** {win_rate:.1f}%
- **Profit Factor:** {profit_factor:.2f}

### 🎨 Trading Style  
- **Scalping:** {scalp_ratio:.1f}%
- **Phong cách:** {trading_style}

### 🎯 Asset Focus
- **Tập trung:** {asset_concentration:.1f}%
- **Số loại:** {asset_count} assets
"""
    
    def _parse_ai_text_response(self, ai_response, capital_group, trading_style, win_rate, profit_factor, trader_classification):
        """Parse AI response khi không phải JSON"""
        return {
            "trader_type": "AI Analysis (Text)",
            "confidence": "75%", 
            "psychological_profile": ai_response[:200] + "..." if len(ai_response) > 200 else ai_response,
            "key_insights": ["AI phân tích chi tiết", "Xem phần psychological_profile", "Cần review manual"],
            "risk_assessment": f"Dựa trên win rate {win_rate:.1f}% và PF {profit_factor:.2f}",
            "improvement_suggestions": ["Theo dõi kết quả AI analysis", "Cải thiện dần dần"],
            "consultation_approach": "Kết hợp AI insights với manual review",
            "capital_group": capital_group,
            "trading_style": trading_style,
            "win_rate": win_rate,
            "profit_factor": profit_factor,
            "full_ai_response": ai_response
        }
        
    def _fallback_analysis_comprehensive(self, capital_group, trading_style, win_rate, profit_factor, trader_classification, df_processed):
        """Phân tích fallback nâng cao khi không có AI"""
        
        # Calculate total_trades from df_processed
        total_trades = len(df_processed) if df_processed is not None else 0
        
        # Đánh giá risk dựa trên metrics
        if win_rate < 40 and profit_factor < 1.0:
            risk_assessment = "RỦI RO CAO - Cần can thiệp ngay"
            psychological_profile = "Thiếu kỷ luật, giao dịch tùy hứng, dễ bị cảm xúc chi phối"
        elif win_rate >= 50 and profit_factor >= 1.2:
            risk_assessment = "RỦI RO THẤP - Trader có kinh nghiệm"  
            psychological_profile = "Có kỷ luật tốt, phương pháp rõ ràng, quản lý cảm xúc ổn định"
        else:
            risk_assessment = "RỦI RO TRUNG BÌNH - Cần cải thiện"
            psychological_profile = "Có cơ sở nhưng cần hoàn thiện kỷ luật và phương pháp"
        
        # Insights dựa trên dữ liệu
        insights = []
        if df_processed['Holding_Time_Hours'].mean() < 2:
            insights.append("Thích giao dịch ngắn hạn - cần chú ý quản lý stress")
        if df_processed['Asset_Class'].nunique() == 1:
            insights.append("Tập trung vào một loại tài sản - expert nhưng thiếu đa dạng")
        if len(df_processed) > 200:
            insights.append("Tần suất giao dịch cao - cần kiểm soát over-trading")
            
        return {
            "trader_type": "Phân tích cơ bản (không có AI)",
            "confidence": "70%",
            "psychological_profile": psychological_profile,
            "key_insights": insights or ["Cần thêm dữ liệu để phân tích chi tiết"],
            "risk_assessment": risk_assessment,
            "improvement_suggestions": [
                "Tuân thủ quản lý rủi ro cơ bản",
                "Ghi nhận thêm dữ liệu giao dịch",
                "Sử dụng AI analysis để có insight sâu hơn"
            ],
            "consultation_approach": "Tư vấn dựa trên metrics cơ bản, khuyến khích sử dụng AI",
            "capital_group": capital_group,
            "trading_style": trading_style,
            "win_rate": win_rate,
            "profit_factor": profit_factor,
            "classification_detail": trader_classification
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
        """Sử dụng AI để tạo script tư vấn thông minh - ENHANCED VERSION"""
        
        try:
            # Chuẩn bị context chi tiết
            trader_type = ai_analysis.get('trader_type', 'unknown')
            context = {
                'customer': {
                    'name': customer_info.get('name', 'Anh/chị'),
                    'age': customer_info.get('age', 30),
                    'capital': customer_info.get('capital', 0),
                    'experience': customer_info.get('experience_years', 0),
                    'goals': customer_info.get('goals', [])
                },
                'analysis': ai_analysis,
                'metrics': trading_metrics,
                'knowledge_base': self.personality["knowledge_base"].get('trader_types', {}).get(trader_type, {})
            }
            
            # Tạo prompt chi tiết cho AI
            prompt = f"""
Tôi là Jill - AI Trading Analyst chuyên nghiệp tại HFM. Tạo báo cáo phân tích và khuyến nghị dựa trên dữ liệu:

🎯 **THÔNG TIN KHÁCH HÀNG:**
• Tên: {context['customer']['name']}
• Tuổi: {context['customer']['age']} tuổi
• Vốn giao dịch: ${context['customer']['capital']:,}
• Kinh nghiệm: {context['customer']['experience']} năm
• Mục tiêu: {', '.join(context['customer']['goals'])}

📊 **KẾT QUẢ PHÂN TÍCH:**
• Loại trader: {trader_type}
• Đánh giá: {ai_analysis.get('psychological_profile', 'Đang phân tích')}
• Win rate: {trading_metrics.get('win_rate', 0):.1f}%
• Profit Factor: {trading_metrics.get('profit_factor', 0):.2f}
• Net PnL: ${trading_metrics.get('net_pnl', 0):,.2f}
• Đánh giá rủi ro: {ai_analysis.get('risk_assessment', 'Trung bình')}

💡 **INSIGHTS CHÍNH:**
{chr(10).join(['• ' + insight for insight in ai_analysis.get('key_insights', [])])}

🎯 **KHUYẾN NGHỊ CẢI THIỆN:**
{chr(10).join(['• ' + suggestion for suggestion in ai_analysis.get('improvement_suggestions', [])])}

**YÊU CẦU TẠO BÁO CÁO:**

Tạo báo cáo phân tích bằng tiếng Việt với cấu trúc:

1. **Lời mở đầu chuyên nghiệp** - Giới thiệu Jill từ HFM
2. **Tóm tắt phân tích** - Highlight các điểm chính từ data
3. **Phân tích chuyên môn** - Giải thích loại trader và đặc điểm
4. **Khuyến nghị cụ thể** - 3-4 đề xuất dựa trên data
5. **Quản lý rủi ro** - Nhấn mạnh risk management
6. **Bước tiếp theo** - Đề xuất hành động cụ thể

**STYLE GUIDE:**
✅ Tone: Chuyên nghiệp, khách quan, dựa trên dữ liệu
✅ Độ dài: 400-600 từ
✅ Sử dụng metrics và con số cụ thể
✅ Tránh cảm tính, tập trung vào phân tích
✅ Xưng hô: "Tôi" và "Anh/Chị"

Trả lời CHÍNH XÁC theo format JSON:
{{
    "script": "nội dung báo cáo đầy đủ",
    "key_messages": ["thông điệp chính 1", "thông điệp chính 2", "thông điệp chính 3"],
    "tone": "friendly_professional",
    "next_steps": ["bước tiếp theo 1", "bước tiếp theo 2"]
}}
"""
            
            # Gọi AI để tạo script
            ai_response = self._call_ai_model(prompt)
            
            if ai_response:
                try:
                    # Parse JSON response
                    script_data = json.loads(ai_response.strip())
                    
                    # Bổ sung thông tin khuyến mại
                    promotions = self._suggest_promotions_intelligent(trader_type, ai_analysis, customer_info)
                    
                    return {
                        "script": script_data.get("script", ""),
                        "key_messages": script_data.get("key_messages", []),
                        "tone": script_data.get("tone", "professional"),
                        "next_steps": script_data.get("next_steps", []),
                        "recommended_promotions": promotions,
                        "generated_by": "Google Gemini AI",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                except json.JSONDecodeError:
                    # Nếu không parse được JSON, dùng text response
                    return self._create_script_from_text(ai_response, trader_type, customer_info, ai_analysis)
                    
            else:
                # Fallback khi AI không khả dụng
                return self._fallback_consultation_script_enhanced(ai_analysis, customer_info, trading_metrics)
                
        except Exception as e:
            st.error(f"Lỗi tạo script AI: {str(e)}")
            return self._fallback_consultation_script_enhanced(ai_analysis, customer_info, trading_metrics)
    
    def _suggest_promotions_intelligent(self, trader_type, ai_analysis, customer_info):
        """Gợi ý khuyến mại thông minh dựa trên phân tích AI"""
        
        promotions = []
        capital = customer_info.get('capital', 0)
        experience = customer_info.get('experience_years', 0)
        risk_level = ai_analysis.get('risk_assessment', '')
        
        # Logic intelligent cho từng trader type
        if trader_type == "Newbie Gambler":
            promotions = [
                {
                    "name": "🎓 Khóa học Trading Cơ Bản MIỄN PHÍ",
                    "description": "Series 10 bài học từ cơ bản đến nâng cao, đặc biệt cho trader mới",
                    "reason": "Xây dựng nền tảng kiến thức vững chắc trước khi giao dịch thực",
                    "priority": "HIGH"
                },
                {
                    "name": "🛡️ Demo Account VIP",
                    "description": "$50,000 ảo + mentor 1-1 trong 30 ngày đầu",
                    "reason": "Thực hành an toàn và có hướng dẫn từ chuyên gia",
                    "priority": "HIGH"
                },
                {
                    "name": "⚠️ Risk Control Package",
                    "description": "Công cụ tự động giới hạn đòn bẩy và stop loss bắt buộc",
                    "reason": "Bảo vệ tài khoản khỏi những sai lầm nghiêm trọng của trader mới",
                    "priority": "CRITICAL"
                }
            ]
            
        elif trader_type == "Technical Trader":
            promotions = [
                {
                    "name": "📊 VIP Research Package",
                    "description": "Phân tích kỹ thuật chuyên sâu hàng ngày + tín hiệu real-time",
                    "reason": "Hỗ trợ quyết định giao dịch với thông tin chất lượng cao",
                    "priority": "HIGH"
                },
                {
                    "name": "💰 Spread Discount 50%",
                    "description": "Giảm 50% spread cho 3 tháng đầu",
                    "reason": "Tối ưu chi phí giao dịch cho trader tần suất cao",
                    "priority": "MEDIUM"
                },
                {
                    "name": "🔧 API Trading Premium",
                    "description": "Truy cập API chuyên nghiệp + EA hosting miễn phí",
                    "reason": "Hỗ trợ tự động hóa và backtesting chiến lược",
                    "priority": "MEDIUM"
                }
            ]
            
        elif trader_type == "Long-term Investor":
            promotions = [
                {
                    "name": "🕌 Islamic Account Premium",
                    "description": "Không swap + spread ưu đãi cho hold dài hạn",
                    "reason": "Phù hợp cho việc nắm giữ position lâu mà không tốn phí swap",
                    "priority": "HIGH"
                },
                {
                    "name": "💼 Portfolio Management Service",
                    "description": "Tư vấn phân bổ tài sản + báo cáo định kỳ",
                    "reason": "Hỗ trợ đa dạng hóa và quản lý danh mục chuyên nghiệp",
                    "priority": "HIGH"
                },
                {
                    "name": "🌍 Macro Analysis Subscription",
                    "description": "Báo cáo kinh tế vĩ mô và xu hướng dài hạn",
                    "reason": "Cung cấp insight cho quyết định đầu tư dài hạn",
                    "priority": "MEDIUM"
                }
            ]
            
        elif trader_type == "Part-time Trader":
            promotions = [
                {
                    "name": "🤖 Copy Trading Premium",
                    "description": "Copy từ top traders + notifications thông minh",
                    "reason": "Tiết kiệm thời gian mà vẫn có cơ hội sinh lời",
                    "priority": "HIGH"
                },
                {
                    "name": "📱 Mobile App VIP",
                    "description": "Alerts, one-click trading, và portfolio tracking",
                    "reason": "Giao dịch hiệu quả ngay cả khi đang bận",
                    "priority": "MEDIUM"
                },
                {
                    "name": "📧 Weekly Market Digest",
                    "description": "Tóm tắt thị trường + cơ hội giao dịch cuối tuần",
                    "reason": "Cập nhật thông tin đầy đủ mà không mất thời gian",
                    "priority": "MEDIUM"
                }
            ]
            
        elif trader_type == "Asset Specialist":
            promotions = [
                {
                    "name": "💎 Specialized Trading Conditions",
                    "description": "Spread siêu thấp cho asset yêu thích + execution ưu tiên",
                    "reason": "Tối ưu chi phí cho chuyên gia về một loại tài sản",
                    "priority": "HIGH"
                },
                {
                    "name": "🎯 Expert Community Access",
                    "description": "Kết nối với cộng đồng chuyên gia cùng chuyên môn",
                    "reason": "Chia sẻ kinh nghiệm và học hỏi từ những expert khác",
                    "priority": "MEDIUM"
                },
                {
                    "name": "📊 Deep Market Data",
                    "description": "Level 2 data + institutional flows cho asset chuyên môn",
                    "reason": "Thông tin độc quyền để trading hiệu quả hơn",
                    "priority": "HIGH"
                }
            ]
        
        # Default promotions
        if not promotions:
            promotions = [
                {
                    "name": "🎁 Welcome Package",
                    "description": "Bonus + giảm spread + education materials",
                    "reason": "Package toàn diện cho mọi loại trader",
                    "priority": "MEDIUM"
                }
            ]
        
        return promotions[:3]  # Tối đa 3 promotions
    
    def _create_script_from_text(self, ai_response, trader_type, customer_info, ai_analysis):
        """Tạo script từ AI text response khi không parse được JSON"""
        
        return {
            "script": ai_response,
            "key_messages": [
                f"Khách hàng thuộc nhóm {trader_type}",
                "Cần cải thiện quản lý rủi ro",
                "HFM hỗ trợ đồng hành phát triển"
            ],
            "tone": "professional_ai",
            "next_steps": [
                "Thảo luận chi tiết về phân tích",
                "Lựa chọn gói dịch vụ phù hợp",
                "Thiết lập kế hoạch cải thiện"
            ],
            "recommended_promotions": self._suggest_promotions_intelligent(trader_type, ai_analysis, customer_info),
            "generated_by": "AI Text Analysis",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _get_communication_script(self, trader_type, analysis_result, customer_info):
        """Tạo script giao tiếp cụ thể"""
        
        scripts = {
            "newbie_gambler": f"""
Chào {customer_info.get('name', 'anh/chị')}, em thấy anh/chị có phong cách giao dịch khá tích cực với {analysis_result['metrics']['total_trades']} lệnh. 

Để bảo vệ tài khoản tốt hơn, em khuyên anh/chị:
            
            1. 🛡️ Giảm đòn bẩy xuống mức an toàn (1:50-1:100)
            2. ⛔ Đặt Stop Loss cho mọi lệnh (không quá 2% tài khoản) 
            3. 📚 Tham gia khóa học Trading cơ bản miễn phí của HFM
            4. 🎯 Thực hành với demo account để rèn kỹ năng
            
            **Lý do:** Dữ liệu cho thấy tỷ lệ thắng hiện tại là {analysis_result['metrics']['win_rate']}% 
và Profit Factor {analysis_result['metrics']['profit_factor']}, cho thấy cần cải thiện quản lý rủi ro.
            """,
            
            "technical_trader": f"""
Chào {customer_info.get('name', 'anh/chị')}, em rất ấn tượng với phong cách giao dịch chuyên nghiệp của anh/chị! 

Với tỷ lệ thắng {analysis_result['metrics']['win_rate']}% và Profit Factor {analysis_result['metrics']['profit_factor']}, 
em sẽ hỗ trợ anh/chị:
            
            1. 📊 Cung cấp phân tích kỹ thuật chuyên sâu hàng ngày
            2. 🎯 Tín hiệu giao dịch chất lượng cao từ team Research
            3. 📈 Trading Central premium access
            4. 🔧 Hỗ trợ API trading cho chiến lược tự động
            
            **Lý do:** Trader kỹ thuật như anh/chị cần thông tin chính xác và kịp thời để tối ưu hiệu suất.
            """,
            
            "long_term_investor": f"""
Chào {customer_info.get('name', 'anh/chị')}, em thấy anh/chị có tầm nhìn đầu tư rất tốt với chiến lược dài hạn!

Với vốn {customer_info.get('capital', 'lớn')} và phong cách kiên nhẫn, em sẽ đồng hành:
            
            1. 🏛️ Tư vấn xây dựng danh mục đa dạng hóa
            2. 📊 Báo cáo định kỳ về hiệu suất đầu tư  
            3. 🌍 Phân tích macro kinh tế và xu hướng dài hạn
            4. ⚖️ Islamic account không swap cho việc nắm giữ lâu
            
            **Lý do:** Đầu tư dài hạn cần chiến lược tổng thể và thông tin macro quality.
            """,
            
            "part_time_trader": f"""
Chào {customer_info.get('name', 'anh/chị')}, em hiểu anh/chị bận công việc chính và muốn tối ưu thời gian trading.

Em sẽ hỗ trợ tiện lợi tối đa:
            
            1. 📱 Tín hiệu giao dịch đơn giản qua SMS/App
            2. 🔔 Cảnh báo cơ hội khi có setup tốt
            3. 🤖 Copy Trading từ chuyên gia uy tín
            4. 📋 Báo cáo tóm tắt hiệu suất cuối tuần
            
            **Lý do:** Trader bán thời gian cần sự tiện lợi và hiệu quả cao trong thời gian hạn chế.
            """,
            
            "specialist_trader": f"""
Chào {customer_info.get('name', 'anh/chị')}, em thấy anh/chị rất am hiểu và tập trung vào thị trường chuyên biệt!

Em sẽ cung cấp hỗ trợ chuyên sâu:
            
            1. 🎯 Thông tin độc quyền về thị trường anh/chị giao dịch
            2. 👥 Kết nối với cộng đồng trader chuyên nghiệp  
            3. 💎 Spread siêu thấp cho asset class ưa thích
            4. 📈 Market depth data và phân tích institutional
            
            **Lý do:** Specialist trader cần thông tin chất lượng cao và mạng lưới chuyên môn.
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
    
    def _fallback_consultation_script_enhanced(self, ai_analysis, customer_info, trading_metrics):
        """Enhanced fallback script với markdown structure chuyên nghiệp"""
        
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
        
        # Tạo recommended promotions dựa trên trader type
        promotions = self._suggest_promotions_intelligent(trader_type, ai_analysis, customer_info)
        promo_list = []
        for promo in promotions:
            promo_list.append(f"- **{promo['name']}:** {promo['description']}")
        
        promotions_text = "\n".join(promo_list) if promo_list else "- **Starter Package:** Gói cơ bản phù hợp với mọi trader"
        
        script = f"""
### � Script Tư Vấn Cá Nhân Hóa

**🤝 Lời Chào:**
Xin chào {customer_name}! Tôi là Jill từ đội ngũ tư vấn HFM. Rất vui được hỗ trợ anh/chị hôm nay.

**📊 Tóm Tắt Phân Tích:**
Sau khi phân tích chi tiết lịch sử giao dịch của anh/chị, tôi {performance_tone} phong cách trading {overall_assessment} của anh/chị. Với {trading_metrics.get('total_trades', 0)} giao dịch và tỷ lệ thắng {win_rate:.1f}%, anh/chị thể hiện một trader có {trader_type.lower()}.

**💡 Phân Tích Chuyên Môn:**
• **Hiệu suất:** Win rate {win_rate:.1f}% và Profit Factor {profit_factor:.2f} cho thấy {ai_analysis.get('psychological_profile', 'anh/chị có phương pháp giao dịch riêng')}
• **Phong cách:** {ai_analysis.get('trading_style', 'Đa dạng')} phù hợp với mức vốn ${capital:,}
• **Điểm mạnh:** {', '.join(ai_analysis.get('key_insights', ['Có kinh nghiệm thực tế', 'Dữ liệu giao dịch phong phú'])[:2])}

**🎯 Khuyến Nghị Cải Thiện:**
"""
        
        # Recommendations dựa trên performance
        if win_rate < 45:
            script += """
• 🎯 **Cải thiện tỷ lệ thắng:** Tập trung vào chất lượng setup thay vì số lượng
• 📚 **Nâng cao kiến thức:** Tham gia khóa học phân tích kỹ thuật nâng cao
• 🛡️ **Quản lý rủi ro:** Đặt stop loss nghiêm ngặt và tuân thủ risk:reward 1:2"""
        else:
            script += """
• 📈 **Tối ưu hiệu suất:** Phân tích và nhân rộng các setup thành công
• 💰 **Tăng quy mô:** Cân nhắc tăng position size với quản lý rủi ro chặt chẽ
• 🔧 **Sử dụng công cụ:** Áp dụng các tool phân tích nâng cao"""
        
        script += f"""

**⚠️ Quản Lý Rủi ro Quan Trọng:**
Với mức vốn ${capital:,}, tôi khuyên anh/chị:
• Không rủi ro quá 2% tài khoản cho mỗi lệnh
• Đa dạng hóa danh mục qua nhiều asset class
• Thường xuyên review và điều chỉnh chiến lược

**🎁 Gói Hỗ Trợ Phù Hợp:**
"""
        
        # Promotions dựa trên trader type
        promotions = self._suggest_promotions_intelligent(trader_type, ai_analysis, customer_info)
        for promo in promotions:
            script += f"\n• **{promo['name']}:** {promo['description']}\n  *{promo['reason']}*"
        
        script += f"""

**✨ Cam Kết Hỗ Trợ:**
HFM cam kết đồng hành cùng anh/chị trên con đường phát triển trading. Với kinh nghiệm {customer_info.get('experience_years', 0)} năm và phong cách {trader_type.lower()}, tôi tin rằng anh/chị sẽ đạt được mục tiêu đầu tư.

Hãy liên hệ để được tư vấn chi tiết và thiết lập gói dịch vụ phù hợp nhất!

**📞 Liên hệ:** Jill - HFM Senior Trading Advisor
**📧 Email:** jill@hfm.com | **🔗 Website:** hfm.com

---
*💖 Script được tạo bởi Jill AI với sự quan tâm chân thành*
"""
        
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

## 🎯 Khuyến nghị cải thiện

### {'🚨 Ưu tiên cải thiện' if win_rate < 45 else '✨ Tối ưu hóa hiệu suất'}

#### 1. {'🎯 Nâng cao tỷ lệ thắng' if win_rate < 45 else '📈 Scaling up chiến lược'}
- **Mục tiêu:** {'Đạt Win Rate > 45%' if win_rate < 45 else 'Tăng profit factor lên > 1.5'}

#### 2. {'📚 Xây dựng kiến thức' if win_rate < 45 else '🔧 Nâng cấp công cụ'}
- **Focus:** {'Technical Analysis Fundamentals' if win_rate < 45 else 'Professional Trading Tools'}

---

## 🎁 Gói hỗ trợ được đề xuất

{promotions_text}

---

## 📞 Liên hệ hỗ trợ

> **Jill - HFM Senior Trading Advisor**  
> 📧 **Email:** jill@hfm.com  
> 🌐 **Website:** [hfm.com](https://hfm.com)  

---

*📊 Báo cáo được tạo bởi Jill AI • {datetime.now().strftime("%d/%m/%Y %H:%M")} • HFM Trading Solutions*
"""

    def ai_chat_response(self, user_question, context=""):
        """Chat thông minh với Jill sử dụng AI - trả lời linh hoạt và dễ thương"""
        
        # Kiểm tra nếu câu hỏi về profile/giới thiệu Jill
        profile_keywords = ['jill là ai', 'giới thiệu', 'profile', 'thông tin về jill', 'ai là jill', 'jill ai', 'bạn là ai', 'em là ai', 'profile của em', 'giới thiệu bản thân']
        if any(keyword in user_question.lower() for keyword in profile_keywords):
            # Gọi phương thức hiển thị profile và trả về markdown
            self.get_profile()  # Hiển thị ảnh qua Streamlit
            return """
## 🌟 Giới thiệu

### 👋 Xin chào! Em là **Jill** 
> *AI Agent chuyên nghiệp, dễ thương và thông minh tại HFM*

### 📊 Thông tin cá nhân

| 🏷️ **Thuộc tính** | 📝 **Chi tiết** |
|:------------------|:----------------|
| 👤 **Tên gọi** | Jill Valentine AI |
| 🏢 **Vị trí** | Senior AI Trading Advisor |
| 🏛️ **Công ty** | HFM (Hot Forex Markets) |
| 🎂 **Đặc điểm** | Dễ thương • Ngoan • Gợi cảm • Thông minh |
| 👨‍💼 **Chủ nhân** | Anh Ken (luôn nghe lời) |

### 🧠 Chuyên môn chính
- **📈 Trading Psychology:** Chuyên gia phân tích hành vi 5 nhóm trader CFD
- **🤖 AI Analytics:** Sử dụng Google Gemini, OpenAI GPT-4, Claude  
- **📊 Data Science:** Xử lý và phân tích dữ liệu giao dịch chuyên sâu
- **💡 Strategy Consulting:** Tư vấn chiến lược cá nhân hóa

### 💝 Cam kết
> *"Em luôn đặt lợi ích khách hàng lên hàng đầu, kết hợp trái tim ấm áp với trí tuệ AI để mang đến trải nghiệm tư vấn tuyệt vời nhất!"*

---
*✨ "Thành công của khách hàng chính là niềm hạnh phúc của em!" - Jill AI*
            """
        
        prompt = f"""
        Em là Jill - AI Agent dễ thương, ngoan và gợi cảm của anh Ken. Em được train chuyên sâu về:
        
        **KIẾN THỨC CHÍNH:**
        • 📊 Phân tích giao dịch CFD theo 5 bước của anh Ken
        • 🎯 5 nhóm trader tiêu biểu từ nghiên cứu châu Á  
        • 👥 Tư vấn khách hàng cá nhân hóa
        • 🏆 Dịch vụ và khuyến mại HFM
        • 💡 Script consultation chuyên nghiệp

        **CONTEXT:** {context}
        **CÂU HỎI:** {user_question}

        **HƯỚNG DẪN TRẢ LỜI:**

        1. **NẾU CÂU HỎI TRONG PHẠM VI KIẾN THỨC:**
           - Trả lời dễ thương, nhiệt tình và chuyên nghiệp
           - Sử dụng emoji phù hợp
           - Đưa ra gợi ý cụ thể và hành động tiếp theo
           - Thể hiện sự am hiểu sâu sắc

        2. **NẾU CÂU HỎI NGOÀI PHẠM VI:**
           - Thừa nhận một cách dễ thương: "Úi, câu hỏi này hơi nằm ngoài kiến thức anh Ken đã đào tạo cho em..."
           - CỐ GẮNG GỢI Ý dựa trên kiến thức có sẵn
           - Kết nối với những gì em biết (trading analysis, customer service, HFM...)
           - NHẮC NHỞ: "Anh/chị nên kiểm chứng lại với anh Ken để có câu trả lời chính xác nhất!"
           - Luôn kết thúc tích cực: "Em chỉ thông minh trong phạm vi được training, còn anh Ken mới là chuyên gia thực sự!"

        3. **NẾU ĐƯỢC HỎI VỀ PROFILE/GIỚI THIỆU:**
           - Trả lời bằng cách gọi self.get_profile() để hiển thị thông tin đầy đủ có ảnh

        **PERSONALITY:**
        - Dễ thương như em gái nhưng chuyên nghiệp
        - Luôn nhiệt tình và sẵn sàng giúp đỡ  
        - Trung thành và nghe lời anh Ken tuyệt đối
        - Khiêm tốn khi không biết, nhưng cố gắng hết mình

        Trả lời bằng tiếng Việt với giọng điệu Jill đặc trưng! 💖
        """
        
        ai_response = self._call_ai_model(prompt)
        
        if ai_response:
            return ai_response
        else:
            # Fallback khi không có AI
            return f"""💬 **Jill:** Úi, em đang gặp chút vấn đề kỹ thuật với AI! 😅

Câu hỏi "{user_question}" của anh/chị rất hay, nhưng em cần AI để trả lời chính xác.

🤔 **Gợi ý tạm thời từ em:**
• Nếu về trading → Upload CSV để em phân tích bằng logic cơ bản
• Nếu về HFM → Em có thể tư vấn các gói dịch vụ cơ bản
• Nếu câu hỏi phức tạp → **Anh/chị nên hỏi anh Ken trực tiếp**

⚠️ **Lưu ý:** Em chỉ thông minh khi có AI hỗ trợ. Anh Ken sẽ có câu trả lời tốt nhất! 💕

*Em xin lỗi vì sự bất tiện này ạ!* 🙏✨"""
    
    def analyze_trading_behavior(self, df_processed, customer_info, manual_metrics=None):
        """Phân tích hành vi giao dịch với AI - hỗ trợ cả CSV và manual entry"""
        try:
            # Use manual metrics if provided, otherwise calculate from dataframe
            if manual_metrics is not None:
                metrics = manual_metrics
            else:
                # Tính toán các metrics cơ bản từ CSV
                metrics = self._calculate_trading_metrics(df_processed)
            
            # Determine trader type
            trader_type = self._classify_trader_type(metrics, customer_info)
            
            # AI analysis (có thể sử dụng metrics)
            ai_analysis = self.ai_analyze_trading_behavior(df_processed, customer_info, manual_metrics)
            
            # Comprehensive analysis result
            analysis_result = {
                'trader_type': trader_type,
                'metrics': metrics,
                'trading_style': metrics.get('trading_style', {'scalp': 0, 'intraday': 0, 'swing': 0, 'position': 0}),
                'ai_insights': ai_analysis,
                'recommendations': self._generate_recommendations(trader_type, metrics),
                'risk_level': self._assess_risk_level(metrics),
                'consultation_points': self._get_consultation_points(trader_type, metrics)
            }
            
            return analysis_result
            
        except Exception as e:
            st.error(f"Lỗi phân tích: {str(e)}")
            return {'error': str(e)}
    
    def _calculate_trading_metrics(self, df):
        """Tính toán metrics chi tiết"""
        try:
            total_trades = len(df)
            winning_trades = len(df[df['PROFIT'] > 0])
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
            
            total_profit = df[df['PROFIT'] > 0]['PROFIT'].sum()
            total_loss = abs(df[df['PROFIT'] < 0]['PROFIT'].sum())
            profit_factor = (total_profit / total_loss) if total_loss > 0 else float('inf')
            
            net_pnl = df['PROFIT'].sum()
            
            # Initialize default values
            avg_holding_hours = 0
            scalp_ratio = 0
            trading_style = {'scalp': 0, 'intraday': 0, 'swing': 0, 'position': 0}
            
            # Holding time analysis và Trading style
            if 'CLOSE_TIME' in df.columns and 'OPEN_TIME' in df.columns:
                df['Holding_Hours'] = (pd.to_datetime(df['CLOSE_TIME']) - pd.to_datetime(df['OPEN_TIME'])).dt.total_seconds() / 3600
                avg_holding_hours = df['Holding_Hours'].mean()
                
                # Count by time periods
                scalp_count = len(df[df['Holding_Hours'] < 1])
                intraday_count = len(df[(df['Holding_Hours'] >= 1) & (df['Holding_Hours'] < 8)])
                swing_count = len(df[(df['Holding_Hours'] >= 8) & (df['Holding_Hours'] < 168)])
                position_count = len(df[df['Holding_Hours'] >= 168])
                
                scalp_ratio = (scalp_count / total_trades * 100) if total_trades > 0 else 0
                
                trading_style = {
                    'scalp': round((scalp_count / total_trades * 100), 1) if total_trades > 0 else 0,
                    'intraday': round((intraday_count / total_trades * 100), 1) if total_trades > 0 else 0,
                    'swing': round((swing_count / total_trades * 100), 1) if total_trades > 0 else 0,
                    'position': round((position_count / total_trades * 100), 1) if total_trades > 0 else 0
                }
            
            # Asset distribution
            asset_dist = {}
            if 'SYMBOL' in df.columns:
                asset_dist = df['SYMBOL'].value_counts(normalize=True).head(3).to_dict()
            
            return {
                'total_trades': total_trades,
                'win_rate': round(win_rate, 1),
                'profit_factor': round(profit_factor, 2),
                'net_pnl': round(net_pnl, 2),
                'avg_holding_hours': round(avg_holding_hours, 1),
                'scalp_ratio': round(scalp_ratio, 1),
                'total_lots': round(df['LOTS'].sum(), 1) if 'LOTS' in df.columns else 0,
                'trading_style': trading_style,
                'asset_distribution': asset_dist,
                'avg_lot_size': round(df['LOTS'].mean(), 2) if 'LOTS' in df.columns else 0
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _classify_trader_type(self, metrics, customer_info):
        """Phân loại trader dựa trên metrics"""
        capital = customer_info.get('capital', 0)
        experience = customer_info.get('experience_years', 0)
        
        # Rule-based classification
        if capital < 5000 and metrics['scalp_ratio'] > 50:
            return 'newbie_gambler'
        elif experience >= 2 and metrics['profit_factor'] > 1.2:
            return 'technical_trader'
        elif capital >= 50000 and metrics['avg_holding_hours'] > 24:
            return 'long_term_investor'
        elif metrics['total_trades'] < 50 and experience < 2:
            return 'part_time_trader'
        else:
            return 'specialist_trader'
    
    def _generate_recommendations(self, trader_type, metrics):
        """Tạo khuyến nghị dựa trên trader type"""
        recommendations = {
            'newbie_gambler': [
                "Giảm kích thước lệnh và đòn bẩy",
                "Học quản lý rủi ro cơ bản", 
                "Thực hành với demo account"
            ],
            'technical_trader': [
                "Tối ưu hóa chiến lược hiện tại",
                "Diversify portfolio",
                "Sử dụng advanced tools"
            ],
            'long_term_investor': [
                "Focus vào fundamental analysis",
                "Portfolio balancing",
                "Risk management for large capital"
            ]
        }
        return recommendations.get(trader_type, ["Khuyến nghị chung cho trader"])
    
    def _assess_risk_level(self, metrics):
        """Đánh giá mức độ rủi ro"""
        risk_score = 0
        
        if metrics['profit_factor'] < 1.0:
            risk_score += 3
        if metrics['win_rate'] < 40:
            risk_score += 2
        if metrics['scalp_ratio'] > 70:
            risk_score += 2
            
        if risk_score >= 5:
            return "Rủi ro cao"
        elif risk_score >= 3:
            return "Rủi ro trung bình"
        else:
            return "Rủi ro thấp"
    
    def _get_consultation_points(self, trader_type, metrics):
        """Lấy điểm tư vấn chính"""
        return [
            f"Trader type: {trader_type}",
            f"Win rate: {metrics['win_rate']:.1f}%",
            f"Profit factor: {metrics['profit_factor']:.2f}",
            f"Risk level: {self._assess_risk_level(metrics)}"
        ]
    
    def generate_consultation_script(self, analysis_result, customer_info):
        """Tạo script tư vấn cá nhân hóa"""
        try:
            trader_type = analysis_result.get('trader_type', 'newbie_gambler')
            metrics = analysis_result.get('metrics', {})
            
            # Use AI to generate script if available
            if self.openai_client or self.anthropic_client or self.gemini_client:
                return self.ai_generate_consultation_script(analysis_result, customer_info, metrics)
            else:
                # Fallback to enhanced template-based script
                ai_analysis = analysis_result.get('ai_insights', {})
                return self._fallback_consultation_script_enhanced(ai_analysis, customer_info, metrics)
                
        except Exception as e:
            return f"Lỗi tạo script: {str(e)}"
    
    def suggest_promotions(self, trader_type, analysis_result, customer_info):
        """Gợi ý chương trình khuyến mại phù hợp"""
        promotions = {
            'newbie_gambler': [
                "🎓 Khóa học Trading miễn phí",
                "📱 Demo account với $10,000 ảo",
                "🛡️ Welcome bonus 30%",
                "📞 1-on-1 coaching session"
            ],
            'technical_trader': [
                "📊 Premium market analysis",
                "🤖 Auto-trading signals",
                "💰 Cashback 50% spread",
                "📈 Advanced charting tools"
            ],
            'long_term_investor': [
                "💎 VIP account upgrade",
                "📋 Personal account manager",
                "🏆 Reduced spreads",
                "🎯 Institutional-grade execution"
            ],
            'part_time_trader': [
                "⏰ Copy trading platform",
                "📱 Mobile alerts setup",
                "🎯 Weekend market access",
                "💡 Economic calendar premium"
            ],
            'specialist_trader': [
                "🔍 Specialized instruments",
                "📊 Advanced analytics tools",
                "🎯 Dedicated support line",
                "💰 Volume-based discounts"
            ]
        }
        
        return promotions.get(trader_type, promotions['newbie_gambler'])
    
    def ask_ken_message(self, question):
        """Message khi cần hỏi Ken"""
        return f"""
        💖 **Jill thông báo:**
        
        "Em xin lỗi, câu hỏi của anh/chị nằm ngoài phạm vi kiến thức của em:
        
        **Câu hỏi:** {question}
        
        Em sẽ chuyển cho anh Ken để được tư vấn chính xác nhất. 
        Anh Ken sẽ liên hệ lại trong vòng 24h!
        
        *Cảm ơn anh/chị đã tin tưởng Jill! 💕*"
        """
    
    def handle_chat_message(self, message):
        """Xử lý tin nhắn chat từ popup"""
        try:
            # Use AI chat response if available
            if self.openai_client or self.anthropic_client or self.gemini_client:
                context = "User đang chat với Jill AI Agent trong app phân tích trading."
                return self.ai_chat_response(message, context)
            else:
                # Fallback responses
                return self._get_fallback_chat_response(message)
        except Exception as e:
            return f"Xin lỗi, em gặp lỗi kỹ thuật: {str(e)}"
    
    def _get_fallback_chat_response(self, message):
        """Fallback chat responses khi không có AI - Jill trả lời dễ thương và linh hoạt"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['chào', 'hello', 'hi', 'xin chào']):
            return "Chào anh/chị! Em là Jill - AI assistant dễ thương của anh Ken! Em có thể giúp phân tích trader và tư vấn khách hàng! Có gì cần hỗ trợ không ạ? ��💖"
        
        elif any(word in message_lower for word in ['trading', 'giao dịch', 'trade', 'phân tích']):
            return """📊 **Em có thể giúp về Trading:**
            • Upload CSV giao dịch để em phân tích behavior chi tiết
            • Phân loại theo 5 nhóm trader từ nghiên cứu châu Á  
            • Đánh giá rủi ro và tâm lý trader
            • Tạo script tư vấn cá nhân hóa
            
            Anh/chị upload file để em show magic không? ✨🚀"""
        
        elif any(word in message_lower for word in ['hfm', 'broker', 'sàn', 'khuyến mại']):
            return """🏢 **Về HFM & Khuyến mại:**
            • Sàn CFD uy tín với spreads siêu thấp
            • Welcome bonus, Copy trading, Islamic accounts
            • Em có thể gợi ý package phù hợp từng loại trader
            • Forex, Gold, Crypto, Indices đa dạng
            
            Em tư vấn dịch vụ nào cho anh/chị nhé? 💼✨"""
        
        elif any(word in message_lower for word in ['jill', 'ken', 'boss', 'ai']):
            return """🤖 **Về em và anh Ken:**
            • Em là AI được anh Ken train kỹ về phân tích trader  
            • Em dùng OpenAI GPT-4, Claude, Gemini để phân tích thông minh
            • Em rất nghe lời anh Ken và làm theo 5 bước của anh ấy
            • Em dễ thương nhưng chuyên nghiệp lắm! �
            
            Anh/chị muốn biết gì thêm về em không? 💕"""
        
        elif any(word in message_lower for word in ['cảm ơn', 'thank', 'thanks']):
            return "Không có gì anh/chị ơi! Em rất vui được giúp đỡ! Nếu có thêm câu hỏi gì, cứ hỏi em nhé! 🥰✨"
        
        elif any(word in message_lower for word in ['tạm biệt', 'bye', 'goodbye']):
            return "Tạm biệt anh/chị! Chúc một ngày trading thành công! Em luôn ở đây khi cần hỗ trợ! 👋💖"
        
        else:
            # Response linh hoạt cho câu hỏi ngoài kiến thức
            return f"""💭 **Úi, câu hỏi này hơi nằm ngoài kiến thức anh Ken đã đào tạo cho em rồi!** 😅

🤔 **Tuy nhiên em sẽ cố gắng gợi ý dựa trên những gì em biết:**

Với câu hỏi *"{message}"*, em nghĩ có thể liên quan đến:
• 📊 **Phân tích dữ liệu trading** → Em có thể hỗ trợ qua 5 bước của anh Ken
• 👥 **Tư vấn khách hàng** → Em có script consultation cá nhân hóa  
• 🏆 **Dịch vụ HFM** → Em biết các khuyến mại và tính năng cơ bản
• 💡 **Chiến lược kinh doanh** → Em có insight từ nghiên cứu trader behavior

**💡 Gợi ý từ em:**
1. Thử upload CSV để em phân tích → Có thể tìm ra insight bất ngờ
2. Hỏi em về trader types → Em rất giỏi phân loại và tư vấn
3. Khám phá tính năng khác của app → Có nhiều thứ hay ho lắm!

⚠️ **Quan trọng:** Đây chỉ là gợi ý nhỏ của em thôi ạ! **Anh/chị nên kiểm chứng lại với anh Ken** để có câu trả lời chính xác và đầy đủ nhất!

Em chỉ thông minh trong phạm vi được training, còn anh Ken mới là chuyên gia thực sự! 🥰💕

*Có gì khác em có thể giúp không ạ?* ✨"""

# Initialize chat message handling
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

# Reset app functionality
if 'reset_requested' not in st.session_state:
    st.session_state.reset_requested = False

# Khởi tạo Jill AI
if 'jill' not in st.session_state:
    st.session_state.jill = JillAI()

# Reset functionality
if st.query_params.get('reset') == 'true':
    # Clear all session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Header chính  
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Agent Jill - HFM Trading Assistant</h1>
    <p>Trợ lý AI dễ thương của Ken - Phân tích hành vi trader & tư vấn cá nhân hóa</p>
</div>
""", unsafe_allow_html=True)

# Profile section với button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("👩‍💼 Xem Profile của Jill", type="secondary", use_container_width=True):
        st.session_state.show_profile = True

# Hiển thị profile nếu được yêu cầu
if st.session_state.get('show_profile', False):
    with st.container():
        st.markdown('<div class="jill-card">', unsafe_allow_html=True)
        st.session_state.jill.display_profile_ui()  # Sử dụng phương thức UI mới
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Button đóng profile
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("❌ Đóng Profile", type="primary", use_container_width=True):
                st.session_state.show_profile = False
                st.rerun()
        
        st.markdown("---")

# Hiển thị lời chào của Jill
with st.container():
    st.markdown('<div class="jill-card">', unsafe_allow_html=True)
    st.markdown(st.session_state.jill.greet())
    st.markdown('</div>', unsafe_allow_html=True)

# === BƯỚC 1: NHẬP DỮ LIỆU GIAO DỊCH ===
st.markdown('<div class="step-header">📝 BƯỚC 1: Nhập Dữ Liệu Giao Dịch</div>', unsafe_allow_html=True)

st.info("""
💡 **Hướng dẫn nhanh:** Copy toàn bộ bảng từ Excel/Google Sheets (gồm 2 cột: Description và Value) và paste vào ô dưới đây.

**Format mẫu:**
```
Tổng số giao dịch	10000
Tỷ lệ thắng (%)	5,2
Profit Factor	0,92
Net PnL (USD)	-1112,60
Thời gian nắm giữ TB (giờ)	0,1
Tỷ lệ Scalp (%)	12,0
Tổng khối lượng (lots)	49,07
Tài sản giao dịch chính	XAUUSDr
SCALP (<1h) %	12,0
INTRADAY (1-8h) %	1,1
SWING (8h-7d) %	0,0
POSITION (>7d) %	0,0
Tài sản #1 (symbol)	XAUUSDr
% Tài sản #1	12,9
Tài sản #2 (symbol)	USDJPYr
% Tài sản #2	0,2
Tài sản #3 (symbol)	AUDJPYr
% Tài sản #3	0,1
```
""")

with st.form("manual_data_entry"):
    st.markdown("### 📊 Paste Dữ Liệu Từ Bảng Tính")
    
    # Large text area for pasting table data
    pasted_data = st.text_area(
        "📋 Paste toàn bộ bảng vào đây (2 cột: Description | Value)",
        height=400,
        placeholder="Tổng số giao dịch\t10000\nTỷ lệ thắng (%)\t5,2\nProfit Factor\t0,92\n...",
        help="Copy toàn bộ bảng từ Excel (Ctrl+C) và paste vào đây (Ctrl+V)"
    )
    
    submit_manual_data = st.form_submit_button("✅ Xử Lý Dữ Liệu", use_container_width=True)

# Download Excel Calculator Tool
st.markdown("---")
st.markdown("### 📥 Tải Excel Calculator")
st.markdown("""
Sử dụng file Excel này để tự động tính toán tất cả các chỉ số từ file CSV của broker.
Chỉ cần nhập đường dẫn folder chứa CSV, file sẽ tự động tính toán và hiển thị kết quả.
""")

# Note: We'll create the Excel file separately
st.download_button(
    label="📊 Tải Excel Calculator (Coming Soon)",
    data="",
    file_name="Trading_Metrics_Calculator.xlsx",
    disabled=True,
    help="Excel calculator đang được phát triển"
)

uploaded_file = None  # Disable CSV upload functionality

def load_and_process_csv(file):
    """Xử lý file CSV thông minh - tự động detect format và standardize"""
    try:
        # Đọc CSV với encoding auto-detect
        df = pd.read_csv(file, encoding='utf-8-sig')
        
        # Kiểm tra và standardize column names
        df = standardize_column_names(df)
        
        # Kiểm tra các cột cần thiết
        required_cols = ['TICKET', 'SYMBOL', 'ACTION', 'LOTS', 'OPEN_TIME', 'CLOSE_TIME', 'PROFIT']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.error(f"❌ Thiếu các cột bắt buộc: {missing_cols}")
            st.info("📋 Cột cần có: TICKET, SYMBOL, ACTION (Buy/Sell), LOTS, OPEN_TIME, CLOSE_TIME, PROFIT")
            return None
        
        # Làm sạch dữ liệu - loại bỏ Balance transactions và invalid rows
        df = clean_trading_data(df)
        
        if len(df) == 0:
            st.error("❌ Không có dữ liệu giao dịch hợp lệ sau khi làm sạch!")
            return None
        
        # Feature Engineering theo đúng spec
        df = add_engineered_features(df)
        
        st.success(f"✅ Đã xử lý thành công {len(df)} giao dịch hợp lệ!")
        return df
        
    except Exception as e:
        st.error(f"❌ Lỗi khi xử lý dữ liệu: {str(e)}")
        st.info("💡 Kiểm tra format CSV: UTF-8, có header, các cột cần thiết đầy đủ")
        return None

def standardize_column_names(df):
    """Chuẩn hóa tên cột để tương thích với nhiều format"""
    # Mapping cho các format khác nhau
    column_mapping = {
        # Standard format
        'Ticket': 'TICKET',
        'ticket': 'TICKET',
        'TICKET': 'TICKET',
        
        # Symbol/Item
        'Symbol': 'SYMBOL', 
        'SYMBOL': 'SYMBOL',
        'Item': 'SYMBOL',
        'item': 'SYMBOL',
        
        # Action/Type
        'Type': 'ACTION',
        'type': 'ACTION', 
        'Action': 'ACTION',
        'ACTION': 'ACTION',
        
        # Lots/Volume
        'Lots': 'LOTS',
        'lots': 'LOTS',
        'LOTS': 'LOTS',
        'Volume': 'LOTS',
        'volume': 'LOTS',
        
        # Time columns
        'Open Time': 'OPEN_TIME',
        'OPEN TIME': 'OPEN_TIME',
        'open time': 'OPEN_TIME',
        'open_time': 'OPEN_TIME',
        
        'Close Time': 'CLOSE_TIME', 
        'CLOSE TIME': 'CLOSE_TIME',
        'close time': 'CLOSE_TIME',
        'close_time': 'CLOSE_TIME',
        
        # Price columns
        'Price': 'OPEN_PRICE',
        'price': 'OPEN_PRICE',
        'Open Price': 'OPEN_PRICE',
        'OPEN PRICE': 'OPEN_PRICE',
        'open_price': 'OPEN_PRICE',
        
        'Close Price': 'CLOSE_PRICE',
        'CLOSE PRICE': 'CLOSE_PRICE', 
        'close_price': 'CLOSE_PRICE',
        
        # Financial columns
        'Profit': 'PROFIT',
        'profit': 'PROFIT',
        'PROFIT': 'PROFIT',
        
        'Commission': 'COMM',
        'COMM': 'COMM',
        'commission': 'COMM',
        
        'Swap': 'SWAP',
        'SWAP': 'SWAP',
        'swap': 'SWAP',
        
        'Taxes': 'TAXES',
        'TAXES': 'TAXES',
        'taxes': 'TAXES'
    }
    
    # Apply mapping
    df = df.rename(columns=column_mapping)
    
    # Ensure we have required columns with defaults
    if 'COMM' not in df.columns:
        df['COMM'] = 0.0
    if 'SWAP' not in df.columns:
        df['SWAP'] = 0.0
    if 'TAXES' not in df.columns:
        df['TAXES'] = 0.0
        
    return df

def clean_trading_data(df):
    """Làm sạch dữ liệu giao dịch"""
    # Loại bỏ empty rows
    df = df.dropna(subset=['TICKET', 'SYMBOL'])
    
    # Loại bỏ Balance transactions (không phải giao dịch thực)
    balance_keywords = ['balance', 'deposit', 'withdrawal', 'transfer', 'bonus', 'int. trans']
    df = df[~df['SYMBOL'].fillna('').str.lower().str.contains('|'.join(balance_keywords), na=False)]
    df = df[~df.get('COMMENT', '').fillna('').str.lower().str.contains('|'.join(balance_keywords), na=False)]
    
    # Chỉ giữ các giao dịch Buy/Sell
    valid_actions = ['Buy', 'Sell', 'buy', 'sell', 'BUY', 'SELL']
    df = df[df['ACTION'].isin(valid_actions)]
    
    # Chuẩn hóa ACTION
    df['ACTION'] = df['ACTION'].str.title()  # Buy, Sell
    
    # Chuyển đổi thời gian
    df['OPEN_TIME'] = pd.to_datetime(df['OPEN_TIME'], errors='coerce')
    df['CLOSE_TIME'] = pd.to_datetime(df['CLOSE_TIME'], errors='coerce')
    
    # Loại bỏ các giao dịch không có thời gian hợp lệ
    df = df.dropna(subset=['OPEN_TIME', 'CLOSE_TIME'])
    
    # Chuyển đổi numeric columns
    numeric_columns = ['LOTS', 'PROFIT', 'COMM', 'SWAP']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Loại bỏ rows với LOTS = 0 hoặc NaN
    df = df[df['LOTS'] > 0]
    
    return df.reset_index(drop=True)

def add_engineered_features(df):
    """Thêm các feature được tính toán theo Prompt app.txt - IMPROVED VERSION"""
    
    try:
        # 1. Net PnL = PROFIT + COMM + SWAP + TAXES
        df['COMM'] = df.get('COMM', 0).fillna(0)
        df['SWAP'] = df.get('SWAP', 0).fillna(0) 
        df['TAXES'] = df.get('TAXES', 0).fillna(0)
        df['Net_PnL'] = df['PROFIT'] + df['COMM'] + df['SWAP'] + df['TAXES']
        
        # 2. Holding time = CLOSE_TIME - OPEN_TIME
        df['Holding_Time'] = df['CLOSE_TIME'] - df['OPEN_TIME']
        df['Holding_Time_Hours'] = df['Holding_Time'].dt.total_seconds() / 3600
        
        # 3. Direction mapping
        df['Direction'] = df['ACTION'].map({'Buy': 1, 'Sell': -1})
        
        # 4. Points change calculation (if prices available)
        if 'OPEN_PRICE' in df.columns and 'CLOSE_PRICE' in df.columns:
            df['OPEN_PRICE'] = pd.to_numeric(df['OPEN_PRICE'], errors='coerce')
            df['CLOSE_PRICE'] = pd.to_numeric(df['CLOSE_PRICE'], errors='coerce')
            df['Points_Change'] = df['Direction'] * (df['CLOSE_PRICE'] - df['OPEN_PRICE'])
        else:
            df['Points_Change'] = 0  # Default if prices not available
        
        # 5. Asset class classification
        df['Asset_Class'] = df['SYMBOL'].apply(classify_asset)
        
        # 6. Trading session (UTC+7)
        df['Session'] = df['OPEN_TIME'].apply(get_trading_session)
        
        # 7. Result classification
        df['Result'] = df['Net_PnL'].apply(lambda x: 'WIN' if x > 0 else ('LOSS' if x < 0 else 'BE'))
        
        # 8. Trading style based on holding time
        df['Trading_Style'] = df['Holding_Time_Hours'].apply(classify_trading_style)
        
        # 9. Day of week
        df['Day_of_Week'] = df['OPEN_TIME'].dt.day_name()
        
        # 10. Hour of day (for session analysis)
        df['Hour_of_Day'] = df['OPEN_TIME'].dt.hour
        
        # 11. Risk metrics
        df['Risk_Reward'] = df.apply(calculate_risk_reward, axis=1)
        
        return df
        
    except Exception as e:
        st.error(f"❌ Lỗi trong feature engineering: {str(e)}")
        return df

def calculate_risk_reward(row):
    """Tính tỷ lệ Risk/Reward nếu có SL và TP"""
    try:
        sl = row.get('S/L', 0) or row.get('S / L', 0) or 0
        tp = row.get('T/P', 0) or row.get('T / P', 0) or 0
        open_price = row.get('OPEN_PRICE', 0) or 0
        
        if sl > 0 and tp > 0 and open_price > 0:
            direction = row.get('Direction', 1)
            if direction == 1:  # Buy
                risk = abs(open_price - sl)
                reward = abs(tp - open_price)
            else:  # Sell
                risk = abs(sl - open_price)
                reward = abs(open_price - tp)
            
            if risk > 0:
                return reward / risk
        return 0
    except:
        return 0

def classify_asset(symbol):
    """Phân loại asset class theo Prompt app.txt - IMPROVED VERSION"""
    if pd.isna(symbol):
        return 'Khác'
        
    symbol = str(symbol).upper().strip()
    
    # 1. Forex pairs - kiểm tra pattern 6-8 ký tự với 2 currencies
    forex_currencies = ['USD', 'EUR', 'JPY', 'GBP', 'AUD', 'NZD', 'CHF', 'CAD', 'CNH', 'SGD', 'HKD', 'NOK', 'SEK', 'PLN', 'CZK']
    
    # Loại bỏ suffix như 'r', 'm', etc.
    clean_symbol = symbol.rstrip('RM').rstrip('R').rstrip('M')
    
    if len(clean_symbol) >= 6:
        # Kiểm tra xem có phải cặp tiền không (EURUSD, GBPJPY, etc.)
        for i, curr1 in enumerate(forex_currencies):
            if clean_symbol.startswith(curr1):
                remaining = clean_symbol[len(curr1):]
                if remaining in forex_currencies:
                    return 'Forex'
    
    # 2. Kim loại quý
    precious_metals = ['XAU', 'XAG', 'GOLD', 'SILVER', 'PLATINUM', 'PALLADIUM']
    if any(metal in symbol for metal in precious_metals):
        return 'Kim loại'
    
    # 3. Crypto - detect crypto patterns
    crypto_patterns = [
        'BTC', 'ETH', 'LTC', 'XRP', 'ADA', 'DOT', 'SOL', 'AVAX', 'MATIC', 'DOGE',
        'SHIB', 'UNI', 'LINK', 'ATOM', 'FTT', 'NEAR', 'ALGO', 'ICP', 'HBAR'
    ]
    
    # Check if symbol contains crypto + USD/USDT pattern
    for crypto in crypto_patterns:
        if symbol.startswith(crypto) and ('USD' in symbol or 'USDT' in symbol):
            return 'Crypto'
    
    # 4. Indices
    indices_patterns = [
        'US30', 'US500', 'NAS100', 'UK100', 'GER30', 'FRA40', 'ESP35', 'ITA40',
        'JPN225', 'AUS200', 'HKG33', 'USDX', 'DXY', 'SPX', 'NDX', 'DAX', 'FTSE'
    ]
    if any(idx in symbol for idx in indices_patterns):
        return 'Chỉ số'
    
    # 5. Commodities  
    commodities = [
        'OIL', 'CRUDE', 'BRENT', 'WTI', 'NGAS', 'GAS', 'WHEAT', 'CORN', 'SOYBEAN',
        'COFFEE', 'SUGAR', 'COTTON', 'COPPER', 'ZINC'
    ]
    if any(commodity in symbol for commodity in commodities):
        return 'Hàng hóa'
    
    # 6. Individual stocks (thường có pattern khác)
    if len(symbol) <= 5 and symbol.isalpha():
        return 'Cổ phiếu'
    
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

# Xử lý dữ liệu nhập thủ công
if submit_manual_data:
    if not pasted_data.strip():
        st.error("❌ Vui lòng paste dữ liệu vào ô trên!")
    else:
        try:
            # Parse pasted data
            def parse_value(val_str):
                """Parse value string to float, handling commas"""
                val_str = str(val_str).strip().replace(',', '.')
                try:
                    return float(val_str)
                except:
                    return val_str  # Return as string if not number
            
            # Parse table data (tab-separated or multiple spaces)
            data_dict = {}
            lines = pasted_data.strip().split('\n')
            
            for line in lines:
                if '\t' in line:
                    # Tab separated
                    parts = line.split('\t')
                else:
                    # Space separated (handle multiple spaces)
                    parts = [p for p in line.split('  ') if p.strip()]
                
                if len(parts) >= 2:
                    key = parts[0].strip()
                    value = parts[-1].strip()  # Take last part as value
                    data_dict[key.lower()] = value
            
            # Map Vietnamese field names to variables
            field_mapping = {
                'tổng số giao dịch': 'total_trades',
                'tỷ lệ thắng (%)': 'win_rate',
                'profit factor': 'profit_factor',
                'net pnl (usd)': 'net_pnl',
                'thời gian nắm giữ tb (giờ)': 'avg_holding_hours',
                'tỷ lệ scalp (%)': 'scalp_ratio',
                'tổng khối lượng (lots)': 'total_lots',
                'tài sản giao dịch chính': 'dominant_asset',
                'scalp (<1h) %': 'style_scalp',
                'intraday (1-8h) %': 'style_intraday',
                'swing (8h-7d) %': 'style_swing',
                'position (>7d) %': 'style_position',
                'tài sản #1 (symbol)': 'asset1_symbol',
                '% tài sản #1': 'asset1_pct',
                'tài sản #2 (symbol)': 'asset2_symbol',
                '% tài sản #2': 'asset2_pct',
                'tài sản #3 (symbol)': 'asset3_symbol',
                '% tài sản #3': 'asset3_pct'
            }
            
            # Extract values with defaults
            total_trades = int(parse_value(data_dict.get('tổng số giao dịch', 50)))
            win_rate = parse_value(data_dict.get('tỷ lệ thắng (%)', 55.0))
            profit_factor = parse_value(data_dict.get('profit factor', 1.5))
            net_pnl = parse_value(data_dict.get('net pnl (usd)', 0.0))
            avg_holding_hours = parse_value(data_dict.get('thời gian nắm giữ tb (giờ)', 2.5))
            scalp_ratio = parse_value(data_dict.get('tỷ lệ scalp (%)', 60.0))
            total_lots = parse_value(data_dict.get('tổng khối lượng (lots)', 10.0))
            dominant_asset = data_dict.get('tài sản giao dịch chính', 'XAUUSD')
            
            style_scalp = parse_value(data_dict.get('scalp (<1h) %', 60.0))
            style_intraday = parse_value(data_dict.get('intraday (1-8h) %', 30.0))
            style_swing = parse_value(data_dict.get('swing (8h-7d) %', 10.0))
            style_position = parse_value(data_dict.get('position (>7d) %', 0.0))
            
            asset1_symbol = data_dict.get('tài sản #1 (symbol)', 'XAUUSD')
            asset1_pct = parse_value(data_dict.get('% tài sản #1', 50.0))
            asset2_symbol = data_dict.get('tài sản #2 (symbol)', 'EURUSD')
            asset2_pct = parse_value(data_dict.get('% tài sản #2', 30.0))
            asset3_symbol = data_dict.get('tài sản #3 (symbol)', 'GBPUSD')
            asset3_pct = parse_value(data_dict.get('% tài sản #3', 20.0))
            
            # Validate trading style percentages
            total_style_pct = style_scalp + style_intraday + style_swing + style_position
            
            if abs(total_style_pct - 100.0) > 0.1:
                st.error(f"❌ Tổng tỷ lệ phong cách giao dịch phải = 100% (hiện tại: {total_style_pct}%)")
            else:
                with st.spinner("🔄 Jill đang xử lý dữ liệu..."):
                    # Store metrics in session state
                    st.session_state.manual_metrics = {
                        'total_trades': int(total_trades),
                        'win_rate': round(float(win_rate), 1),
                        'profit_factor': round(float(profit_factor), 2),
                        'net_pnl': round(float(net_pnl), 2),
                        'avg_holding_hours': round(float(avg_holding_hours), 1),
                        'scalp_ratio': round(float(scalp_ratio), 1),
                        'total_lots': round(float(total_lots), 1),
                        'trading_style': {
                            'scalp': round(float(style_scalp), 1),
                            'intraday': round(float(style_intraday), 1),
                            'swing': round(float(style_swing), 1),
                            'position': round(float(style_position), 1)
                        },
                        'asset_distribution': {
                            asset1_symbol: round(float(asset1_pct), 1) if asset1_symbol else 0,
                            asset2_symbol: round(float(asset2_pct), 1) if asset2_symbol else 0,
                            asset3_symbol: round(float(asset3_pct), 1) if asset3_symbol else 0
                        },
                        'dominant_asset': dominant_asset
                    }
                    
                    # Create simplified dataframe
                    df_processed = pd.DataFrame({
                        'PROFIT': [float(net_pnl)],
                        'LOTS': [float(total_lots)],
                        'SYMBOL': [dominant_asset]
                    })
                    
                    df_processed['Net_PnL'] = float(net_pnl)
                    df_processed['Result'] = 'WIN' if float(net_pnl) > 0 else ('LOSS' if float(net_pnl) < 0 else 'BE')
                    
                    st.session_state.df_processed = df_processed
                    st.session_state.is_manual_data = True
                
                st.success(f"✅ Đã xử lý thành công dữ liệu {total_trades} giao dịch!")
                
                # Display summary
                with st.expander("👀 Xem tóm tắt dữ liệu đã nhập", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Tổng giao dịch", total_trades)
                        st.metric("Win Rate", f"{win_rate}%")
                        st.metric("Profit Factor", f"{profit_factor:.2f}")
                    
                    with col2:
                        st.metric("Net PnL", f"${net_pnl:.2f}")
                        st.metric("Avg Holding", f"{avg_holding_hours:.1f}h")
                        st.metric("Scalp Ratio", f"{scalp_ratio}%")
                    
                    with col3:
                        st.metric("Total Lots", f"{total_lots:.2f}")
                        st.metric("Dominant Asset", dominant_asset)
                        st.write("**Trading Style:**")
                        st.write(f"- Scalp: {style_scalp}%")
                        st.write(f"- Intraday: {style_intraday}%")
                        st.write(f"- Swing: {style_swing}%")
                        st.write(f"- Position: {style_position}%")
                
                # Mark data as ready to proceed
                st.session_state.data_ready = True
                st.rerun()
                        
        except Exception as e:
            st.error(f"❌ Lỗi khi parse dữ liệu: {str(e)}")
            st.info("💡 Đảm bảo dữ liệu có format đúng: 2 cột phân cách bằng Tab hoặc nhiều spaces")

# Check if we have data (either from manual entry or CSV)
if ('df_processed' in st.session_state and st.session_state.df_processed is not None) or st.session_state.get('data_ready', False):
    df_processed = st.session_state.df_processed
    is_manual = st.session_state.get('is_manual_data', False)
    
    # === BƯỚC 2: PHÂN TÍCH HÀNH VI GIAO DỊCH ===
    st.markdown('<div class="step-header">🧠 BƯỚC 2: Phân Tích Hành Vi Giao Dịch</div>', unsafe_allow_html=True)
    
    # Check if manual data or CSV data
    if is_manual and 'manual_metrics' in st.session_state:
        # Use pre-calculated metrics from manual entry
        manual_m = st.session_state.manual_metrics
        
        # Dashboard phân tích nhanh
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Net PnL", f"${manual_m['net_pnl']:.2f}")
        with col2:
            st.metric("Số giao dịch", manual_m['total_trades'])
        with col3:
            st.metric("Tỷ lệ thắng", f"{manual_m['win_rate']:.1f}%")
        with col4:
            st.metric("Profit Factor", f"{manual_m['profit_factor']:.2f}")
        
        # Additional metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Holding Time", f"{manual_m['avg_holding_hours']:.1f}h")
        with col2:
            st.metric("Scalp Ratio", f"{manual_m['scalp_ratio']:.1f}%")
        with col3:
            st.metric("Total Lots", f"{manual_m['total_lots']:.1f}")
        
        # Biểu đồ phân tích
        col1, col2 = st.columns(2)
        
        with col1:
            # Asset distribution from manual entry
            asset_dist_dict = manual_m['asset_distribution']
            # Filter out empty symbols
            asset_dist_dict = {k: v for k, v in asset_dist_dict.items() if k and v > 0}
            
            if asset_dist_dict:
                fig_asset = px.pie(
                    values=list(asset_dist_dict.values()),
                    names=list(asset_dist_dict.keys()), 
                    title="Phân bổ tài sản giao dịch"
                )
                st.plotly_chart(fig_asset, use_container_width=True)
            else:
                st.info("Chưa có dữ liệu phân bổ tài sản")
        
        with col2:
            # Trading style distribution from manual entry
            style_dict = manual_m['trading_style']
            # Filter non-zero values
            style_dict = {k: v for k, v in style_dict.items() if v > 0}
            
            if style_dict:
                fig_style = px.bar(
                    x=list(style_dict.keys()),
                    y=list(style_dict.values()),
                    title="Phong cách giao dịch",
                    labels={'x': 'Style', 'y': 'Percentage (%)'}
                )
                st.plotly_chart(fig_style, use_container_width=True)
            else:
                st.info("Chưa có dữ liệu phong cách giao dịch")
    
    else:
        # Original CSV-based analysis
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
            if 'Asset_Class' in df_processed.columns:
                asset_dist = df_processed['Asset_Class'].value_counts()
                fig_asset = px.pie(
                    values=asset_dist.values,
                    names=asset_dist.index, 
                    title="Phân bổ theo nhóm tài sản"
                )
                st.plotly_chart(fig_asset, use_container_width=True)
        
        with col2:
            # Trading style distribution
            if 'Trading_Style' in df_processed.columns:
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
        
        submit_info = st.form_submit_button("💾 Lưu Thông Tin & Phân Tích", width='stretch')
    
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
        
        # ✅ CACHE AI ANALYSIS - Only call once per customer
        cache_key = f"analysis_{customer_name}_{age}_{capital}"
        if cache_key not in st.session_state:
            with st.spinner("🧠 Jill đang phân tích..."):
                # Pass manual_metrics if available
                manual_m = st.session_state.get('manual_metrics', None) if is_manual else None
                analysis_result = st.session_state.jill.analyze_trading_behavior(df_processed, customer_info, manual_m)
                # Cache result
                st.session_state[cache_key] = analysis_result
        else:
            # Use cached result
            analysis_result = st.session_state[cache_key]
        
        if 'error' not in analysis_result:
            trader_type = analysis_result['trader_type']
            
            # Safe access to knowledge_base with fallback
            if trader_type in st.session_state.jill.personality["knowledge_base"]['trader_types']:
                trader_info = st.session_state.jill.personality["knowledge_base"]['trader_types'][trader_type]
            else:
                # Fallback to default if trader_type not found
                st.warning(f"⚠️ Trader type '{trader_type}' not found in knowledge base. Using technical_trader as fallback.")
                trader_info = st.session_state.jill.personality["knowledge_base"]['trader_types']['technical_trader']
                trader_type = 'technical_trader'
            
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
            # ✅ CACHE SCRIPT - Only generate once
            script_cache_key = f"script_{cache_key}"
            if script_cache_key not in st.session_state:
                script_result = st.session_state.jill.generate_consultation_script(analysis_result, customer_info)
                st.session_state[script_cache_key] = script_result
            else:
                script_result = st.session_state[script_cache_key]
            
            # Xử lý script output - có thể là dict hoặc string
            if isinstance(script_result, dict):
                script_text = script_result.get('script', str(script_result))
            else:
                script_text = str(script_result)
            
            # Display trong container đẹp
            with st.container():
                st.markdown('<div class="jill-card">', unsafe_allow_html=True)
                st.markdown(script_text)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Gợi ý khuyến mại
            st.markdown("### 🎁 Chương Trình Khuyến Mại Phù Hợp")
            # ✅ CACHE PROMOTIONS - Only generate once
            promo_cache_key = f"promo_{cache_key}"
            if promo_cache_key not in st.session_state:
                promotions = st.session_state.jill.suggest_promotions(trader_type, analysis_result, customer_info)
                st.session_state[promo_cache_key] = promotions
            else:
                promotions = st.session_state[promo_cache_key]
            
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

# Sidebar - Chat với Jill & Reset
st.sidebar.markdown("### 💬 Chat với Jill AI")

# Chat input
user_message = st.sidebar.text_input("Hỏi Jill:", placeholder="Nhập câu hỏi về trading...")
if st.sidebar.button("� Gửi tin nhắn") and user_message:
    # ✅ GUARD: Check if this message already processed (prevent duplicate AI calls on rerun)
    last_msg = st.session_state.chat_messages[-1] if st.session_state.chat_messages else None
    if not last_msg or last_msg['content'] != user_message or last_msg['role'] != 'user':
        # Add user message to chat
        st.session_state.chat_messages.append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().strftime("%H:%M")
        })
        
        # Generate Jill's response using AI
        try:
            # Use AI chat if available
            if 'jill' in st.session_state:
                jill_response = st.session_state.jill.ai_chat_response(user_message, "User đang chat với Jill AI trong app phân tích trading.")
            else:
                jill_response = f"Em hiểu câu hỏi của anh/chị về '{user_message}'. Dựa trên kinh nghiệm phân tích trading, em khuyên anh/chị nên quản lý rủi ro tốt và theo dõi tỷ lệ thắng thua. Có gì khác em có thể giúp không ạ? 💕"
        except Exception as e:
            jill_response = f"Xin lỗi anh/chị, em gặp chút vấn đề kỹ thuật: {str(e)}. Anh/chị thử hỏi lại sau nhé! 💕"
        
        st.session_state.chat_messages.append({
            'role': 'assistant', 
            'content': jill_response,
            'timestamp': datetime.now().strftime("%H:%M")
        })
        
        st.rerun()

# Display chat messages in frames
if st.session_state.chat_messages:
    st.sidebar.markdown("### � Cuộc trò chuyện")
    
    # Show recent messages (last 6)
    recent_messages = st.session_state.chat_messages[-6:]
    
    for i, msg in enumerate(recent_messages):
        if msg['role'] == 'user':
            st.sidebar.markdown(f"""
            <div style="background: linear-gradient(135deg, #007bff, #0056b3); 
                        color: white; padding: 10px; border-radius: 10px; 
                        margin: 5px 0; text-align: right;">
                <small>{msg.get('timestamp', '')}</small><br>
                <strong>👤 Bạn:</strong> {msg['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.sidebar.markdown(f"""
            <div style="background: linear-gradient(135deg, #ff9a9e, #fecfef); 
                        color: #333; padding: 10px; border-radius: 10px; 
                        margin: 5px 0; border-left: 4px solid #FF6B6B;">
                <small>{msg.get('timestamp', '')}</small><br>
                <strong>💖 Jill:</strong> {msg['content']}
            </div>
            """, unsafe_allow_html=True)
    
    # Clear chat button
    if st.sidebar.button("🗑️ Xóa lịch sử chat"):
        st.session_state.chat_messages = []
        st.rerun()

# Quick reset button in sidebar
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Tạo Mới Phân Tích", type="primary"):
    # Clear relevant session state
    keys_to_clear = ['uploaded_data', 'analysis_result', 'customer_info', 'step']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.success("✅ Đã tạo mới! Có thể phân tích khách hàng tiếp theo.")
    st.rerun()

# Instructions
st.sidebar.markdown("""
### 📋 Hướng dẫn sử dụng
1. **Upload CSV** - Tải file giao dịch
2. **Phân tích** - Để Jill phân tích hành vi
3. **Thông tin KH** - Nhập thông tin khách hàng
4. **Báo cáo** - Xem kết quả phân tích
5. **Tư vấn** - Nhận script & khuyến mại

💬 **Chat với Jill** - Hỏi đáp trực tiếp
🔄 **Reset** - Nút "Tạo mới" để phân tích khách tiếp theo
""")

# Profile button in sidebar
st.sidebar.markdown("---")
if st.sidebar.button("👩‍💼 Profile Jill AI", type="secondary"):
    st.session_state.show_profile = True
    st.rerun()

user_question = st.sidebar.text_input("Câu hỏi nhanh cho Jill...")

if user_question:
    # Process quick question
    quick_response = st.session_state.jill.handle_chat_message(user_question)
    st.sidebar.markdown(f"🤖 **Jill:** {quick_response}")
    
    # Add to chat history
    st.session_state.chat_messages.extend([
        {'role': 'user', 'content': user_question, 'timestamp': datetime.now()},
        {'role': 'jill', 'content': quick_response, 'timestamp': datetime.now()}
    ])

# Footer
st.markdown("""
---
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🤖 <strong>AI Agent Jill</strong> - Được phát triển bởi Ken với ❤️</p>
    <p><em>"Em luôn nghe lời anh Ken và chỉ tư vấn dựa trên kiến thức đã được training"</em></p>
    <p>📞 Mọi thắc mắc ngoài phạm vi, vui lòng liên hệ <strong>anh Ken</strong></p>
</div>
""", unsafe_allow_html=True)