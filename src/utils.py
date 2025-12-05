"""
Utility functions for the Trading Advisor app
"""

import streamlit as st
import logging
from functools import wraps
from typing import Any, Callable

logger = logging.getLogger(__name__)

def handle_errors(func: Callable) -> Callable:
    """Decorator to handle errors gracefully"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            st.error(f"❌ Đã xảy ra lỗi: {str(e)}")
            return None
    return wrapper

@st.cache_data(ttl=3600)
def load_config(config_path: str) -> dict:
    """Load and cache configuration files"""
    import yaml
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@st.cache_data(ttl=600)
def process_csv_data(csv_string: str) -> Any:
    """Cache CSV processing results"""
    from data_loader import TradeDataLoader
    loader = TradeDataLoader()
    return loader.parse_csv_string(csv_string)

def validate_dataframe(df: Any, required_columns: list) -> bool:
    """Validate dataframe has required columns"""
    if df is None or len(df) == 0:
        return False
    missing = set(required_columns) - set(df.columns)
    if missing:
        logger.warning(f"Missing columns: {missing}")
        return False
    return True

def format_number(value: float, decimals: int = 2) -> str:
    """Format number with locale-specific formatting"""
    return f"{value:,.{decimals}f}"

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safe division with default value"""
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ZeroDivisionError):
        return default
