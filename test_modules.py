"""
Comprehensive test script for Trading Advisor modules
Tests each component individually to identify bugs and issues
"""

import sys
from pathlib import Path
import pandas as pd
import traceback

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

def test_imports():
    """Test all imports"""
    print("\n" + "="*60)
    print("TEST 1: IMPORTS")
    print("="*60)
    
    errors = []
    
    try:
        from user_profile import UserProfile
        print("✓ user_profile imported successfully")
    except Exception as e:
        errors.append(f"user_profile: {str(e)}")
        print(f"✗ user_profile failed: {str(e)}")
    
    try:
        from data_loader import TradeDataLoader
        print("✓ data_loader imported successfully")
    except Exception as e:
        errors.append(f"data_loader: {str(e)}")
        print(f"✗ data_loader failed: {str(e)}")
    
    try:
        from metrics_calculator import PerformanceMetrics
        print("✓ metrics_calculator imported successfully")
    except Exception as e:
        errors.append(f"metrics_calculator: {str(e)}")
        print(f"✗ metrics_calculator failed: {str(e)}")
    
    try:
        from trader_classifier import TraderClassifier
        print("✓ trader_classifier imported successfully")
    except Exception as e:
        errors.append(f"trader_classifier: {str(e)}")
        print(f"✗ trader_classifier failed: {str(e)}")
    
    try:
        from advisor import TradingAdvisor
        print("✓ advisor imported successfully")
    except Exception as e:
        errors.append(f"advisor: {str(e)}")
        print(f"✗ advisor failed: {str(e)}")
    
    try:
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
        print("✓ visualizations imported successfully")
    except Exception as e:
        errors.append(f"visualizations: {str(e)}")
        print(f"✗ visualizations failed: {str(e)}")
    
    return errors

def test_data_loader():
    """Test data loading functionality"""
    print("\n" + "="*60)
    print("TEST 2: DATA LOADER")
    print("="*60)
    
    errors = []
    
    try:
        from data_loader import TradeDataLoader
        
        # Test with sample data file
        data_path = Path(__file__).parent / 'data' / 'sample_trades.csv'
        
        if not data_path.exists():
            errors.append(f"Sample data file not found: {data_path}")
            print(f"✗ Sample data file not found: {data_path}")
            return errors
        
        print(f"Loading data from: {data_path}")
        loader = TradeDataLoader(str(data_path), source_type='file')
        
        # Load data
        df = loader.load_from_file(str(data_path))
        print(f"✓ Data loaded successfully: {len(df)} rows")
        print(f"  Columns: {list(df.columns)}")
        
        # Check for required columns
        required_cols = ['OPEN TIME', 'CLOSE TIME', 'SYMBOL', 'ACTION', 'PROFIT']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            errors.append(f"Missing required columns: {missing_cols}")
            print(f"✗ Missing required columns: {missing_cols}")
        else:
            print(f"✓ All required columns present")
        
        # Check data types
        print(f"✓ Data preprocessing successful (done in load_from_file)")
        print(f"  Date columns parsed: {'OPEN TIME' in df.columns and pd.api.types.is_datetime64_any_dtype(df['OPEN TIME'])}")
        
    except Exception as e:
        errors.append(f"data_loader test: {str(e)}")
        print(f"✗ data_loader test failed: {str(e)}")
        traceback.print_exc()
    
    return errors

def test_metrics_calculator():
    """Test metrics calculation"""
    print("\n" + "="*60)
    print("TEST 3: METRICS CALCULATOR")
    print("="*60)
    
    errors = []
    
    try:
        from data_loader import TradeDataLoader
        from metrics_calculator import PerformanceMetrics
        
        # Load sample data
        data_path = Path(__file__).parent / 'data' / 'sample_trades.csv'
        loader = TradeDataLoader(str(data_path), source_type='file')
        df = loader.load_from_file(str(data_path))
        
        # Calculate metrics
        calculator = PerformanceMetrics(df)
        metrics = calculator.calculate_all_metrics()
        
        print(f"✓ Metrics calculated successfully")
        print(f"  Total metrics: {len(metrics)}")
        print(f"  Sample metrics:")
        
        # Show key metrics
        key_metrics = ['total_trades', 'win_rate', 'total_pnl', 'avg_win', 'avg_loss', 'profit_factor']
        for key in key_metrics:
            if key in metrics:
                print(f"    {key}: {metrics[key]}")
        
    except Exception as e:
        errors.append(f"metrics_calculator test: {str(e)}")
        print(f"✗ metrics_calculator test failed: {str(e)}")
        traceback.print_exc()
    
    return errors

