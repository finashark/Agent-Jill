"""
Data Loader Module
Handles loading and preprocessing of trading data from CSV
"""

import pandas as pd
import numpy as np
from io import StringIO
from typing import Optional, Tuple
import re

class TradeDataLoader:
    """Load and preprocess trading data from CSV string or file"""
    
    def __init__(self, data_source: str = None, source_type: str = 'paste'):
        """
        Initialize data loader
        
        Args:
            data_source: CSV string (if paste) or filepath (if file) - optional
            source_type: 'paste' or 'file'
        """
        self.data_source = data_source
        self.source_type = source_type
        self.df = None
        self.trades_df = None
        self.balance_df = None
        
    def detect_delimiter(self, sample: str) -> str:
        """Auto-detect CSV delimiter"""
        delimiters = [',', '\t', ';', '|']
        delimiter_counts = {}
        
        # Count occurrences of each delimiter in first line
        first_line = sample.split('\n')[0]
        for delim in delimiters:
            delimiter_counts[delim] = first_line.count(delim)
        
        # Return delimiter with highest count
        return max(delimiter_counts, key=delimiter_counts.get)
    
    def _process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process and clean a dataframe"""
        # Remove quotes from column names and standardize
        df.columns = df.columns.str.replace('"', '').str.strip()
        
        # Convert numeric columns
        numeric_cols = ['LOTS', 'PROFIT', 'COMM', 'SWAP', 'T/P', 'S/L', 
                       'OPEN PRICE', 'CLOSE PRICE']
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Parse date columns
        date_cols = ['OPEN TIME', 'CLOSE TIME']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Calculate duration if dates are present
        if 'OPEN TIME' in df.columns and 'CLOSE TIME' in df.columns:
            df['DURATION_MINUTES'] = (
                (df['CLOSE TIME'] - df['OPEN TIME']).dt.total_seconds() / 60
            )
        
        return df
    
    def parse_csv_string(self, csv_string: str) -> pd.DataFrame:
        """Parse CSV from pasted text and return cleaned, processed data"""
        try:
            # Detect delimiter
            delimiter = self.detect_delimiter(csv_string)
            
            # Parse CSV
            df = pd.read_csv(
                StringIO(csv_string),
                delimiter=delimiter,
                encoding='utf-8',
                on_bad_lines='skip'
            )
            
            # Clean and process the data
            df = self._process_dataframe(df)
            
            return df
        except Exception as e:
            raise ValueError(f"Error parsing CSV: {str(e)}")
    
    def load_from_file(self, filepath: str) -> pd.DataFrame:
        """Load CSV from uploaded file and return cleaned, processed data"""
        try:
            df = pd.read_csv(filepath, encoding='utf-8', on_bad_lines='skip')
            
            # Clean and process the data
            df = self._process_dataframe(df)
            
            return df
        except Exception as e:
            raise ValueError(f"Error loading file: {str(e)}")
    
    def load(self) -> pd.DataFrame:
        """Load data based on source type"""
        if self.source_type == 'paste':
            self.df = self.parse_csv_string(self.data_source)
        else:
            self.df = self.load_from_file(self.data_source)
        
        return self.df
    
    def clean_data(self) -> pd.DataFrame:
        """Handle missing values and convert types"""
        if self.df is None:
            raise ValueError("No data loaded. Call load() first.")
        
        # Remove quotes from column names
        self.df.columns = self.df.columns.str.replace('"', '').str.strip()
        
        # Convert numeric columns
        numeric_cols = ['LOTS', 'PROFIT', 'COMM', 'SWAP', 'T/P', 'S/L', 
                       'OPEN PRICE', 'CLOSE PRICE']
        
        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        return self.df
    
    def parse_dates(self) -> pd.DataFrame:
        """Convert date strings to datetime"""
        if self.df is None:
            raise ValueError("No data loaded.")
        
        date_cols = ['OPEN TIME', 'CLOSE TIME']
        
        for col in date_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        
        return self.df
    
    def calculate_duration(self) -> pd.DataFrame:
        """Calculate holding time for each trade in minutes"""
        if self.df is None:
            raise ValueError("No data loaded.")
        
        if 'OPEN TIME' in self.df.columns and 'CLOSE TIME' in self.df.columns:
            self.df['DURATION_MINUTES'] = (
                (self.df['CLOSE TIME'] - self.df['OPEN TIME'])
                .dt.total_seconds() / 60
            )
        
        return self.df
    
    def identify_balance_transactions(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Separate balance transactions from trades"""
        if self.df is None:
            raise ValueError("No data loaded.")
        
        # Balance transactions have empty SYMBOL or contain "Balance"
        balance_mask = (
            self.df['SYMBOL'].isna() | 
            (self.df['SYMBOL'] == '') | 
            (self.df['ACTION'] == 'Balance')
        )
        
        self.balance_df = self.df[balance_mask].copy()
        self.trades_df = self.df[~balance_mask].copy()
        
        return self.trades_df, self.balance_df
    
    def process_all(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Run full preprocessing pipeline"""
        self.load()
        self.clean_data()
        self.parse_dates()
        self.calculate_duration()
        self.identify_balance_transactions()
        
        return self.trades_df, self.balance_df
    
    def get_data_summary(self) -> dict:
        """Get summary statistics of loaded data"""
        if self.trades_df is None:
            return {}
        
        return {
            'total_trades': len(self.trades_df),
            'date_range': {
                'start': self.trades_df['OPEN TIME'].min(),
                'end': self.trades_df['CLOSE TIME'].max()
            },
            'symbols': self.trades_df['SYMBOL'].unique().tolist(),
            'total_balance_transactions': len(self.balance_df) if self.balance_df is not None else 0
        }
