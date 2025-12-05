"""
Streamlit Trading Advisor Application

This application analyzes trading behavior and provides personalized advice
based on user profile and historical trading data.
"""

import streamlit as st
import pandas as pd
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from user_profile import UserProfile
from data_loader import TradeDataLoader
from metrics_calculator import PerformanceMetrics
from trader_classifier import TraderClassifier
from advisor_en import TradingAdvisor
from pdf_generator_v2 import PDFReportGeneratorV2 as PDFReportGenerator
from visualizations import (
    plot_pnl_timeline,
    plot_symbol_distribution,
    plot_win_loss_distribution,
    plot_trading_hours_heatmap,
    plot_holding_time_boxplot,
    plot_trader_profile_radar,
    plot_daily_pnl,
    create_metrics_cards
)

# Page configuration
st.set_page_config(
    page_title="Trading Advisor AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/sharkmeai',
        'Report a bug': 'https://github.com/sharkmeai/issues',
        'About': 'Trading Advisor AI v1.0 - Phân tích hành vi giao dịch và tư vấn cá nhân hóa'
    }
)

# Initialize session state
if 'profile_data' not in st.session_state:
    st.session_state.profile_data = None
if 'trade_data' not in st.session_state:
    st.session_state.trade_data = None
if 'metrics' not in st.session_state:
    st.session_state.metrics = None
if 'classification' not in st.session_state:
    st.session_state.classification = None
if 'advisory' not in st.session_state:
    st.session_state.advisory = None

# App header
st.title("📈 Trading Advisor AI")
st.markdown("""
Ứng dụng phân tích hành vi giao dịch và đưa ra lời tư vấn cá nhân hóa 
dựa trên dữ liệu thực tế và hồ sơ của bạn.
""")

# Sidebar navigation
st.sidebar.title("📋 Navigation")
tab_selection = st.sidebar.radio(
    "Chọn phần:",
    ["🏠 Giới thiệu", "👤 Hồ sơ người dùng", "📊 Dữ liệu giao dịch", 
     "📈 Dashboard", "🔍 Phân tích chi tiết", "🎯 Phân loại", "💡 Tư vấn"]
)

# Tab 1: Introduction
if tab_selection == "🏠 Giới thiệu":
    st.header("Chào mừng đến với Trading Advisor AI")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Mục đích")
        st.write("""
        Ứng dụng giúp bạn:
        - Phân tích hành vi giao dịch từ lịch sử thực tế
        - Xác định phong cách trading của bạn
        - Nhận tư vấn cá nhân hóa để cải thiện hiệu suất
        - Nhận diện các bias tâm lý trong giao dịch
        """)
        
        st.subheader("🚀 Cách sử dụng")
        st.write("""
        1. **Điền hồ sơ**: Cung cấp thông tin cá nhân và mục tiêu
        2. **Tải dữ liệu**: Copy/paste hoặc upload file CSV lịch sử giao dịch
        3. **Xem phân tích**: Dashboard và biểu đồ chi tiết
        4. **Nhận phân loại**: Khám phá trader type của bạn
        5. **Đọc tư vấn**: Nhận recommendations để cải thiện
        """)
    
    with col2:
        st.subheader("📊 5 Loại Trader")
        st.write("""
        **1. Newbie Gambler** 🎲
        - Mới bắt đầu, mạo hiểm cao
        - Cần học quản lý rủi ro
        
        **2. Technical Day/Swing Trader** 📈
        - Có kinh nghiệm, kỷ luật tốt
        - Dùng phân tích kỹ thuật
        
        **3. Long-term Value Investor** 💰
        - Đầu tư dài hạn, thận trọng
        - Tầm nhìn xa, kiên nhẫn
        
        **4. Part-time Opportunist** ⏰
        - Bán thời gian, cân bằng tốt
        - Trading song song công việc chính
        
        **5. Asset Specialist** 🎯
        - Chuyên sâu một loại tài sản
        - Expert trong lĩnh vực hẹp
        """)
    
    st.info("👈 Bắt đầu bằng cách chọn **'👤 Hồ sơ người dùng'** ở sidebar")