def test_trader_classifier():
    """Test trader classification"""
    print("\n" + "="*60)
    print("TEST 4: TRADER CLASSIFIER")
    print("="*60)
    
    errors = []
    
    try:
        from data_loader import TradeDataLoader
        from metrics_calculator import PerformanceMetrics
        from trader_classifier import TraderClassifier
        
        # Load sample data
        data_path = Path(__file__).parent / 'data' / 'sample_trades.csv'
        loader = TradeDataLoader(str(data_path), source_type='file')
        df = loader.load_from_file(str(data_path))
        
        # Calculate metrics
        calculator = PerformanceMetrics(df)
        metrics = calculator.calculate_all_metrics()
        
        # Create sample profile
        profile = {
            'basic_info': {
                'name': 'Test User',
                'age': 35,
                'gender': 'Nam',
                'education': 'Đại học'
            },
            'financial_info': {
                'income': 'Từ 30-50 triệu',
                'trading_capital': 'Từ 100-500 triệu',
                'investment_ratio': '20-40%'
            },
            'experience_goals': {
                'trading_experience': '1-3 năm',
                'primary_goal': 'Tăng trưởng vốn dài hạn',
                'expected_return': '10-20%/năm'
            },
            'self_assessment': {
                'risk_tolerance': 5,
                'emotion_control': 6,
                'discipline': 7
            }
        }
        
        # Classify trader
        classifier = TraderClassifier()
        classification = classifier.classify_trader_type(profile, metrics)
        
        print(f"✓ Classification successful")
        print(f"  Trader type: {classification.get('trader_type', 'N/A')}")
        print(f"  Confidence: {classification.get('confidence_score', 0)}%")
        print(f"  Trading style: {classification.get('trading_style', 'N/A')}")
        print(f"  Risk level: {classification.get('risk_level', 'N/A')}")
        
    except Exception as e:
        errors.append(f"trader_classifier test: {str(e)}")
        print(f"✗ trader_classifier test failed: {str(e)}")
        traceback.print_exc()
    
    return errors

def test_advisor():
    """Test trading advisor"""
    print("\n" + "="*60)
    print("TEST 5: TRADING ADVISOR")
    print("="*60)
    
    errors = []
    
    try:
        from data_loader import TradeDataLoader
        from metrics_calculator import PerformanceMetrics
        from trader_classifier import TraderClassifier
        from advisor import TradingAdvisor
        
        # Load sample data
        data_path = Path(__file__).parent / 'data' / 'sample_trades.csv'
        loader = TradeDataLoader(str(data_path), source_type='file')
        df = loader.load_from_file(str(data_path))
        
        # Calculate metrics
        calculator = PerformanceMetrics(df)
        metrics = calculator.calculate_all_metrics()
        
        # Create sample profile
        profile = {
            'basic_info': {
                'name': 'Test User',
                'age': 35,
                'gender': 'Nam',
                'education': 'Đại học'
            },
            'financial_info': {
                'income': 'Từ 30-50 triệu',
                'trading_capital': 'Từ 100-500 triệu',
                'investment_ratio': '20-40%'
            },
            'experience_goals': {
                'trading_experience': '1-3 năm',
                'primary_goal': 'Tăng trưởng vốn dài hạn',
                'expected_return': '10-20%/năm'
            },
            'self_assessment': {
                'risk_tolerance': 5,
                'emotion_control': 6,
                'discipline': 7
            }
        }
        
        # Classify trader
        classifier = TraderClassifier()
        classification = classifier.classify_trader_type(profile, metrics)
        
        # Generate advice
        advisor = TradingAdvisor()
        advice = advisor.generate_full_report(classification['trader_type'], metrics)
        
        print(f"✓ Advice generation successful")
        print(f"  Trader type: {advice.get('trader_type', 'N/A')}")
        print(f"  Strengths: {len(advice.get('strengths', []))}")
        print(f"  Weaknesses: {len(advice.get('weaknesses', []))}")
        print(f"  Recommendations: {len(advice.get('recommendations', []))}")
        
    except Exception as e:
        errors.append(f"advisor test: {str(e)}")
        print(f"✗ advisor test failed: {str(e)}")
        traceback.print_exc()
    
    return errors

