"""
Trading Advisor Module - English Version
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
            strengths.append(f"Good win rate ({metrics['win_rate']:.1f}%)")
        
        if metrics.get('risk_reward_ratio', 0) > 1.5:
            strengths.append(f"Positive Risk/Reward ratio ({metrics['risk_reward_ratio']:.2f})")
        
        sl_usage = metrics.get('stop_loss_usage', 0)
        if sl_usage > 70:
            strengths.append(f"Good Stop Loss discipline ({sl_usage:.1f}%)")
        
        if metrics.get('max_drawdown', 100) < 15:
            strengths.append(f"Good drawdown control ({metrics['max_drawdown']:.1f}%)")
        
        if metrics.get('profit_factor', 0) > 1.5:
            strengths.append(f"Strong Profit Factor ({metrics['profit_factor']:.2f})")
        
        # Type-specific strengths
        type_strengths = {
            "Newbie Gambler": [
                "Enthusiastic and willing to learn",
                "Active in trading"
            ],
            "Technical Day/Swing Trader": [
                "Clear trading system",
                "Technical analysis knowledge",
                "Disciplined risk management"
            ],
            "Long-term Value Investor": [
                "Long-term vision and patience",
                "Portfolio diversification",
                "Conservative risk management"
            ],
            "Part-time Opportunist": [
                "Good work-trading balance",
                "Pragmatic and flexible",
                "Emotion control"
            ],
            "Asset Specialist Trader": [
                "Deep market knowledge",
                "High focus",
                "Specialized experience"
            ]
        }
        
        strengths.extend(type_strengths.get(trader_type, []))
        
        return strengths
    
    def get_weaknesses(self, trader_type: str, metrics: Dict[str, Any]) -> List[str]:
        """Identify areas for improvement"""
        weaknesses = []
        
        # Based on metrics
        if metrics.get('win_rate', 100) < 45:
            weaknesses.append(f"Low win rate ({metrics['win_rate']:.1f}%)")
        
        if metrics.get('risk_reward_ratio', 10) < 1:
            weaknesses.append(f"Poor Risk/Reward ratio ({metrics['risk_reward_ratio']:.2f})")
        
        sl_usage = metrics.get('stop_loss_usage', 100)
        if sl_usage < 50:
            weaknesses.append(f"Poor Stop Loss discipline ({sl_usage:.1f}%)")
        
        if metrics.get('max_drawdown', 0) > 30:
            weaknesses.append(f"Excessive drawdown ({metrics['max_drawdown']:.1f}%)")
        
        freq = metrics.get('avg_trades_per_day', 0)
        if freq > 20:
            weaknesses.append(f"Overtrading ({freq:.1f} trades/day)")
        
        # Type-specific weaknesses
        type_weaknesses = {
            "Newbie Gambler": [
                "Lack of experience and knowledge",
                "Emotional trading",
                "Excessive risk-taking"
            ],
            "Technical Day/Swing Trader": [
                "Over-confidence in system",
                "Psychological pressure from frequent trading"
            ],
            "Asset Specialist Trader": [
                "Lack of diversification (concentration risk)",
                "Over-dependence on single market"
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
                "Take basic trading courses",
                "Reduce trading volume by 50%",
                "Always set stop loss before entering trades",
                "Never risk >2% per trade",
                "Keep a trading journal to learn from mistakes",
                "Use demo account for practice"
            ],
            "Technical Day/Swing Trader": [
                "Continue backtesting and optimizing strategy",
                "Set daily trade limits to avoid overtrading",
                "Take breaks after losing streaks to avoid revenge trading",
                "Diversify portfolio further to reduce risk",
                "Monitor major economic news to avoid volatility"
            ],
            "Long-term Value Investor": [
                "Continue current long-term strategy",
                "Rebalance portfolio quarterly",
                "Monitor macroeconomic indicators",
                "Consider additional safe investment channels",
                "Update fundamental analysis knowledge"
            ],
            "Part-time Opportunist": [
                "Optimize trading time (focus on quality over quantity)",
                "Consider using alerts and automation",
                "Set price alerts to not miss opportunities",
                "Focus on swing trading instead of scalping",
                "Plan trades weekly in advance"
            ],
            "Asset Specialist Trader": [
                "Diversify into 2-3 other assets",
                "Monitor correlation between markets",
                "Use hedging to protect positions",
                "Expand knowledge to related markets",
                "Allocate no more than 50% capital to single asset"
            ]
        }
        
        recommendations.extend(type_recommendations.get(trader_type, []))
        
        return recommendations
    
    def get_risk_warnings(self, trader_type: str, metrics: Dict[str, Any]) -> List[str]:
        """Get risk warnings"""
        warnings = []
        
        # Critical warnings based on metrics
        if metrics.get('max_drawdown', 0) > 30:
            warnings.append("ACCOUNT BURNOUT RISK: Drawdown too high!")
        
        if metrics.get('win_rate', 50) < 40:
            warnings.append("Win rate too low - stop trading and review strategy")
        
        freq = metrics.get('avg_trades_per_day', 0)
        if freq > 20:
            warnings.append("Severe overtrading - reduce trades per day")
        
        # Type-specific warnings
        type_warnings = {
            "Newbie Gambler": [
                "High account burnout risk from overtrading",
                "Easy to fall into overconfidence trap after wins",
                "FOMO psychology can lead to bad decisions"
            ],
            "Technical Day/Swing Trader": [
                "Abnormal markets can break technical systems",
                "Watch for confirmation bias",
                "Burnout risk from excessive trading"
            ],
            "Long-term Value Investor": [
                "Large short-term volatility can cause panic",
                "Overnight swap fees can erode profits",
                "Black swan events can cause major losses"
            ],
            "Part-time Opportunist": [
                "Missing important news when not monitoring",
                "Price gaps when market opens",
                "Cannot react quickly to sudden volatility"
            ],
            "Asset Specialist Trader": [
                "High concentration risk if market collapses",
                "Correlation risk from single asset trading",
                "Lack of diversification increases portfolio volatility"
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
                f"You are a beginner trader with a risk-taking style. "
                f"Current win rate {win_rate:.1f}% and P&L ${total_pnl:.2f}. "
                f"Focus on learning and risk management before increasing volume."
            ),
            "Technical Day/Swing Trader": (
                f"You are an experienced technical trader. "
                f"Win rate {win_rate:.1f}% shows you're on the right track. "
                f"Continue optimizing your system and maintaining discipline."
            ),
            "Long-term Value Investor": (
                f"You are a long-term investor with far-sighted vision. "
                f"Conservative approach fits your goals of capital preservation and sustainable growth. "
                f"Continue maintaining current strategy."
            ),
            "Part-time Opportunist": (
                f"You balance work and trading well. "
                f"Win rate {win_rate:.1f}% is reasonable for part-time trader. "
                f"Optimize time and tools to increase efficiency."
            ),
            "Asset Specialist Trader": (
                f"You specialize in specific asset class. "
                f"Specialized knowledge is strength, but diversification needed to reduce risk. "
                f"Consider expanding to 2-3 related markets."
            )
        }
        
        return summaries.get(trader_type, "No summary available")
