"""
Trader Classifier Module
Classifies traders based on profile and trading behavior
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple

class TraderClassifier:
    """Classify trader based on form data + trading behavior"""
    
    def __init__(self):
        """Initialize classifier"""
        self.profile = None
        self.trades_df = None
        self.metrics = None
        self.classification = {}
        self.confidence_score = 0.0
        
    def determine_trading_style(self) -> str:
        """Identify trading style from behavior"""
        avg_holding = self.metrics.get('avg_holding_minutes', 0)
        
        if avg_holding < 60:
            return "Scalping"
        elif avg_holding < 480:  # 8 hours
            return "Day Trading"
        elif avg_holding < 10080:  # 1 week
            return "Swing Trading"
        else:
            return "Position Trading"
    
    def assess_risk_level(self) -> str:
        """Assess risk level from trading data"""
        win_rate = self.metrics.get('win_rate', 50)
        avg_loss = abs(self.metrics.get('avg_loss', 0))
        max_dd = self.metrics.get('max_drawdown', 0)
        sl_usage = self.metrics.get('stop_loss_usage', 0)
        
        risk_score = 0
        
        # Low win rate
        if win_rate < 40:
            risk_score += 3
        elif win_rate < 50:
            risk_score += 1
        
        # Large average loss
        if avg_loss > 10:
            risk_score += 2
        elif avg_loss > 5:
            risk_score += 1
        
        # High drawdown
        if max_dd > 30:
            risk_score += 3
        elif max_dd > 15:
            risk_score += 1
        
        # Low SL usage
        if sl_usage < 50:
            risk_score += 2
        elif sl_usage < 70:
            risk_score += 1
        
        if risk_score >= 7:
            return "Very High"
        elif risk_score >= 5:
            return "High"
        elif risk_score >= 3:
            return "Moderate"
        else:
            return "Low"
    
    def find_preferred_assets(self) -> list:
        """Find most traded symbols from metrics"""
        if not self.metrics or 'symbol_analysis' not in self.metrics:
            return ["N/A"]
        
        symbol_analysis = self.metrics.get('symbol_analysis', {})
        if not symbol_analysis:
            return ["N/A"]
        
        # Sort by trade count
        sorted_symbols = sorted(
            symbol_analysis.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )
        
        # Get top 3 symbols
        top_symbols = []
        for symbol, data in sorted_symbols[:3]:
            # Categorize asset type
            if 'XAU' in symbol:
                asset_type = "Gold"
            elif any(x in symbol for x in ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'NZD']):
                asset_type = "Forex"
            elif any(x in symbol for x in ['BTC', 'ETH']):
                asset_type = "Crypto"
            else:
                asset_type = "Other"
            
            top_symbols.append(f"{symbol} ({asset_type})")
        
        return top_symbols if top_symbols else ["N/A"]
    
    def detect_psychological_biases(self) -> list:
        """Detect psychological biases from trading patterns"""
        biases = []
        
        # Overconfidence: too many trades
        freq = self.metrics.get('avg_trades_per_day', 0)
        if freq > 20:
            biases.append("Overtrading")
        
        # Loss aversion: win rate too low with frequent trading
        win_rate = self.metrics.get('win_rate', 50)
        if win_rate < 40 and freq > 10:
            biases.append("Poor discipline")
        
        # Revenge trading: many small losses in sequence
        if self.metrics.get('losing_trades', 0) > self.metrics.get('winning_trades', 0):
            biases.append("Loss aversion")
        
        # Poor discipline: low SL usage
        sl_rate = self.metrics.get('stop_loss_usage', 0)
        if sl_rate < 50:
            biases.append("Poor risk management")
        
        # Risk-seeking: high drawdown
        max_dd = self.metrics.get('max_drawdown', 0)
        if max_dd > 20:
            biases.append("Excessive risk-taking")
        
        return biases
    
    def classify_trader_type(self, user_profile: Dict[str, Any], metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify into 5 main types with confidence score
        
        Args:
            user_profile: User profile data from form
            metrics: Calculated trading metrics
            
        Returns:
            Dict with classification results
        """
        # Store for use in other methods
        from user_profile import UserProfile
        profile_obj = UserProfile()
        self.profile = profile_obj.calculate_profile_features(user_profile)
        self.metrics = metrics
        # Weighted scoring: Profile 40% + Behavior 60%
        
        # Profile scores (0-10 scale)
        profile_score = {
            'capital': 0,
            'experience': 0,
            'goals': 0,
            'demographics': 0
        }
        
        # Capital score
        if self.profile['capital_level'] == 'Small':
            profile_score['capital'] = 3
        elif self.profile['capital_level'] == 'Medium':
            profile_score['capital'] = 6
        else:
            profile_score['capital'] = 9
        
        # Experience score
        exp_map = {'Newbie': 2, 'Beginner': 4, 'Intermediate': 7, 'Experienced': 10}
        profile_score['experience'] = exp_map.get(self.profile['experience_level'], 5)
        
        # Goals analysis
        goals = self.profile.get('goals', [])
        if 'Giải trí' in goals or 'Tăng trưởng vốn nhanh' in goals:
            profile_score['goals'] = 3  # Speculative
        elif 'Bảo toàn tài sản' in goals:
            profile_score['goals'] = 9  # Conservative
        else:
            profile_score['goals'] = 6  # Balanced
        
        # Demographics (age + education)
        age_score = {'Young': 3, 'Young-Adult': 5, 'Middle-Aged': 7, 'Senior': 9}
        profile_score['demographics'] = (
            age_score.get(self.profile['age_group'], 5) + 
            self.profile['education_level']
        ) / 2
        
        # Behavior scores (0-10 scale)
        behavior_score = {
            'style': 0,
            'performance': 0,
            'discipline': 0,
            'risk': 0
        }
        
        # Style score
        style = self.determine_trading_style()
        style_map = {'Scalping': 2, 'Day Trading': 4, 'Swing Trading': 7, 'Position Trading': 10}
        behavior_score['style'] = style_map.get(style, 5)
        
        # Performance score
        win_rate = self.metrics.get('win_rate', 50)
        if win_rate < 45:
            behavior_score['performance'] = 3
        elif win_rate < 55:
            behavior_score['performance'] = 6
        else:
            behavior_score['performance'] = 9
        
        # Discipline score (based on SL usage and consistency)
        sl_usage = self.metrics.get('stop_loss_usage', 0)
        behavior_score['discipline'] = min(sl_usage / 10, 10)
        
        # Risk score
        risk_level = self.assess_risk_level()
        risk_map = {'Low': 9, 'Moderate': 6, 'High': 3, 'Very High': 1}
        behavior_score['risk'] = risk_map.get(risk_level, 5)
        
        # Calculate weighted final score (0-100)
        profile_avg = sum(profile_score.values()) / len(profile_score) * 4  # 40%
        behavior_avg = sum(behavior_score.values()) / len(behavior_score) * 6  # 60%
        final_score = profile_avg + behavior_avg
        
        # Classify based on combined factors
        trader_type = self._determine_type_from_scores(
            profile_score, behavior_score, final_score
        )
        
        # Calculate confidence (how well profile and behavior align)
        profile_tendency = profile_avg / 4  # Normalize to 0-10
        behavior_tendency = behavior_avg / 6  # Normalize to 0-10
        alignment = 1 - abs(profile_tendency - behavior_tendency) / 10
        confidence = alignment * 100
        
        # Return full classification result
        return {
            'trader_type': trader_type,
            'confidence_score': round(confidence, 2),
            'trading_style': self.determine_trading_style(),
            'risk_level': self.assess_risk_level(),
            'preferred_assets': self.find_preferred_assets(),
            'psychological_biases': self.detect_psychological_biases(),
            'explanation': self.get_classification_explanation(trader_type)
        }
    
    def _determine_type_from_scores(
        self, 
        profile_score: Dict, 
        behavior_score: Dict, 
        final_score: float
    ) -> str:
        """Determine trader type from scores"""
        
        # Newbie Gambler: Low capital, low experience, high risk, poor performance
        if (profile_score['capital'] <= 4 and 
            profile_score['experience'] <= 4 and
            behavior_score['risk'] <= 4 and
            behavior_score['discipline'] <= 4):
            return "Newbie Gambler"
        
        # Long-term Investor: High capital, conservative goals, long holding
        if (profile_score['capital'] >= 7 and
            profile_score['goals'] >= 7 and
            behavior_score['style'] >= 8 and
            behavior_score['risk'] >= 7):
            return "Long-term Value Investor"
        
        # Technical Trader: Medium-high experience, day/swing style, good discipline
        if (profile_score['experience'] >= 6 and
            4 <= behavior_score['style'] <= 7 and
            behavior_score['discipline'] >= 6 and
            behavior_score['performance'] >= 6):
            return "Technical Day/Swing Trader"
        
        # Part-time: Medium capital, limited time, moderate activity
        time_commitment = self.profile.get('time_commitment', 'Low')
        if time_commitment in ['Low', 'Very Low'] and final_score >= 40:
            return "Part-time Opportunist"
        
        # Asset Specialist: Check symbol concentration from metrics
        if self.metrics and 'symbol_analysis' in self.metrics:
            symbols = self.metrics['symbol_analysis']
            if symbols and isinstance(symbols, dict):
                # Calculate concentration of top symbol
                symbol_counts = [data.get('count', 0) for data in symbols.values() if isinstance(data, dict)]
                if symbol_counts:
                    total_trades = sum(symbol_counts)
                    top_symbol_count = max(symbol_counts)
                    concentration = (top_symbol_count / total_trades * 100) if total_trades > 0 else 0
                    
                    if concentration > 70:
                        return "Asset Specialist Trader"
        
        # Default based on final score
        if final_score < 40:
            return "Newbie Gambler"
        elif final_score < 60:
            return "Part-time Opportunist"
        else:
            return "Technical Day/Swing Trader"
    
    def get_classification_explanation(self, trader_type: str) -> str:
        """Explain classification reasoning"""
        explanations = {
            "Newbie Gambler": (
                "Phân loại dựa trên: Vốn nhỏ, kinh nghiệm hạn chế, "
                "giao dịch thường xuyên với rủi ro cao, kỷ luật chưa tốt. "
                "Cần tập trung vào học hỏi và quản lý rủi ro."
            ),
            "Technical Day/Swing Trader": (
                "Phân loại dựa trên: Có kinh nghiệm, sử dụng phân tích kỹ thuật, "
                "kỷ luật tốt, win rate ổn định. Phong cách giao dịch ngắn-trung hạn "
                "với quản lý rủi ro hợp lý."
            ),
            "Long-term Value Investor": (
                "Phân loại dựa trên: Vốn lớn, mục tiêu dài hạn, nắm giữ vị thế lâu, "
                "rủi ro thấp, tập trung vào giá trị và tăng trưởng bền vững."
            ),
            "Part-time Opportunist": (
                "Phân loại dựa trên: Thời gian theo dõi hạn chế, giao dịch theo cơ hội, "
                "cân bằng giữa công việc chính và trading. Phong cách thực dụng, linh hoạt."
            ),
            "Asset Specialist Trader": (
                "Phân loại dựa trên: Tập trung cao vào một loại tài sản cụ thể, "
                "hiểu sâu về thị trường đó, nhưng thiếu đa dạng hóa."
            )
        }
        
        return explanations.get(trader_type, "Không có thông tin")

