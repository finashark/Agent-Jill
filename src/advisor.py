"""
Trading Advisor Module
Generates personalized advice based on trader classification
"""

from typing import Dict, Any, List

class TradingAdvisor:
    """Generate personalized trading advice"""
    
    def __init__(self):
        """Initialize advisor"""
        pass
        
    def get_strengths(self, trader_type: str, metrics: Dict[str, Any]) -> List[str]:
        """Identify trader's strengths"""
        strengths = []
        
        # Based on metrics
        if metrics.get('win_rate', 0) > 55:
            strengths.append(f"✅ Tỷ lệ thắng tốt ({metrics['win_rate']:.1f}%)")
        
        if metrics.get('risk_reward_ratio', 0) > 1.5:
            strengths.append(f"✅ Risk/Reward ratio tích cực ({metrics['risk_reward_ratio']:.2f})")
        
        sl_usage = metrics.get('stop_loss_usage', 0)
        if sl_usage > 70:
            strengths.append(f"✅ Kỷ luật đặt Stop Loss tốt ({sl_usage:.1f}%)")
        
        if metrics.get('max_drawdown', 100) < 15:
            strengths.append(f"✅ Kiểm soát drawdown tốt ({metrics['max_drawdown']:.1f}%)")
        
        if metrics.get('profit_factor', 0) > 1.5:
            strengths.append(f"✅ Profit Factor mạnh ({metrics['profit_factor']:.2f})")
        
        # Type-specific strengths
        type_strengths = {
            "Newbie Gambler": [
                "✅ Nhiệt huyết và sẵn sàng học hỏi",
                "✅ Năng động trong giao dịch"
            ],
            "Technical Day/Swing Trader": [
                "✅ Có hệ thống giao dịch rõ ràng",
                "✅ Hiểu biết về phân tích kỹ thuật",
                "✅ Kỷ luật trong quản lý rủi ro"
            ],
            "Long-term Value Investor": [
                "✅ Tầm nhìn dài hạn và kiên nhẫn",
                "✅ Đa dạng hóa danh mục",
                "✅ Quản lý rủi ro thận trọng"
            ],
            "Part-time Opportunist": [
                "✅ Cân bằng tốt giữa công việc và trading",
                "✅ Thực dụng và linh hoạt",
                "✅ Không để cảm xúc chi phối"
            ],
            "Asset Specialist Trader": [
                "✅ Hiểu sâu về thị trường chuyên môn",
                "✅ Tập trung cao độ",
                "✅ Kinh nghiệm chuyên sâu"
            ]
        }
        
        strengths.extend(type_strengths.get(trader_type, []))
        
        return strengths
    
    def get_weaknesses(self, trader_type: str, metrics: Dict[str, Any]) -> List[str]:
        """Identify areas for improvement"""
        weaknesses = []
        
        # Based on metrics
        if metrics.get('win_rate', 100) < 45:
            weaknesses.append(f"⚠️ Tỷ lệ thắng thấp ({metrics['win_rate']:.1f}%)")
        
        if metrics.get('risk_reward_ratio', 10) < 1:
            weaknesses.append(f"⚠️ Risk/Reward ratio kém ({metrics['risk_reward_ratio']:.2f})")
        
        sl_usage = metrics.get('stop_loss_usage', 100)
        if sl_usage < 50:
            weaknesses.append(f"⚠️ Kỷ luật đặt Stop Loss kém ({sl_usage:.1f}%)")
        
        if metrics.get('max_drawdown', 0) > 30:
            weaknesses.append(f"⚠️ Drawdown quá lớn ({metrics['max_drawdown']:.1f}%)")
        
        freq = metrics.get('avg_trades_per_day', 0)
        if freq > 20:
            weaknesses.append(f"⚠️ Giao dịch quá thường xuyên ({freq:.1f} lệnh/ngày)")
        
        # Type-specific weaknesses
        type_weaknesses = {
            "Newbie Gambler": [
                "⚠️ Thiếu kinh nghiệm và kiến thức",
                "⚠️ Dễ bị cảm xúc chi phối",
                "⚠️ Rủi ro quá mức"
            ],
            "Technical Day/Swing Trader": [
                "⚠️ Có thể quá tự tin vào hệ thống",
                "⚠️ Áp lực tâm lý khi giao dịch thường xuyên"
            ],
            "Asset Specialist Trader": [
                "⚠️ Thiếu đa dạng hóa (rủi ro tập trung)",
                "⚠️ Phụ thuộc quá nhiều vào một thị trường"
            ]
        }
        
        weaknesses.extend(type_weaknesses.get(trader_type, []))
        
        return weaknesses
    
    def get_recommendations(self, trader_type: str, metrics: Dict[str, Any]) -> List[str]:
        """Get actionable recommendations"""
        recommendations = []
        
        # Based on trader type
        type_recommendations = {
            "Newbie Gambler": [
                "📚 Tham gia các khóa học trading cơ bản",
                "📉 Giảm khối lượng giao dịch xuống 50%",
                "🛡️ Luôn đặt stop loss trước khi vào lệnh",
                "📊 Không nên rủi ro >2% mỗi lệnh",
                "📝 Ghi nhật ký giao dịch để rút kinh nghiệm",
                "💪 Sử dụng tài khoản demo để thực hành"
            ],
            "Technical Day/Swing Trader": [
                "📊 Tiếp tục backtest và tối ưu hóa chiến lược",
                "⏱️ Đặt giới hạn số lệnh mỗi ngày để tránh overtrading",
                "😌 Nghỉ ngơi sau chuỗi thua để tránh revenge trading",
                "🌐 Đa dạng hóa danh mục thêm để giảm rủi ro",
                "📰 Theo dõi tin tức kinh tế lớn để tránh biến động"
            ],
            "Long-term Value Investor": [
                "📈 Tiếp tục chiến lược dài hạn hiện tại",
                "🔄 Định kỳ rebalance danh mục mỗi quý",
                "📊 Theo dõi các chỉ số kinh tế vĩ mô",
                "💼 Xem xét thêm các kênh đầu tư an toàn",
                "📚 Cập nhật kiến thức về phân tích cơ bản"
            ],
            "Part-time Opportunist": [
                "⏰ Tối ưu hóa thời gian trading (focus vào quality)",
                "🤖 Xem xét sử dụng alerts và automation",
                "📱 Đặt cảnh báo giá để không bỏ lỡ cơ hội",
                "📊 Tập trung vào swing trading thay vì scalping",
                "📝 Lập kế hoạch trading trước mỗi tuần"
            ],
            "Asset Specialist Trader": [
                "🌐 Đa dạng hóa sang 2-3 tài sản khác",
                "📊 Theo dõi correlation giữa các thị trường",
                "🛡️ Sử dụng hedging để bảo vệ vị thế",
                "📚 Mở rộng kiến thức sang các thị trường liên quan",
                "💼 Phân bổ không quá 50% vốn vào một tài sản"
            ]
        }
        
        recommendations.extend(type_recommendations.get(trader_type, []))
        
        return recommendations
    
    def get_risk_warnings(self, trader_type: str, metrics: Dict[str, Any]) -> List[str]:
        """Get risk warnings"""
        warnings = []
        
        # Critical warnings based on metrics
        if metrics.get('max_drawdown', 0) > 30:
            warnings.append("🚨 NGUY CƠ CHÁY TÀI KHOẢN: Drawdown quá cao!")
        
        if metrics.get('win_rate', 50) < 40:
            warnings.append("🚨 Tỷ lệ thắng quá thấp - ngừng giao dịch và review chiến lược")
        
        freq = metrics.get('avg_trades_per_day', 0)
        if freq > 20:
            warnings.append("🚨 Overtrading nghiêm trọng - giảm số lệnh mỗi ngày")
        
        # Type-specific warnings
        type_warnings = {
            "Newbie Gambler": [
                "🚨 Nguy cơ cháy tài khoản cao do overtrading",
                "🚨 Dễ rơi vào bẫy tự tin thái quá sau vài lần thắng",
                "🚨 Tâm lý FOMO có thể dẫn đến quyết định sai"
            ],
            "Technical Day/Swing Trader": [
                "🚨 Thị trường bất thường có thể phá vỡ hệ thống kỹ thuật",
                "🚨 Cẩn thận với confirmation bias",
                "🚨 Nguy cơ burnout nếu trade quá nhiều"
            ],
            "Long-term Value Investor": [
                "🚨 Biến động lớn ngắn hạn có thể gây hoảng loạn",
                "🚨 Phí swap qua đêm có thể ăn mòn lợi nhuận",
                "🚨 Black swan events có thể gây thiệt hại lớn"
            ],
            "Part-time Opportunist": [
                "🚨 Bỏ lỡ tin tức quan trọng khi không theo dõi",
                "🚨 Gap price khi thị trường mở cửa",
                "🚨 Không thể phản ứng kịp với biến động đột ngột"
            ],
            "Asset Specialist Trader": [
                "🚨 Rủi ro tập trung cao nếu thị trường sụp đổ",
                "🚨 Correlation risk khi chỉ trade một loại",
                "🚨 Thiếu đa dạng hóa làm tăng volatility danh mục"
            ]
        }
        
        warnings.extend(type_warnings.get(trader_type, []))
        
        return warnings
    
    def generate_full_report(self, trader_type: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive advisory report"""
        return {
            'trader_type': trader_type,
            'strengths': self.get_strengths(trader_type, metrics),
            'weaknesses': self.get_weaknesses(trader_type, metrics),
            'recommendations': self.get_recommendations(trader_type, metrics),
            'risk_warnings': self.get_risk_warnings(trader_type, metrics),
            'summary': self._generate_summary(trader_type, metrics)
        }
    
    def _generate_summary(self, trader_type: str, metrics: Dict[str, Any]) -> str:
        """Generate executive summary"""
        win_rate = metrics.get('win_rate', 0)
        total_pnl = metrics.get('total_pnl', 0)
        
        summaries = {
            "Newbie Gambler": (
                f"Bạn là một trader mới bắt đầu với phong cách mạo hiểm. "
                f"Win rate hiện tại {win_rate:.1f}% và P&L ${total_pnl:.2f}. "
                f"Cần tập trung vào học hỏi và quản lý rủi ro trước khi tăng khối lượng giao dịch."
            ),
            "Technical Day/Swing Trader": (
                f"Bạn là trader có kinh nghiệm với phong cách kỹ thuật. "
                f"Win rate {win_rate:.1f}% cho thấy bạn đang trên đúng hướng. "
                f"Tiếp tục tối ưu hóa hệ thống và duy trì kỷ luật."
            ),
            "Long-term Value Investor": (
                f"Bạn là nhà đầu tư dài hạn với tầm nhìn xa. "
                f"Phong cách thận trọng phù hợp với mục tiêu bảo toàn và tăng trưởng bền vững. "
                f"Tiếp tục duy trì chiến lược hiện tại."
            ),
            "Part-time Opportunist": (
                f"Bạn cân bằng tốt giữa công việc và trading. "
                f"Win rate {win_rate:.1f}% là hợp lý cho trader bán thời gian. "
                f"Tối ưu hóa thời gian và công cụ để tăng hiệu quả."
            ),
            "Asset Specialist Trader": (
                f"Bạn chuyên sâu vào một loại tài sản cụ thể. "
                f"Kiến thức chuyên môn là điểm mạnh, nhưng cần đa dạng hóa để giảm rủi ro. "
                f"Xem xét mở rộng sang 2-3 thị trường liên quan."
            )
        }
        
        return summaries.get(trader_type, "Không có thông tin tóm tắt")
