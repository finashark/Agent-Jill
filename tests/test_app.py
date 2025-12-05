"""
Unit tests for Trading Advisor modules
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from data_loader import TradeDataLoader
from metrics_calculator import PerformanceMetrics
from user_profile import UserProfile
from trader_classifier import TraderClassifier
from advisor import TradingAdvisor

@pytest.fixture
def sample_trade_data():
    """Sample trading data for testing"""
    data = {
        'TICKET': [1, 2, 3],
        'SYMBOL': ['EURUSD', 'GBPUSD', 'EURUSD'],
        'ACTION': ['BUY', 'SELL', 'BUY'],
        'LOTS': [0.1, 0.2, 0.15],
        'OPEN TIME': ['2025-01-01 10:00:00', '2025-01-01 11:00:00', '2025-01-01 12:00:00'],
        'CLOSE TIME': ['2025-01-01 15:00:00', '2025-01-01 16:00:00', '2025-01-01 17:00:00'],
        'PROFIT': [10.5, -5.2, 15.8],
        'COMM': [0, 0, 0],
        'SWAP': [0, 0, 0],
        'COMMENT': ['', '', ''],
        'T/P': [0, 0, 0],
        'S/L': [1.1000, 0, 1.1100],
        'OPEN PRICE': [1.0950, 1.2500, 1.0980],
        'CLOSE PRICE': [1.1000, 1.2480, 1.1030]
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_profile():
    """Sample user profile for testing"""
    return {
        'name': 'Test User',
        'age': 30,
        'gender': 'Nam',
        'education': 'Đại học',
        'income': '$50,000 - $100,000',
        'capital': 10000,
        'experience': '1 - 3 năm',
        'goals': ['Thu nhập đều đặn'],
        'risk_tolerance': 5,
        'available_time': '3 - 6 giờ'
    }

def test_data_loader_parse(sample_trade_data):
    """Test data loader parsing"""
    loader = TradeDataLoader()
    # Test that sample data is valid
    assert len(sample_trade_data) == 3
    assert 'PROFIT' in sample_trade_data.columns

def test_metrics_calculator(sample_trade_data):
    """Test metrics calculation"""
    calc = PerformanceMetrics(sample_trade_data)
    metrics = calc.calculate_all_metrics()
    
    assert 'total_pnl' in metrics
    assert 'win_rate' in metrics
    assert 'total_trades' in metrics
    assert metrics['total_trades'] == 3

def test_user_profile_validation(sample_profile):
    """Test user profile validation"""
    profile = UserProfile()
    assert profile.validate_profile(sample_profile) == True

def test_trader_classification(sample_profile, sample_trade_data):
    """Test trader classification"""
    calc = PerformanceMetrics(sample_trade_data)
    metrics = calc.calculate_all_metrics()
    
    classifier = TraderClassifier()
    classification = classifier.classify_trader_type(sample_profile, metrics)
    
    assert 'trader_type' in classification
    assert 'confidence_score' in classification
    assert 'trading_style' in classification

def test_advisor_generation(sample_profile, sample_trade_data):
    """Test advisory generation"""
    calc = PerformanceMetrics(sample_trade_data)
    metrics = calc.calculate_all_metrics()
    
    classifier = TraderClassifier()
    classification = classifier.classify_trader_type(sample_profile, metrics)
    
    advisor = TradingAdvisor()
    report = advisor.generate_full_report(classification['trader_type'], metrics)
    
    assert 'strengths' in report
    assert 'weaknesses' in report
    assert 'recommendations' in report
    assert 'risk_warnings' in report

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