# Tab 2: User Profile
elif tab_selection == "👤 Hồ sơ người dùng":
    st.header("👤 Thông tin hồ sơ")
    
    user_profile = UserProfile()
    
    # Section 1: Basic Info
    basic_info = user_profile.collect_basic_info()
    
    # Section 2: Financial Info
    financial_info = user_profile.collect_financial_info()
    
    # Section 3: Experience & Goals
    exp_goals = user_profile.collect_experience_goals()
    
    # Section 4: Self Assessment
    assessment = user_profile.collect_self_assessment()
    
    # Save profile button
    if st.button("💾 Lưu hồ sơ", type="primary", use_container_width=True):
        # Combine all data
        profile_data = {**basic_info, **financial_info, **exp_goals, **assessment}
        
        # Validate
        if user_profile.validate_profile(profile_data):
            st.session_state.profile_data = profile_data
            st.success("✅ Đã lưu hồ sơ thành công!")
            st.balloons()
            
            # Show summary
            with st.expander("📋 Xem tóm tắt hồ sơ"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Name", profile_data['name'])
                    st.metric("Age", profile_data['age'])
                    st.metric("Gender", profile_data['gender'])
                with col2:
                    st.metric("Education", profile_data['education'])
                    st.metric("Income", profile_data['income'])
                    st.metric("Capital", f"${profile_data['capital']:,}")
                with col3:
                    st.metric("Experience", profile_data['experience'])
                    st.metric("Risk", f"{profile_data['risk_tolerance']}/10")
                    st.metric("Time", profile_data['available_time'])
        else:
            st.error("❌ Vui lòng điền đầy đủ các trường bắt buộc!")
    
    # Show saved profile
    if st.session_state.profile_data:
        st.info("✅ Hồ sơ đã được lưu. Tiếp tục với phần **'📊 Dữ liệu giao dịch'**")

# Tab 3: Trade Data
elif tab_selection == "📊 Dữ liệu giao dịch":
    st.header("📊 Tải dữ liệu giao dịch")
    
    if not st.session_state.profile_data:
        st.warning("⚠️ Vui lòng điền **Hồ sơ người dùng** trước!")
        st.stop()
    
    data_loader = TradeDataLoader()
    
    # Input method selection
    input_method = st.radio(
        "Chọn phương thức nhập liệu:",
        ["📋 Copy/Paste CSV", "📁 Upload File"],
        horizontal=True
    )
    
    trades_df = None
    
    if input_method == "📋 Copy/Paste CSV":
        st.info("""
        📌 **Hướng dẫn:**
        1. Mở file Excel/CSV lịch sử giao dịch
        2. Chọn tất cả dữ liệu (bao gồm header)
        3. Copy (Ctrl+C)
        4. Paste vào ô bên dưới
        """)
        
        csv_text = st.text_area(
            "Paste dữ liệu CSV vào đây:",
            height=300,
            placeholder="TICKET,SYMBOL,ACTION,LOTS,OPEN TIME,CLOSE TIME,PROFIT,COMM,SWAP..."
        )
        
        if st.button("🔄 Phân tích dữ liệu", type="primary"):
            if csv_text.strip():
                try:
                    with st.spinner("Đang xử lý dữ liệu..."):
                        trades_df = data_loader.parse_csv_string(csv_text)
                        if trades_df is not None and len(trades_df) > 0:
                            st.session_state.trade_data = trades_df
                            st.success(f"✅ Đã tải {len(trades_df)} giao dịch!")
                            logger.info(f"Loaded {len(trades_df)} trades successfully")
                        else:
                            st.error("❌ Không thể đọc dữ liệu. Vui lòng kiểm tra định dạng!")
                            logger.warning("Failed to parse CSV data")
                except Exception as e:
                    st.error(f"❌ Lỗi xử lý dữ liệu: {str(e)}")
                    logger.error(f"CSV parsing error: {str(e)}", exc_info=True)
            else:
                st.warning("⚠️ Vui lòng paste dữ liệu CSV!")
    
    else:  # File upload
        uploaded_file = st.file_uploader(
            "Chọn file CSV:",
            type=['csv', 'txt'],
            help="File CSV chứa lịch sử giao dịch"
        )
        
        if uploaded_file:
            try:
                with st.spinner("Đang đọc file..."):
                    trades_df = data_loader.load_from_file(uploaded_file)
                    if trades_df is not None and len(trades_df) > 0:
                        st.session_state.trade_data = trades_df
                        st.success(f"✅ Đã tải {len(trades_df)} giao dịch!")
                        logger.info(f"Loaded {len(trades_df)} trades from file")
                    else:
                        st.error("❌ Không thể đọc file!")
                        logger.warning("Failed to load file")
            except Exception as e:
                st.error(f"❌ Lỗi đọc file: {str(e)}")
                logger.error(f"File upload error: {str(e)}", exc_info=True)
    
    # Show data preview
    if st.session_state.trade_data is not None:
        st.subheader("👀 Xem trước dữ liệu")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Tổng giao dịch", len(st.session_state.trade_data))
        with col2:
            st.metric("Tổng symbols", st.session_state.trade_data['SYMBOL'].nunique())
        with col3:
            date_range = (st.session_state.trade_data['CLOSE TIME'].max() - 
                         st.session_state.trade_data['CLOSE TIME'].min()).days
            st.metric("Số ngày", date_range)
        with col4:
            total_pnl = st.session_state.trade_data['PROFIT'].sum()
            st.metric("Tổng P&L", f"${total_pnl:.2f}")
        
        with st.expander("📋 Xem chi tiết dữ liệu"):
            st.dataframe(st.session_state.trade_data.head(50), use_container_width=True)
        
        st.info("✅ Dữ liệu đã sẵn sàng. Xem phân tích tại **'📈 Dashboard'**")

# Tab 4: Dashboard
elif tab_selection == "📈 Dashboard":
    st.header("📈 Dashboard Tổng quan")
    
    if st.session_state.trade_data is None:
        st.warning("⚠️ Vui lòng tải **Dữ liệu giao dịch** trước!")
        st.stop()
    
    # Calculate metrics if not already done
    if st.session_state.metrics is None:
        with st.spinner("Đang tính toán metrics..."):
            calc = PerformanceMetrics(st.session_state.trade_data)
            st.session_state.metrics = calc.calculate_all_metrics()
    
    metrics = st.session_state.metrics
    
    # Display metrics cards
    st.markdown(create_metrics_cards(metrics), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 P&L Timeline")
        fig_pnl = plot_pnl_timeline(st.session_state.trade_data)
        st.plotly_chart(fig_pnl, use_container_width=True)
        
        st.subheader("🎯 Symbol Distribution")
        fig_symbols = plot_symbol_distribution(st.session_state.trade_data)
        st.plotly_chart(fig_symbols, use_container_width=True)
    
    with col2:
        st.subheader("📊 Win/Loss Distribution")
        fig_winloss = plot_win_loss_distribution(st.session_state.trade_data)
        st.plotly_chart(fig_winloss, use_container_width=True)
        
        st.subheader("📅 Daily P&L")
        fig_daily = plot_daily_pnl(st.session_state.trade_data)
        st.plotly_chart(fig_daily, use_container_width=True)

# Tab 5: Detailed Analysis
elif tab_selection == "🔍 Phân tích chi tiết":
    st.header("🔍 Phân tích Chi tiết")
    
    if st.session_state.trade_data is None:
        st.warning("⚠️ Vui lòng tải **Dữ liệu giao dịch** trước!")
        st.stop()
    
    if st.session_state.metrics is None:
        calc = PerformanceMetrics(st.session_state.trade_data)
        st.session_state.metrics = calc.calculate_all_metrics()
    
    # Trading hours heatmap
    st.subheader("🕐 Trading Hours Heatmap")
    fig_hours = plot_trading_hours_heatmap(st.session_state.trade_data)
    st.plotly_chart(fig_hours, use_container_width=True)
    
    # Holding time analysis
    st.subheader("⏱️ Holding Time Analysis")
    fig_holding = plot_holding_time_boxplot(st.session_state.trade_data)
    st.plotly_chart(fig_holding, use_container_width=True)
    
    # Detailed metrics table
    st.subheader("📋 Chi tiết Metrics")
    
    metrics = st.session_state.metrics
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 Performance")
        st.write(f"**Total P&L:** ${metrics['total_pnl']:.2f}")
        st.write(f"**Win Rate:** {metrics['win_rate']:.1f}%")
        st.write(f"**Profit Factor:** {metrics['profit_factor']:.2f}")
        st.write(f"**Max Drawdown:** {metrics['max_drawdown']:.2f}%")
        st.write(f"**Risk/Reward Ratio:** {metrics['risk_reward_ratio']:.2f}")
        
        st.markdown("### 📊 Trading Behavior")
        st.write(f"**Total Trades:** {metrics['total_trades']}")
        st.write(f"**Avg Trades/Day:** {metrics['avg_trades_per_day']:.1f}")
        st.write(f"**Avg Holding Time:** {metrics['avg_holding_hours']:.1f} hours")
        st.write(f"**Stop Loss Usage:** {metrics['stop_loss_usage']:.1f}%")
    
    with col2:
        st.markdown("### 📈 Win/Loss Analysis")
        st.write(f"**Winning Trades:** {metrics['winning_trades']}")
        st.write(f"**Losing Trades:** {metrics['losing_trades']}")
        st.write(f"**Avg Win:** ${metrics['avg_win']:.2f}")
        st.write(f"**Avg Loss:** ${metrics['avg_loss']:.2f}")
        st.write(f"**Best Trade:** ${metrics['best_trade']:.2f}")
        st.write(f"**Worst Trade:** ${metrics['worst_trade']:.2f}")
        
        st.markdown("### 🎯 Top Symbols")
        for symbol, data in list(metrics['symbol_analysis'].items())[:5]:
            st.write(f"**{symbol}:** {data['count']} trades, ${data['pnl']:.2f}")

# Tab 6: Classification
elif tab_selection == "🎯 Phân loại":
    st.header("🎯 Phân loại Trader Type")
    
    if not st.session_state.profile_data or st.session_state.trade_data is None:
        st.warning("⚠️ Vui lòng hoàn thành **Hồ sơ** và **Dữ liệu giao dịch** trước!")
        st.stop()
    
    # Calculate classification if not done
    if st.session_state.classification is None:
        with st.spinner("Đang phân tích và phân loại..."):
            # Calculate metrics first
            if st.session_state.metrics is None:
                calc = PerformanceMetrics(st.session_state.trade_data)
                st.session_state.metrics = calc.calculate_all_metrics()
            
            # Classify
            classifier = TraderClassifier()
            st.session_state.classification = classifier.classify_trader_type(
                st.session_state.profile_data,
                st.session_state.metrics
            )
    
    classification = st.session_state.classification
    
    # Display classification result
    st.success(f"### Bạn là: **{classification['trader_type']}**")
    st.progress(classification['confidence_score'] / 100)
    st.caption(f"Độ tin cậy: {classification['confidence_score']:.1f}%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Đặc điểm")
        st.write(f"**Trading Style:** {classification['trading_style']}")
        st.write(f"**Risk Level:** {classification['risk_level']}")
        st.write(f"**Preferred Assets:** {', '.join(classification['preferred_assets'][:3])}")
        
        if classification['psychological_biases']:
            st.subheader("⚠️ Biases tâm lý phát hiện")
            for bias in classification['psychological_biases']:
                st.warning(f"• {bias}")
    
    with col2:
        st.subheader("💡 Giải thích")
        st.info(classification['explanation'])
    
    # Radar chart
    st.subheader("🕸️ Profile Radar Chart")
    
    # Extract profile features for radar chart
    user_profile = UserProfile()
    profile_features = user_profile.calculate_profile_features(st.session_state.profile_data)
    
    fig_radar = plot_trader_profile_radar(profile_features, st.session_state.metrics)
    st.plotly_chart(fig_radar, use_container_width=True)

# Tab 7: Advisory
elif tab_selection == "💡 Tư vấn":
    st.header("💡 Tư vấn Cá nhân hóa")
    
    if st.session_state.classification is None:
        st.warning("⚠️ Vui lòng hoàn thành phần **Phân loại** trước!")
        st.stop()
    
    # Generate advisory if not done
    if st.session_state.advisory is None:
        with st.spinner("Đang tạo tư vấn cá nhân hóa..."):
            advisor = TradingAdvisor()
            st.session_state.advisory = advisor.generate_full_report(
                st.session_state.classification['trader_type'],
                st.session_state.metrics
            )
    
    advisory = st.session_state.advisory
    
    # Display trader type
    st.info(f"### Trader Type: **{advisory['trader_type']}**")
    
    # Strengths
    st.subheader("💪 Điểm mạnh")
    for strength in advisory['strengths']:
        st.success(f"✅ {strength}")
    
    st.markdown("---")
    
    # Weaknesses
    st.subheader("⚠️ Điểm yếu")
    for weakness in advisory['weaknesses']:
        st.warning(f"⚠️ {weakness}")
    
    st.markdown("---")
    
    # Recommendations
    st.subheader("🎯 Khuyến nghị")
    for rec in advisory['recommendations']:
        st.info(f"{rec}")
    
    st.markdown("---")
    
    # Risk warnings
    st.subheader("🚨 Cảnh báo rủi ro")
    for warning in advisory['risk_warnings']:
        st.error(f"{warning}")
    
    st.markdown("---")
    
    # Summary
    st.subheader("📝 Tóm tắt")
    st.markdown(advisory['summary'])
    
    st.markdown("---")
    
    # Export report button
    st.subheader("📄 Xuất báo cáo")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("Tải xuống báo cáo đầy đủ dưới dạng PDF để lưu trữ hoặc chia sẻ.")
    
    with col2:
        if st.button("📥 Xuất báo cáo PDF", type="primary", use_container_width=True):
            try:
                with st.spinner("Đang tạo báo cáo PDF và biểu đồ..."):
                    # Generate charts for PDF
                    charts = []
                    try:
                        # P&L Timeline
                        fig_pnl = plot_pnl_timeline(st.session_state.trade_data)
                        charts.append(fig_pnl)
                        
                        # Win/Loss Distribution
                        fig_winloss = plot_win_loss_distribution(st.session_state.trade_data)
                        charts.append(fig_winloss)
                        
                        # Symbol Distribution
                        fig_symbols = plot_symbol_distribution(st.session_state.trade_data)
                        charts.append(fig_symbols)
                        
                        # Trading Hours Heatmap
                        fig_hours = plot_trading_hours_heatmap(st.session_state.trade_data)
                        charts.append(fig_hours)
                    except Exception as chart_err:
                        logger.warning(f"Chart generation warning: {chart_err}")
                        charts = None
                    
                    # Generate PDF with charts
                    pdf_generator = PDFReportGenerator()
                    pdf_data = pdf_generator.generate_report(
                        profile_data=st.session_state.profile_data,
                        classification=st.session_state.classification,
                        metrics=st.session_state.metrics,
                        advisory=st.session_state.advisory,
                        charts=charts
                    )
                    
                    # Generate filename
                    filename = pdf_generator.generate_filename(st.session_state.profile_data)
                    
                    # Provide download button
                    st.download_button(
                        label="⬇️ Tải xuống PDF (có biểu đồ)",
                        data=pdf_data,
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    chart_count = len(charts) if charts else 0
                    st.success(f"✅ Báo cáo PDF đã được tạo thành công ({chart_count} biểu đồ)!")
                    
            except Exception as e:
                st.error(f"❌ Lỗi khi tạo báo cáo PDF: {str(e)}")
                logger.error(f"PDF generation error: {str(e)}", exc_info=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📖 Về ứng dụng
**Trading Advisor AI** v1.0

Phát triển bởi SharkMe AI
Dựa trên nghiên cứu về hành vi giao dịch

[📚 Tài liệu](https://github.com) | [💬 Hỗ trợ](mailto:support@example.com)
""")

# Debug info (optional)
if st.sidebar.checkbox("🐛 Debug Mode"):
    st.sidebar.json({
        "profile_loaded": st.session_state.profile_data is not None,
        "data_loaded": st.session_state.trade_data is not None,
        "metrics_calculated": st.session_state.metrics is not None,
        "classified": st.session_state.classification is not None,
        "advisory_generated": st.session_state.advisory is not None
    })
