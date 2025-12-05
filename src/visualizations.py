"""
Visualization Module
Creates charts and graphs for trading analysis
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

def plot_pnl_timeline(df: pd.DataFrame) -> go.Figure:
    """Plot cumulative P&L over time"""
    if 'CLOSE TIME' not in df.columns or 'PROFIT' not in df.columns:
        return go.Figure()
    
    # Sort by time
    df_sorted = df.sort_values('CLOSE TIME')
    df_sorted['Cumulative P&L'] = df_sorted['PROFIT'].cumsum()
    
    # Determine color based on final P&L
    final_pnl = df_sorted['Cumulative P&L'].iloc[-1]
    line_color = '#27ae60' if final_pnl >= 0 else '#e74c3c'
    fill_color = 'rgba(39, 174, 96, 0.2)' if final_pnl >= 0 else 'rgba(231, 76, 60, 0.2)'
    
    fig = go.Figure()
    
    # Add cumulative P&L line
    fig.add_trace(go.Scatter(
        x=df_sorted['CLOSE TIME'],
        y=df_sorted['Cumulative P&L'],
        mode='lines',
        name='Cumulative P&L',
        line=dict(color=line_color, width=3),
        fill='tozeroy',
        fillcolor=fill_color,
        hovertemplate='<b>Date:</b> %{x}<br><b>Cumulative P&L:</b> $%{y:,.2f}<extra></extra>'
    ))
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5, line_width=1)
    
    fig.update_layout(
        title=dict(
            text='Cumulative Profit & Loss Over Time',
            font=dict(size=16, color='#2c3e50')
        ),
        xaxis=dict(
            title='Date',
            showgrid=True,
            gridcolor='#ecf0f1'
        ),
        yaxis=dict(
            title='Cumulative P&L ($)',
            showgrid=True,
            gridcolor='#ecf0f1',
            tickformat='$,.0f'
        ),
        hovermode='x unified',
        template='plotly_white',
        height=450,
        margin=dict(l=60, r=20, t=60, b=60)
    )
    
    return fig

def plot_symbol_distribution(df: pd.DataFrame) -> go.Figure:
    """Plot distribution of trades by symbol"""
    if 'SYMBOL' not in df.columns:
        return go.Figure()
    
    symbol_counts = df['SYMBOL'].value_counts()
    
    # Create better color scheme
    colors = px.colors.qualitative.Set3
    
    fig = go.Figure(data=[go.Pie(
        labels=symbol_counts.index,
        values=symbol_counts.values,
        hole=0.35,
        marker=dict(
            colors=colors,
            line=dict(color='white', width=2)
        ),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(size=12),
        hovertemplate='<b>%{label}</b><br>Trades: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(
            text='Trading Distribution by Symbol',
            font=dict(size=16, color='#2c3e50')
        ),
        height=450,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(size=11)
        ),
        margin=dict(l=20, r=150, t=60, b=20)
    )
    
    return fig

def plot_win_loss_distribution(df: pd.DataFrame) -> go.Figure:
    """Plot histogram of profit/loss distribution"""
    if 'PROFIT' not in df.columns:
        return go.Figure()
    
    fig = go.Figure()
    
    # Separate wins and losses
    wins = df[df['PROFIT'] > 0]['PROFIT']
    losses = df[df['PROFIT'] < 0]['PROFIT']
    
    fig.add_trace(go.Histogram(
        x=wins,
        name='Winning Trades',
        marker=dict(
            color='#27ae60',
            line=dict(color='white', width=1)
        ),
        opacity=0.75,
        nbinsx=25,
        hovertemplate='<b>Wins</b><br>Profit: $%{x:,.2f}<br>Count: %{y}<extra></extra>'
    ))
    
    fig.add_trace(go.Histogram(
        x=losses,
        name='Losing Trades',
        marker=dict(
            color='#e74c3c',
            line=dict(color='white', width=1)
        ),
        opacity=0.75,
        nbinsx=25,
        hovertemplate='<b>Losses</b><br>Loss: $%{x:,.2f}<br>Count: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='Win/Loss Distribution',
            font=dict(size=16, color='#2c3e50')
        ),
        xaxis=dict(
            title='Profit/Loss ($)',
            showgrid=True,
            gridcolor='#ecf0f1',
            tickformat='$,.0f'
        ),
        yaxis=dict(
            title='Number of Trades',
            showgrid=True,
            gridcolor='#ecf0f1'
        ),
        barmode='overlay',
        template='plotly_white',
        height=450,
        margin=dict(l=60, r=20, t=60, b=60),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(255, 255, 255, 0.8)"
        )
    )
    
    return fig

def plot_trading_hours_heatmap(df: pd.DataFrame) -> go.Figure:
    """Plot heatmap of trading activity by hour and day"""
    if 'OPEN TIME' not in df.columns:
        return go.Figure()
    
    df_copy = df.copy()
    df_copy['Hour'] = df_copy['OPEN TIME'].dt.hour
    df_copy['DayOfWeek'] = df_copy['OPEN TIME'].dt.day_name()
    
    # Count trades by hour and day
    heatmap_data = df_copy.groupby(['DayOfWeek', 'Hour']).size().reset_index(name='Trades')
    
    # Pivot for heatmap
    heatmap_pivot = heatmap_data.pivot(index='DayOfWeek', columns='Hour', values='Trades').fillna(0)
    
    # Reorder days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_pivot = heatmap_pivot.reindex([d for d in day_order if d in heatmap_pivot.index])
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        colorscale='Blues',
        text=heatmap_pivot.values,
        texttemplate='%{text}',
        textfont=dict(size=10, color='white'),
        hovertemplate='<b>%{y}</b><br>Hour: %{x}:00<br>Trades: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='Trading Activity Heatmap (by Hour and Day)',
            font=dict(size=16, color='#2c3e50')
        ),
        xaxis=dict(
            title='Hour of Day (24h format)',
            tickmode='linear',
            tick0=0,
            dtick=2,
            showgrid=False
        ),
        yaxis=dict(
            title='Day of Week',
            showgrid=False
        ),
        height=450,
        template='plotly_white',
        margin=dict(l=100, r=100, t=60, b=60)
    )
    
    return fig

def plot_holding_time_boxplot(df: pd.DataFrame) -> go.Figure:
    """Plot boxplot of position holding time"""
    if 'DURATION_MINUTES' not in df.columns:
        return go.Figure()
    
    # Convert to hours for better readability
    df_copy = df.copy()
    df_copy['Duration_Hours'] = df_copy['DURATION_MINUTES'] / 60
    
    # Separate by win/loss
    df_copy['Result'] = df_copy['PROFIT'].apply(lambda x: 'Win' if x > 0 else 'Loss')
    
    fig = go.Figure()
    
    for result in ['Win', 'Loss']:
        data = df_copy[df_copy['Result'] == result]['Duration_Hours']
        fig.add_trace(go.Box(
            y=data,
            name=result,
            marker_color='green' if result == 'Win' else 'red'
        ))
    
    fig.update_layout(
        title='Position Holding Time Distribution',
        yaxis_title='Duration (Hours)',
        template='plotly_white',
        height=400
    )
    
    return fig

def plot_trader_profile_radar(
    profile_features: Dict[str, Any],
    classification: Dict[str, Any]
) -> go.Figure:
    """Plot 8-dimensional radar chart of trader characteristics"""
    
    # Define 8 dimensions
    dimensions = [
        'Capital Level',
        'Experience',
        'Risk Tolerance',
        'Time Commitment',
        'Discipline',
        'Performance',
        'Asset Focus',
        'Goals Alignment'
    ]
    
    # Map features to scores (0-10)
    capital_map = {'Small': 3, 'Medium': 6, 'Large': 9}
    exp_map = {'Newbie': 2, 'Beginner': 4, 'Intermediate': 7, 'Experienced': 10}
    risk_map = {'Conservative': 3, 'Moderate': 6, 'Aggressive': 9}
    time_map = {'Very Low': 2, 'Low': 4, 'Medium': 7, 'High': 10}
    
    scores = [
        capital_map.get(profile_features.get('capital_level', 'Medium'), 5),
        exp_map.get(profile_features.get('experience_level', 'Beginner'), 5),
        profile_features.get('risk_appetite_score', 5),
        time_map.get(profile_features.get('time_commitment', 'Medium'), 5),
        classification.get('behavior_summary', {}).get('discipline_score', 5),
        min(classification.get('behavior_summary', {}).get('win_rate', 50) / 10, 10),
        classification.get('preferred_assets', {}).get('diversity_score', 5),
        7  # Default goals alignment
    ]
    
    # Ensure 8 scores
    while len(scores) < 8:
        scores.append(5)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=dimensions,
        fill='toself',
        name='Your Profile',
        line_color='#1f77b4'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=True,
        title='Trader Profile: 8-Dimensional Analysis',
        height=500
    )
    
    return fig

def plot_daily_pnl(df: pd.DataFrame) -> go.Figure:
    """Plot daily P&L bar chart"""
    if 'CLOSE TIME' not in df.columns or 'PROFIT' not in df.columns:
        return go.Figure()
    
    df_copy = df.copy()
    df_copy['Date'] = df_copy['CLOSE TIME'].dt.date
    daily_pnl = df_copy.groupby('Date')['PROFIT'].sum().reset_index()
    
    colors = ['green' if x >= 0 else 'red' for x in daily_pnl['PROFIT']]
    
    fig = go.Figure(data=[
        go.Bar(
            x=daily_pnl['Date'],
            y=daily_pnl['PROFIT'],
            marker_color=colors
        )
    ])
    
    fig.update_layout(
        title='Daily Profit & Loss',
        xaxis_title='Date',
        yaxis_title='Daily P&L ($)',
        template='plotly_white',
        height=400
    )
    
    return fig

def create_metrics_cards(metrics: Dict[str, Any]) -> str:
    """Generate HTML for metrics cards"""
    total_pnl = metrics.get('total_pnl', 0)
    win_rate = metrics.get('win_rate', 0)
    total_trades = metrics.get('total_trades', 0)
    max_dd = metrics.get('max_drawdown', 0)
    
    pnl_color = "green" if total_pnl >= 0 else "red"
    win_color = "green" if win_rate >= 50 else "orange" if win_rate >= 40 else "red"
    dd_color = "green" if max_dd < 10 else "orange" if max_dd < 20 else "red"
    
    html = f"""
    <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 20px;">
        <div style="flex: 1; min-width: 200px; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">Total P&L</h3>
            <p style="margin: 10px 0 0 0; font-size: 32px; font-weight: bold; color: {pnl_color};">${total_pnl:,.2f}</p>
        </div>
        <div style="flex: 1; min-width: 200px; padding: 20px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 10px; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">Win Rate</h3>
            <p style="margin: 10px 0 0 0; font-size: 32px; font-weight: bold; color: {win_color};">{win_rate:.1f}%</p>
        </div>
        <div style="flex: 1; min-width: 200px; padding: 20px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 10px; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">Total Trades</h3>
            <p style="margin: 10px 0 0 0; font-size: 32px; font-weight: bold;">{total_trades}</p>
        </div>
        <div style="flex: 1; min-width: 200px; padding: 20px; background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); border-radius: 10px; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">Max Drawdown</h3>
            <p style="margin: 10px 0 0 0; font-size: 32px; font-weight: bold; color: {dd_color};">{max_dd:.1f}%</p>
        </div>
    </div>
    """
    
    return html
