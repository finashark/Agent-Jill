"""
Module phân tích hành vi giao dịch dựa trên nghiên cứu
Phân loại trader thành 5 nhóm chính:
1. Newbie Gambler - Nhà giao dịch mới, vốn nhỏ, ưa mạo hiểm  
2. Technical Trader - Nhà giao dịch lướt sóng kỹ thuật kỷ luật
3. Long-term Investor - Nhà đầu tư dài hạn thận trọng
4. Part-time Trader - Nhà giao dịch bán thời gian thực dụng
5. Asset Specialist - Nhà giao dịch chuyên tập trung một loại tài sản
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class TradingBehaviorAnalyzer:
    def __init__(self):
        self.trader_profiles = {
            "Newbie Gambler": {
                "name": "Nhà giao dịch mới, vốn nhỏ, ưa mạo hiểm",
                "characteristics": [
                    "Vốn nhỏ (< $5,000)",
                    "Kinh nghiệm ít (< 1 năm)",
                    "Tần suất giao dịch cao",
                    "Thích scalping, day trading",
                    "Dùng đòn bẩy cao",
                    "Win rate thấp",
                    "Ưa thích crypto, sản phẩm biến động mạnh"
                ],
                "risks": [
                    "Nguy cơ cháy tài khoản cao",
                    "Thiếu kỷ luật quản lý rủi ro",
                    "Dễ bị cảm xúc chi phối",
                    "Giao dịch như đánh bạc"
                ],
                "advice": [
                    "Giáo dục cơ bản về quản lý vốn",
                    "Hạn chế đòn bẩy",
                    "Đặt strict stop loss",
                    "Bắt đầu với demo account"
                ]
            },
            "Technical Trader": {
                "name": "Nhà giao dịch lướt sóng kỹ thuật kỷ luật",
                "characteristics": [
                    "Kinh nghiệm 1-3 năm",
                    "Vốn trung bình ($5K-$100K)",
                    "Có hệ thống giao dịch",
                    "Sử dụng phân tích kỹ thuật",
                    "Day/swing trading có kỷ luật",
                    "Win rate vừa phải (45-60%)",
                    "Profit factor > 1"
                ],
                "risks": [
                    "Quá tự tin vào hệ thống",
                    "Stress từ giao dịch thường xuyên",
                    "Có thể mất kỷ luật khi thua dài"
                ],
                "advice": [
                    "Cung cấp phân tích kỹ thuật chất lượng",
                    "Hỗ trợ công cụ nâng cao",
                    "Nhắc nhở quản lý cảm xúc",
                    "Đề xuất diversification"
                ]
            },
            "Long-term Investor": {
                "name": "Nhà đầu tư dài hạn thận trọng",
                "characteristics": [
                    "Vốn lớn (> $100K)",
                    "Mục tiêu dài hạn",
                    "Ít giao dịch, giữ lâu",
                    "Đa dạng hóa tốt",
                    "Quan tâm phân tích cơ bản",
                    "Sử dụng đòn bẩy thấp",
                    "Ưa thích forex major, vàng"
                ],
                "risks": [
                    "Có thể hoảng sợ trong biến động lớn",
                    "Chi phí swap cao khi giữ lâu",
                    "Bỏ lỡ cơ hội ngắn hạn"
                ],
                "advice": [
                    "Cung cấp phân tích vĩ mô",
                    "Báo cáo định kỳ danh mục",
                    "Tư vấn tái cân bằng",
                    "Trấn an trong biến động"
                ]
            },
            "Part-time Trader": {
                "name": "Nhà giao dịch bán thời gian thực dụng",
                "characteristics": [
                    "Có công việc chính khác",
                    "Thời gian trading hạn chế",
                    "Mục tiêu thu nhập phụ",
                    "Swing trading, position trading",
                    "Thực dụng, linh hoạt",
                    "Không theo sát thị trường liên tục"
                ],
                "risks": [
                    "Bỏ lỡ cơ hội do bận việc",
                    "Khó quản lý rủi ro real-time",
                    "Cảm xúc công việc ảnh hưởng trading"
                ],
                "advice": [
                    "Cung cấp tín hiệu giao dịch đơn giản",
                    "Hỗ trợ công cụ tự động",
                    "Báo cáo thị trường cuối ngày",
                    "Cảnh báo qua SMS/email"
                ]
            },
            "Asset Specialist": {
                "name": "Nhà giao dịch chuyên tập trung một loại tài sản",
                "characteristics": [
                    "Chuyên sâu về một thị trường",
                    "Hiểu rõ đặc thù sản phẩm",
                    "Có thể bất kỳ phong cách nào",
                    "Tập trung cao",
                    "Kiến thức chuyên môn sâu",
                    "Ví dụ: Forex specialist, Gold specialist, Crypto specialist"
                ],
                "risks": [
                    "Thiếu đa dạng hóa",
                    "Rủi ro tập trung cao",
                    "Có thể bỏ qua cơ hội thị trường khác"
                ],
                "advice": [
                    "Cung cấp phân tích chuyên sâu",
                    "Kết nối với chuyên gia cùng lĩnh vực",
                    "Đề xuất nhẹ về diversification",
                    "Thông tin độc quyền về thị trường chuyên môn"
                ]
            }
        }
    
    def analyze_trading_behavior(self, df, customer_info=None):
        """
        Phân tích hành vi giao dịch và phân loại trader
        
        Args:
            df: DataFrame chứa dữ liệu giao dịch đã được xử lý
            customer_info: Dict chứa thông tin khách hàng từ AM
        
        Returns:
            dict: Kết quả phân tích bao gồm trader type, scores, insights
        """
        if df is None or len(df) == 0:
            return None
            
        # Tính toán các metrics cơ bản
        metrics = self._calculate_basic_metrics(df)
        
        # Phân tích đặc điểm hành vi
        behavior_analysis = self._analyze_behavior_patterns(df, metrics)
        
        # Tính điểm cho từng profile
        profile_scores = self._calculate_profile_scores(metrics, behavior_analysis, customer_info)
        
        # Xác định trader type chính
        primary_trader_type = max(profile_scores, key=profile_scores.get)
        
        # Tạo insights và khuyến nghị
        insights = self._generate_insights(primary_trader_type, metrics, behavior_analysis, customer_info)
        
        return {
            "primary_trader_type": primary_trader_type,
            "profile_scores": profile_scores,
            "metrics": metrics,
            "behavior_analysis": behavior_analysis,
            "insights": insights,
            "trader_profile": self.trader_profiles[primary_trader_type]
        }
    
    def _calculate_basic_metrics(self, df):
        """Tính toán các metrics cơ bản từ dữ liệu giao dịch"""
        total_trades = len(df)
        
        # Net PnL metrics
        net_pnl = df['Net_PnL'].sum()
        gross_profit = df['PROFIT'].sum()
        total_commission = df['COMM'].sum()
        total_swap = df['SWAP'].sum()
        
        # Win/Loss metrics
        win_trades = len(df[df['Result'] == 'WIN'])
        loss_trades = len(df[df['Result'] == 'LOSS'])
        be_trades = len(df[df['Result'] == 'BE'])
        win_rate = win_trades / total_trades if total_trades > 0 else 0
        
        # Profit factor
        winning_pnl = df[df['Net_PnL'] > 0]['Net_PnL'].sum()
        losing_pnl = abs(df[df['Net_PnL'] < 0]['Net_PnL'].sum())
        profit_factor = winning_pnl / losing_pnl if losing_pnl > 0 else float('inf')
        
        # Volume metrics
        total_lots = df['LOTS'].sum()
        avg_lot_size = df['LOTS'].mean()
        
        # Holding time metrics
        avg_holding_hours = df['Holding_Hours'].mean()
        median_holding_hours = df['Holding_Hours'].median()
        
        # Trading frequency (trades per day)
        if 'CLOSE_TIME' in df.columns and len(df) > 1:
            date_range = (df['CLOSE_TIME'].max() - df['CLOSE_TIME'].min()).days
            trades_per_day = total_trades / max(date_range, 1)
        else:
            trades_per_day = 0
        
        return {
            'total_trades': total_trades,
            'net_pnl': net_pnl,
            'gross_profit': gross_profit,
            'total_commission': total_commission,
            'total_swap': total_swap,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'total_lots': total_lots,
            'avg_lot_size': avg_lot_size,
            'avg_holding_hours': avg_holding_hours,
            'median_holding_hours': median_holding_hours,
            'trades_per_day': trades_per_day,
            'win_trades': win_trades,
            'loss_trades': loss_trades,
            'be_trades': be_trades
        }
    
    def _analyze_behavior_patterns(self, df, metrics):
        """Phân tích các pattern hành vi cụ thể"""
        
        # Phân tích holding time patterns
        holding_distribution = self._analyze_holding_time_distribution(df)
        
        # Phân tích asset preference
        asset_preference = self._analyze_asset_preference(df)
        
        # Phân tích trading session preference
        session_preference = self._analyze_session_preference(df)
        
        # Phân tích risk appetite
        risk_appetite = self._analyze_risk_appetite(df, metrics)
        
        # Phân tích consistency
        consistency = self._analyze_consistency(df)
        
        return {
            'holding_distribution': holding_distribution,
            'asset_preference': asset_preference,
            'session_preference': session_preference,
            'risk_appetite': risk_appetite,
            'consistency': consistency
        }
    
    def _analyze_holding_time_distribution(self, df):
        """Phân tích phân bổ thời gian nắm giữ"""
        if 'Holding_Hours' not in df.columns:
            return {}
            
        # Phân loại theo thời gian nắm giữ
        scalp = len(df[df['Holding_Hours'] < 1])  # < 1 giờ
        intraday = len(df[(df['Holding_Hours'] >= 1) & (df['Holding_Hours'] <= 8)])  # 1-8 giờ
        swing_short = len(df[(df['Holding_Hours'] > 8) & (df['Holding_Hours'] <= 168)])  # 8h - 7 ngày
        position = len(df[df['Holding_Hours'] > 168])  # > 7 ngày
        
        total = len(df)
        
        return {
            'scalp_pct': scalp / total * 100 if total > 0 else 0,
            'intraday_pct': intraday / total * 100 if total > 0 else 0,
            'swing_short_pct': swing_short / total * 100 if total > 0 else 0,
            'position_pct': position / total * 100 if total > 0 else 0,
            'scalp_count': scalp,
            'intraday_count': intraday,
            'swing_short_count': swing_short,
            'position_count': position
        }
    
    def _analyze_asset_preference(self, df):
        """Phân tích sở thích tài sản"""
        if 'Asset_Class' not in df.columns:
            return {}
            
        asset_counts = df['Asset_Class'].value_counts()
        total = len(df)
        
        asset_pcts = {}
        for asset, count in asset_counts.items():
            asset_pcts[f"{asset.lower()}_pct"] = count / total * 100
            asset_pcts[f"{asset.lower()}_count"] = count
        
        # Xác định asset chính (>50%)
        dominant_asset = None
        for asset, count in asset_counts.items():
            if count / total > 0.5:
                dominant_asset = asset
                break
        
        asset_pcts['dominant_asset'] = dominant_asset
        asset_pcts['diversification_level'] = len(asset_counts)
        
        return asset_pcts
    
    def _analyze_session_preference(self, df):
        """Phân tích sở thích phiên giao dịch"""
        if 'Session' not in df.columns:
            return {}
            
        session_counts = df['Session'].value_counts()
        total = len(df)
        
        return {
            'asia_pct': session_counts.get('Asia', 0) / total * 100,
            'london_pct': session_counts.get('London', 0) / total * 100,
            'ny_pct': session_counts.get('New York', 0) / total * 100,
            'preferred_session': session_counts.index[0] if len(session_counts) > 0 else None
        }
    
    def _analyze_risk_appetite(self, df, metrics):
        """Phân tích khẩu vị rủi ro"""
        # Đánh giá dựa trên nhiều yếu tố
        risk_score = 0
        risk_factors = []
        
        # Factor 1: Lot size (đòn bẩy)
        avg_lot = metrics['avg_lot_size']
        if avg_lot > 1.0:
            risk_score += 2
            risk_factors.append("Khối lượng giao dịch lớn")
        elif avg_lot > 0.5:
            risk_score += 1
            risk_factors.append("Khối lượng giao dịch trung bình")
        
        # Factor 2: Win rate vs Profit factor (risk/reward)
        if metrics['win_rate'] < 0.45 and metrics['profit_factor'] < 1:
            risk_score += 2
            risk_factors.append("Win rate thấp với profit factor kém")
        elif metrics['win_rate'] < 0.45:
            risk_score += 1
            risk_factors.append("Win rate thấp")
        
        # Factor 3: Trading frequency
        if metrics['trades_per_day'] > 10:
            risk_score += 2
            risk_factors.append("Tần suất giao dịch rất cao")
        elif metrics['trades_per_day'] > 3:
            risk_score += 1
            risk_factors.append("Tần suất giao dịch cao")
        
        # Factor 4: Asset concentration
        if 'asset_preference' in df.columns:
            crypto_pct = df[df['Asset_Class'] == 'Crypto'].shape[0] / len(df) * 100
            if crypto_pct > 50:
                risk_score += 1
                risk_factors.append("Tập trung nhiều vào Crypto")
        
        # Phân loại rủi ro
        if risk_score >= 5:
            risk_level = "CAO"
        elif risk_score >= 3:
            risk_level = "TRUNG BÌNH"
        else:
            risk_level = "THẤP"
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_factors': risk_factors
        }
    
    def _analyze_consistency(self, df):
        """Phân tích tính nhất quán trong giao dịch"""
        if len(df) < 10:
            return {'consistency_score': 0, 'consistency_level': 'INSUFFICIENT_DATA'}
        
        # Phân tích độ nhất quán theo thời gian
        df_sorted = df.sort_values('CLOSE_TIME')
        
        # Chia thành các periods để so sánh
        n_periods = min(5, len(df) // 10)
        period_size = len(df) // n_periods
        
        period_metrics = []
        for i in range(n_periods):
            start_idx = i * period_size
            end_idx = (i + 1) * period_size if i < n_periods - 1 else len(df)
            period_df = df_sorted.iloc[start_idx:end_idx]
            
            if len(period_df) > 0:
                period_win_rate = len(period_df[period_df['Result'] == 'WIN']) / len(period_df)
                period_pnl = period_df['Net_PnL'].sum()
                period_metrics.append({
                    'win_rate': period_win_rate,
                    'pnl': period_pnl
                })
        
        if len(period_metrics) > 1:
            # Tính coefficient of variation
            win_rates = [p['win_rate'] for p in period_metrics]
            pnls = [p['pnl'] for p in period_metrics]
            
            win_rate_cv = np.std(win_rates) / np.mean(win_rates) if np.mean(win_rates) > 0 else float('inf')
            
            # Consistency score (thấp hơn = nhất quán hơn)
            consistency_score = min(100, win_rate_cv * 100)
            
            if consistency_score < 20:
                consistency_level = "CAO"
            elif consistency_score < 50:
                consistency_level = "TRUNG BÌNH"
            else:
                consistency_level = "THẤP"
        else:
            consistency_score = 0
            consistency_level = "INSUFFICIENT_DATA"
        
        return {
            'consistency_score': consistency_score,
            'consistency_level': consistency_level,
            'period_count': len(period_metrics)
        }
    
    def _calculate_profile_scores(self, metrics, behavior_analysis, customer_info):
        """Tính điểm cho từng trader profile"""
        scores = {}
        
        for profile_name in self.trader_profiles.keys():
            score = 0
            
            if profile_name == "Newbie Gambler":
                score = self._score_newbie_gambler(metrics, behavior_analysis, customer_info)
            elif profile_name == "Technical Trader":
                score = self._score_technical_trader(metrics, behavior_analysis, customer_info)
            elif profile_name == "Long-term Investor":
                score = self._score_longterm_investor(metrics, behavior_analysis, customer_info)
            elif profile_name == "Part-time Trader":
                score = self._score_parttime_trader(metrics, behavior_analysis, customer_info)
            elif profile_name == "Asset Specialist":
                score = self._score_asset_specialist(metrics, behavior_analysis, customer_info)
            
            scores[profile_name] = max(0, min(100, score))  # Giới hạn 0-100
        
        return scores
    
    def _score_newbie_gambler(self, metrics, behavior, customer_info):
        """Tính điểm cho Newbie Gambler profile"""
        score = 0
        
        # High frequency trading (scalping)
        if behavior['holding_distribution']['scalp_pct'] >= 60:
            score += 25
        elif behavior['holding_distribution']['scalp_pct'] >= 40:
            score += 15
        
        # Low win rate
        if metrics['win_rate'] < 0.4:
            score += 20
        elif metrics['win_rate'] < 0.5:
            score += 10
        
        # High trading frequency
        if metrics['trades_per_day'] > 10:
            score += 20
        elif metrics['trades_per_day'] > 5:
            score += 15
        
        # Poor profit factor
        if metrics['profit_factor'] < 0.8:
            score += 15
        elif metrics['profit_factor'] < 1.0:
            score += 10
        
        # High risk appetite
        if behavior['risk_appetite']['risk_level'] == "CAO":
            score += 15
        
        # Customer info factors
        if customer_info:
            # Low capital
            if customer_info.get('capital_level') == 'low':
                score += 10
            # Young age
            if customer_info.get('age', 0) < 25:
                score += 5
            # Limited experience
            if customer_info.get('experience_years', 0) < 1:
                score += 10
        
        return score
    
    def _score_technical_trader(self, metrics, behavior, customer_info):
        """Tính điểm cho Technical Trader profile"""
        score = 0
        
        # Moderate holding times (intraday/swing)
        intraday_swing = behavior['holding_distribution']['intraday_pct'] + behavior['holding_distribution']['swing_short_pct']
        if intraday_swing >= 60:
            score += 25
        elif intraday_swing >= 40:
            score += 15
        
        # Decent win rate
        if 0.45 <= metrics['win_rate'] <= 0.65:
            score += 20
        
        # Good profit factor
        if metrics['profit_factor'] >= 1.2:
            score += 20
        elif metrics['profit_factor'] >= 1.0:
            score += 15
        
        # Moderate trading frequency
        if 2 <= metrics['trades_per_day'] <= 8:
            score += 15
        
        # Consistency
        if behavior['consistency']['consistency_level'] in ["CAO", "TRUNG BÌNH"]:
            score += 15
        
        # Customer info factors
        if customer_info:
            # Medium capital
            if customer_info.get('capital_level') == 'medium':
                score += 10
            # Some experience
            if 1 <= customer_info.get('experience_years', 0) <= 3:
                score += 10
        
        return score
    
    def _score_longterm_investor(self, metrics, behavior, customer_info):
        """Tính điểm cho Long-term Investor profile"""
        score = 0
        
        # Long holding times (position trading)
        if behavior['holding_distribution']['position_pct'] >= 40:
            score += 30
        elif behavior['holding_distribution']['position_pct'] >= 20:
            score += 20
        
        # Good win rate
        if metrics['win_rate'] >= 0.55:
            score += 20
        
        # Excellent profit factor
        if metrics['profit_factor'] >= 1.5:
            score += 20
        elif metrics['profit_factor'] >= 1.3:
            score += 15
        
        # Low trading frequency
        if metrics['trades_per_day'] <= 1:
            score += 15
        elif metrics['trades_per_day'] <= 2:
            score += 10
        
        # Diversification
        if behavior['asset_preference']['diversification_level'] >= 3:
            score += 10
        
        # Customer info factors
        if customer_info:
            # High capital
            if customer_info.get('capital_level') == 'high':
                score += 15
            # Mature age
            if customer_info.get('age', 0) >= 40:
                score += 5
            # Conservative goals
            if customer_info.get('investment_goal') in ['wealth_preservation', 'long_term_growth']:
                score += 10
        
        return score
    
    def _score_parttime_trader(self, metrics, behavior, customer_info):
        """Tính điểm cho Part-time Trader profile"""
        score = 0
        
        # Moderate holding times
        swing_position = behavior['holding_distribution']['swing_short_pct'] + behavior['holding_distribution']['position_pct']
        if swing_position >= 50:
            score += 20
        
        # Moderate trading frequency
        if 1 <= metrics['trades_per_day'] <= 3:
            score += 20
        elif metrics['trades_per_day'] <= 5:
            score += 15
        
        # Practical performance
        if 0.45 <= metrics['win_rate'] <= 0.6:
            score += 15
        
        if 1.0 <= metrics['profit_factor'] <= 1.5:
            score += 15
        
        # Risk management
        if behavior['risk_appetite']['risk_level'] in ["THẤP", "TRUNG BÌNH"]:
            score += 15
        
        # Customer info factors
        if customer_info:
            # Has other occupation
            if customer_info.get('has_other_job', False):
                score += 20
            # Supplementary income goal
            if customer_info.get('investment_goal') == 'supplementary_income':
                score += 15
        
        return score
    
    def _score_asset_specialist(self, metrics, behavior, customer_info):
        """Tính điểm cho Asset Specialist profile"""
        score = 0
        
        # High concentration in one asset class
        if behavior['asset_preference']['dominant_asset']:
            score += 30
        
        # Low diversification
        if behavior['asset_preference']['diversification_level'] <= 2:
            score += 20
        
        # Can have various trading styles, so don't penalize specific patterns
        # Focus on specialization
        
        # Customer info factors
        if customer_info:
            # Professional background related to specific market
            if customer_info.get('has_market_expertise', False):
                score += 20
            # Strong preference for specific asset
            if customer_info.get('preferred_asset'):
                score += 15
        
        return score
    
    def _generate_insights(self, trader_type, metrics, behavior_analysis, customer_info):
        """Tạo insights và khuyến nghị dựa trên phân tích"""
        profile = self.trader_profiles[trader_type]
        
        insights = {
            "trader_type": trader_type,
            "trader_name": profile["name"],
            "confidence_score": 0,  # Sẽ tính dựa trên profile scores
            "key_characteristics": [],
            "risk_assessment": {},
            "recommendations": [],
            "trading_summary": "",
            "behavioral_insights": "",
            "risk_warnings": []
        }
        
        # Tạo trading summary
        insights["trading_summary"] = self._create_trading_summary(metrics, behavior_analysis)
        
        # Tạo behavioral insights
        insights["behavioral_insights"] = self._create_behavioral_insights(trader_type, behavior_analysis, customer_info)
        
        # Risk assessment
        insights["risk_assessment"] = behavior_analysis['risk_appetite']
        
        # Recommendations dựa trên trader type
        insights["recommendations"] = profile["advice"].copy()
        
        # Risk warnings
        insights["risk_warnings"] = profile["risks"].copy()
        
        # Key characteristics found
        insights["key_characteristics"] = self._identify_key_characteristics(trader_type, metrics, behavior_analysis)
        
        return insights
    
    def _create_trading_summary(self, metrics, behavior_analysis):
        """Tạo tóm tắt giao dịch"""
        summary_parts = []
        
        # Basic stats
        summary_parts.append(f"Tổng số lệnh: {metrics['total_trades']}")
        summary_parts.append(f"Tỷ lệ thắng: {metrics['win_rate']:.1%}")
        summary_parts.append(f"Profit Factor: {metrics['profit_factor']:.2f}")
        summary_parts.append(f"Net PnL: ${metrics['net_pnl']:.2f}")
        
        # Holding time preference
        holding_dist = behavior_analysis['holding_distribution']
        if holding_dist['scalp_pct'] > 50:
            summary_parts.append("Chủ yếu scalping (< 1 giờ)")
        elif holding_dist['intraday_pct'] > 40:
            summary_parts.append("Chủ yếu day trading (1-8 giờ)")
        elif holding_dist['swing_short_pct'] > 40:
            summary_parts.append("Chủ yếu swing trading (8h-7 ngày)")
        elif holding_dist['position_pct'] > 30:
            summary_parts.append("Có xu hướng position trading (>7 ngày)")
        
        # Risk level
        risk_level = behavior_analysis['risk_appetite']['risk_level']
        summary_parts.append(f"Mức độ rủi ro: {risk_level}")
        
        return " | ".join(summary_parts)
    
    def _create_behavioral_insights(self, trader_type, behavior_analysis, customer_info):
        """Tạo insights hành vi cụ thể"""
        insights = []
        
        # Asset preference insights
        asset_pref = behavior_analysis['asset_preference']
        if asset_pref.get('dominant_asset'):
            insights.append(f"Tập trung chủ yếu vào {asset_pref['dominant_asset']}")
        
        # Time distribution insights
        holding_dist = behavior_analysis['holding_distribution']
        if holding_dist['scalp_pct'] > 60:
            insights.append("Rất thích giao dịch ngắn hạn, có thể có xu hướng over-trading")
        
        # Risk appetite insights
        risk_factors = behavior_analysis['risk_appetite']['risk_factors']
        if risk_factors:
            insights.append(f"Các yếu tố rủi ro: {', '.join(risk_factors)}")
        
        # Consistency insights
        consistency = behavior_analysis['consistency']
        if consistency['consistency_level'] == "CAO":
            insights.append("Thể hiện tính nhất quán cao trong giao dịch")
        elif consistency['consistency_level'] == "THẤP":
            insights.append("Kết quả giao dịch thiếu ổn định, cần cải thiện kỷ luật")
        
        return " | ".join(insights) if insights else "Cần thêm dữ liệu để phân tích chi tiết"
    
    def _identify_key_characteristics(self, trader_type, metrics, behavior_analysis):
        """Xác định các đặc điểm key đã được tìm thấy"""
        characteristics = []
        
        # Common characteristics based on data
        if metrics['trades_per_day'] > 5:
            characteristics.append("Tần suất giao dịch cao")
        
        if metrics['win_rate'] < 0.45:
            characteristics.append("Tỷ lệ thắng thấp")
        elif metrics['win_rate'] > 0.6:
            characteristics.append("Tỷ lệ thắng tốt")
        
        if metrics['profit_factor'] > 1.3:
            characteristics.append("Profit factor khá tốt")
        elif metrics['profit_factor'] < 1.0:
            characteristics.append("Profit factor kém")
        
        # Holding time characteristics
        holding_dist = behavior_analysis['holding_distribution']
        if holding_dist['scalp_pct'] > 50:
            characteristics.append("Thích scalping")
        if holding_dist['position_pct'] > 30:
            characteristics.append("Có xu hướng nắm giữ dài hạn")
        
        # Risk characteristics
        risk_level = behavior_analysis['risk_appetite']['risk_level']
        if risk_level == "CAO":
            characteristics.append("Chấp nhận rủi ro cao")
        elif risk_level == "THẤP":
            characteristics.append("Thận trọng với rủi ro")
        
        return characteristics

# Export main class
__all__ = ['TradingBehaviorAnalyzer']