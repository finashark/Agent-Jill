"""
Test script for PDF generation
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from pdf_generator import PDFReportGenerator

def test_pdf_generation():
    """Test PDF generation with sample data"""
    
    # Sample data
    profile_data = {
        'name': 'Nguyen Van A',
        'age': 35,
        'gender': 'Nam',
        'education': 'Đại học',
        'income': '$50,000 - $100,000',
        'capital': 10000,
        'experience': '2-5 năm',
        'risk_tolerance': 7,
        'available_time': '2-4 giờ/ngày',
        'goals': 'Tăng thu nhập'
    }
    
    classification = {
        'trader_type': 'Aggressive Trader',
        'confidence_score': 0.85,
        'trading_style': 'Day Trading',
        'risk_level': 'High'
    }
    
    metrics = {
        'total_pnl': 5432.50,
        'win_rate': 65.5,
        'total_trades': 150,
        'winning_trades': 98,
        'losing_trades': 52,
        'avg_profit': 120.5,
        'avg_loss': -85.3,
        'max_drawdown': -1500.0,
        'risk_reward_ratio': 1.41,
        'profit_factor': 2.15
    }
    
    advisory = {
        'trader_type': 'Aggressive Trader',
        'strengths': [
            'Tỷ lệ thắng cao (65.5%), cho thấy khả năng phân tích tốt',
            'Risk/Reward ratio tích cực (1.41)',
            'Số lượng giao dịch đủ lớn để đánh giá'
        ],
        'weaknesses': [
            'Max drawdown cao (-$1,500), cần quản lý rủi ro tốt hơn',
            'Thiếu kiên nhẫn trong việc chờ đợi setup tốt',
            'Có xu hướng giao dịch quá nhiều trong một phiên'
        ],
        'recommendations': [
            'Giảm kích thước vị thế xuống 1-2% mỗi giao dịch để giảm rủi ro',
            'Thiết lập stop-loss cố định cho mọi giao dịch',
            'Tập trung vào 2-3 cặp tiền chính để hiểu rõ hơn về price action',
            'Ghi nhật ký giao dịch để phân tích và cải thiện chiến lược'
        ],
        'risk_warnings': [
            'Mức độ rủi ro cao - chỉ phù hợp với nhà đầu tư có kinh nghiệm',
            'Không sử dụng đòn bẩy quá cao (khuyến nghị tối đa 1:10)',
            'Luôn có kế hoạch quản lý vốn rõ ràng trước khi giao dịch'
        ],
        'summary': 'Bạn là một trader năng động với phong cách giao dịch tích cực. Điểm mạnh của bạn là tỷ lệ thắng tốt và khả năng đọc thị trường. Tuy nhiên, cần cải thiện quản lý rủi ro để giảm drawdown và bảo vệ vốn.'
    }
    
    # Generate PDF
    print("Generating PDF report...")
    pdf_generator = PDFReportGenerator()
    pdf_data = pdf_generator.generate_report(
        profile_data=profile_data,
        classification=classification,
        metrics=metrics,
        advisory=advisory
    )
    
    # Save to file
    filename = pdf_generator.generate_filename(profile_data)
    output_path = Path(__file__).parent / filename
    
    with open(output_path, 'wb') as f:
        f.write(pdf_data)
    
    print(f"✅ PDF generated successfully: {output_path}")
    print(f"File size: {len(pdf_data)} bytes")

if __name__ == "__main__":
    test_pdf_generation()
