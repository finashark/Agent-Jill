# 🚀 Jill AI Agent - Streamlit Cloud Deployment Guide

## 📋 Bước 1: Chuẩn Bị Repository

### GitHub Repository Setup
1. Tạo repository mới trên GitHub: `jill-ai-agent`
2. Push toàn bộ code từ folder này lên repo
3. Đảm bảo các files quan trọng:
   - `app.py` (main application)
   - `requirements.txt` (dependencies)
   - `README.md` (documentation)
   - `.streamlit/config.toml` (theme config)

## 🔐 Bước 2: Config API Keys trên Streamlit Cloud

### Secrets Management
1. Vào Streamlit Cloud dashboard
2. Chọn app của bạn
3. Vào Settings > Secrets
4. Thêm các secrets sau:

```toml
# Streamlit secrets format
OPENAI_API_KEY = "sk-your-openai-key"
ANTHROPIC_API_KEY = "sk-ant-your-anthropic-key"
GOOGLE_API_KEY = "your-google-api-key"
```

## 🌐 Bước 3: Deploy trên Streamlit Cloud

### Deployment Steps
1. Truy cập https://share.streamlit.io/
2. Đăng nhập bằng GitHub account
3. Click "New app"
4. Chọn repository: `jill-ai-agent`
5. Main file path: `app.py`
6. Click "Deploy!"

## ⚙️ Bước 4: Kiểm Tra App

### Health Check
- ✅ App loads without errors
- ✅ CSV upload works
- ✅ AI models initialize (check sidebar)
- ✅ 5-step workflow functions
- ✅ Charts render correctly

## 🔧 Troubleshooting

### Common Issues
1. **Import Errors**: Check requirements.txt có đầy đủ packages
2. **AI API Errors**: Verify API keys trong Streamlit secrets
3. **Memory Issues**: Optimize data processing for large CSV files
4. **Timeout**: Add progress bars cho long-running operations

### Debug Mode
Để debug trên local:
```bash
streamlit run app.py --logger.level debug
```

## 📊 App Features Ready for Production

### Core Functionality
- ✅ CSV data upload & processing
- ✅ AI-powered behavior analysis
- ✅ Customer information collection
- ✅ Smart reporting with charts
- ✅ AI consultation script generation

### AI Integration
- ✅ OpenAI GPT-4 for analysis
- ✅ Anthropic Claude for backup
- ✅ Google Gemini for additional insights
- ✅ Fallback mode when AI unavailable

### UI/UX
- ✅ Professional Streamlit theme
- ✅ Responsive layout
- ✅ Progress indicators
- ✅ Error handling with user feedback

## 🎯 Production URL
Sau khi deploy, app sẽ có URL dạng:
`https://share.streamlit.io/[username]/jill-ai-agent/main/app.py`

## 💡 Tips for Success
1. Test thoroughly với sample CSV data
2. Monitor API usage limits
3. Keep dependencies minimal để tránh conflicts
4. Use Streamlit caching cho performance
5. Add analytics tracking if needed

---
**🤖 Jill AI Agent ready for production deployment!**