def test_visualizations():
    """Test visualization functions"""
    print("\n" + "="*60)
    print("TEST 6: VISUALIZATIONS")
    print("="*60)
    
    errors = []
    
    try:
        from data_loader import TradeDataLoader
        from metrics_calculator import PerformanceMetrics
        from visualizations import (
            plot_pnl_timeline,
            plot_symbol_distribution,
            plot_win_loss_distribution,
            plot_trading_hours_heatmap,
            plot_holding_time_boxplot,
            plot_daily_pnl
        )
        
        # Load sample data
        data_path = Path(__file__).parent / 'data' / 'sample_trades.csv'
        loader = TradeDataLoader(str(data_path), source_type='file')
        df = loader.load_from_file(str(data_path))
        
        # Calculate metrics
        calculator = PerformanceMetrics(df)
        metrics = calculator.calculate_all_metrics()
        
        # Test each visualization
        viz_tests = [
            ('PnL Timeline', lambda: plot_pnl_timeline(df)),
            ('Symbol Distribution', lambda: plot_symbol_distribution(df)),
            ('Win/Loss Distribution', lambda: plot_win_loss_distribution(df)),
            ('Trading Hours Heatmap', lambda: plot_trading_hours_heatmap(df)),
            ('Holding Time Boxplot', lambda: plot_holding_time_boxplot(df)),
            ('Daily PnL', lambda: plot_daily_pnl(df))
        ]
        
        for viz_name, viz_func in viz_tests:
            try:
                fig = viz_func()
                if fig is not None:
                    print(f"✓ {viz_name} created successfully")
                else:
                    print(f"⚠ {viz_name} returned None")
            except Exception as e:
                errors.append(f"{viz_name}: {str(e)}")
                print(f"✗ {viz_name} failed: {str(e)}")
        
    except Exception as e:
        errors.append(f"visualizations test: {str(e)}")
        print(f"✗ visualizations test failed: {str(e)}")
        traceback.print_exc()
    
    return errors

def test_yaml_configs():
    """Test YAML configuration loading"""
    print("\n" + "="*60)
    print("TEST 7: YAML CONFIGURATIONS")
    print("="*60)
    
    errors = []
    
    import yaml
    
    config_files = [
        'config/form_fields.yaml',
        'config/trader_profiles.yaml',
        'config/advisory_rules.yaml'
    ]
    
    for config_file in config_files:
        try:
            config_path = Path(__file__).parent / config_file
            
            if not config_path.exists():
                errors.append(f"{config_file} not found")
                print(f"✗ {config_file} not found")
                continue
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            print(f"✓ {config_file} loaded successfully")
            print(f"  Keys: {list(config.keys()) if isinstance(config, dict) else 'Not a dict'}")
            
        except Exception as e:
            errors.append(f"{config_file}: {str(e)}")
            print(f"✗ {config_file} failed: {str(e)}")
    
    return errors

def main():
    """Run all tests"""
    print("\n" + "="*80)
    print(" TRADING ADVISOR - COMPREHENSIVE MODULE TESTING")
    print("="*80)
    
    all_errors = []
    
    # Run all tests
    all_errors.extend(test_imports())
    all_errors.extend(test_yaml_configs())
    all_errors.extend(test_data_loader())
    all_errors.extend(test_metrics_calculator())
    all_errors.extend(test_trader_classifier())
    all_errors.extend(test_advisor())
    all_errors.extend(test_visualizations())
    
    # Summary
    print("\n" + "="*80)
    print(" TEST SUMMARY")
    print("="*80)
    
    if all_errors:
        print(f"\n❌ FAILED: {len(all_errors)} error(s) found:\n")
        for i, error in enumerate(all_errors, 1):
            print(f"{i}. {error}")
    else:
        print("\n✅ SUCCESS: All tests passed!")
    
    print("\n" + "="*80)
    
    return len(all_errors) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
