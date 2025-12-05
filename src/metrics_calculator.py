"""
Metrics Calculator Module
Calculates trading performance metrics
"""

import pandas as pd
import numpy as np
from typing import Dict, Any

class PerformanceMetrics:
    """Calculate trading performance metrics"""
    
    def __init__(self, trades_df: pd.DataFrame):
        """
        Initialize with trades dataframe
        
        Args:
            trades_df: DataFrame containing trade history
        """
        self.df = trades_df.copy()
        self.metrics = {}
        
    def total_pnl(self) -> float:
        """Calculate total profit/loss"""
        return self.df['PROFIT'].sum()
    
    def win_rate(self) -> float:
        """Calculate percentage of winning trades"""
        wins = len(self.df[self.df['PROFIT'] > 0])
        total = len(self.df)
        return (wins / total * 100) if total > 0 else 0.0
    
    def total_trades(self) -> int:
        """Total number of trades"""
        return len(self.df)
    
    def winning_trades(self) -> int:
        """Number of winning trades"""
        return len(self.df[self.df['PROFIT'] > 0])
    
    def losing_trades(self) -> int:
        """Number of losing trades"""
        return len(self.df[self.df['PROFIT'] < 0])
    
    def avg_win(self) -> float:
        """Average winning trade"""
        wins = self.df[self.df['PROFIT'] > 0]['PROFIT']
        return wins.mean() if len(wins) > 0 else 0.0
    
    def avg_loss(self) -> float:
        """Average losing trade"""
        losses = self.df[self.df['PROFIT'] < 0]['PROFIT']
        return losses.mean() if len(losses) > 0 else 0.0
    
    def largest_win(self) -> float:
        """Largest winning trade"""
        return self.df['PROFIT'].max()
    
    def largest_loss(self) -> float:
        """Largest losing trade"""
        return self.df['PROFIT'].min()
    
    def max_drawdown(self) -> float:
        """Calculate maximum drawdown percentage"""
        cumulative = self.df['PROFIT'].cumsum()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max)
        max_dd = drawdown.min()
        
        # Convert to percentage
        if running_max.max() > 0:
            max_dd_pct = (max_dd / running_max.max() * 100)
        else:
            max_dd_pct = 0.0
            
        return abs(max_dd_pct)
    
    def risk_reward_ratio(self) -> float:
        """Calculate average risk/reward ratio"""
        avg_w = self.avg_win()
        avg_l = abs(self.avg_loss())
        
        if avg_l > 0:
            return avg_w / avg_l
        return 0.0
    
    def trading_frequency(self) -> Dict[str, float]:
        """Calculate trading frequency"""
        if 'OPEN TIME' not in self.df.columns:
            return {'trades_per_day': 0, 'trades_per_week': 0}
        
        # Get date range
        start_date = self.df['OPEN TIME'].min()
        end_date = self.df['OPEN TIME'].max()
        
        if pd.isna(start_date) or pd.isna(end_date):
            return {'trades_per_day': 0, 'trades_per_week': 0}
        
        days = (end_date - start_date).days + 1
        weeks = days / 7
        
        trades_per_day = len(self.df) / days if days > 0 else 0
        trades_per_week = len(self.df) / weeks if weeks > 0 else 0
        
        return {
            'trades_per_day': round(trades_per_day, 2),
            'trades_per_week': round(trades_per_week, 2),
            'total_days': days
        }
    
    def avg_holding_time(self) -> Dict[str, float]:
        """Calculate average position holding time"""
        if 'DURATION_MINUTES' not in self.df.columns:
            return {'minutes': 0, 'hours': 0, 'days': 0}
        
        avg_minutes = self.df['DURATION_MINUTES'].mean()
        
        if pd.isna(avg_minutes):
            return {'minutes': 0, 'hours': 0, 'days': 0}
        
        return {
            'minutes': round(avg_minutes, 2),
            'hours': round(avg_minutes / 60, 2),
            'days': round(avg_minutes / 1440, 2)
        }
    
    def stop_loss_usage(self) -> Dict[str, Any]:
        """Analyze stop loss usage"""
        if 'COMMENT' not in self.df.columns:
            return {'usage_rate': 0, 'sl_trades': 0}
        
        # Count trades with [sl] in comment
        sl_trades = self.df[self.df['COMMENT'].str.contains('[sl]', na=False, case=False)]
        sl_count = len(sl_trades)
        total = len(self.df)
        
        usage_rate = (sl_count / total * 100) if total > 0 else 0.0
        
        return {
            'usage_rate': round(usage_rate, 2),
            'sl_trades': sl_count,
            'total_trades': total
        }
    
    def profit_factor(self) -> float:
        """Calculate profit factor (gross profit / gross loss)"""
        gross_profit = self.df[self.df['PROFIT'] > 0]['PROFIT'].sum()
        gross_loss = abs(self.df[self.df['PROFIT'] < 0]['PROFIT'].sum())
        
        if gross_loss > 0:
            return gross_profit / gross_loss
        return 0.0
    
    def symbol_analysis(self) -> pd.DataFrame:
        """Analyze performance by symbol"""
        if 'SYMBOL' not in self.df.columns:
            return pd.DataFrame()
        
        symbol_stats = self.df.groupby('SYMBOL').agg({
            'PROFIT': ['sum', 'mean', 'count'],
            'LOTS': 'sum'
        }).round(2)
        
        symbol_stats.columns = ['Total P&L', 'Avg P&L', 'Trades', 'Total Lots']
        symbol_stats = symbol_stats.sort_values('Total P&L', ascending=False)
        
        return symbol_stats
    
    def calculate_all_metrics(self) -> Dict[str, Any]:
        """Calculate all metrics and return as dictionary"""
        # Get nested metrics
        trading_freq = self.trading_frequency()
        holding_time = self.avg_holding_time()
        sl_usage = self.stop_loss_usage()
        
        # Get symbol analysis
        symbol_stats = self.symbol_analysis()
        symbol_dict = {}
        if not symbol_stats.empty:
            for symbol in symbol_stats.index:
                symbol_dict[symbol] = {
                    'pnl': symbol_stats.loc[symbol, 'Total P&L'],
                    'avg_pnl': symbol_stats.loc[symbol, 'Avg P&L'],
                    'count': symbol_stats.loc[symbol, 'Trades'],
                    'lots': symbol_stats.loc[symbol, 'Total Lots']
                }
        
        self.metrics = {
            'total_pnl': round(self.total_pnl(), 2),
            'win_rate': round(self.win_rate(), 2),
            'total_trades': self.total_trades(),
            'winning_trades': self.winning_trades(),
            'losing_trades': self.losing_trades(),
            'avg_win': round(self.avg_win(), 2),
            'avg_loss': round(self.avg_loss(), 2),
            'best_trade': round(self.largest_win(), 2),
            'worst_trade': round(self.largest_loss(), 2),
            'max_drawdown': round(self.max_drawdown(), 2),
            'risk_reward_ratio': round(self.risk_reward_ratio(), 2),
            'profit_factor': round(self.profit_factor(), 2),
            # Flatten nested dicts for easy access
            'avg_trades_per_day': trading_freq.get('trades_per_day', 0),
            'avg_trades_per_week': trading_freq.get('trades_per_week', 0),
            'total_trading_days': trading_freq.get('total_days', 0),
            'avg_holding_minutes': holding_time.get('minutes', 0),
            'avg_holding_hours': holding_time.get('hours', 0),
            'avg_holding_days': holding_time.get('days', 0),
            'stop_loss_usage': sl_usage.get('usage_rate', 0),
            'sl_trades_count': sl_usage.get('sl_trades', 0),
            'symbol_analysis': symbol_dict
        }
        
        return self.metrics
