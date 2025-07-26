import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

def plot_stock_data(data, ticker):
    """
    Plot the stock's closing price and moving average.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data['Close'], label='Close Price', color='blue')
    if '10-day MA' in data.columns:
        plt.plot(data.index, data['10-day MA'], label='10-day MA', color='orange')
    plt.title(f"{ticker} Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()
    plt.show()

def plot_stock_comparison(comparison_df, tickers):
    """
    Plot the comparison of multiple stocks.
    """
    plt.figure(figsize=(12, 6))
    comparison_df.plot(figsize=(12, 6), title="Stock Comparison")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend(tickers)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_forecast(data, forecast, future_dates, upper_bound=None, lower_bound=None):
    """
    Plot historical data and curved forecast with confidence bands
    """
    plt.figure(figsize=(12, 6))
    
    # Plot historical data
    plt.plot(data.index, data['Close'], label='Historical', color='blue')
    
    # Plot forecast
    plt.plot(future_dates, forecast, label='Forecast', color='red', linestyle='--')
    
    # Plot confidence bands if available
    if upper_bound is not None and lower_bound is not None:
        plt.fill_between(future_dates, lower_bound, upper_bound, 
                        color='red', alpha=0.1, label='Confidence Interval')
    
    plt.title("Stock Price Forecast")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    
    # Add last known price and forecasted final price annotations
    last_known_price = data['Close'].iloc[-1]
    final_forecast_price = forecast[-1]
    
    plt.annotate(f'Last Known: ${last_known_price:.2f}', 
                xy=(data.index[-1], last_known_price),
                xytext=(10, 10), textcoords='offset points')
    
    plt.annotate(f'Final Forecast: ${final_forecast_price:.2f}', 
                xy=(future_dates[-1], final_forecast_price),
                xytext=(10, -10), textcoords='offset points')
    
    plt.tight_layout()
    plt.show()

def plot_technical_indicators_plotly(data, ticker):
    """
    Create an interactive Plotly chart with price, RSI, and Bollinger Bands
    """
    # Create subplots
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=(f'{ticker} Price & Bollinger Bands', 'RSI', 'Volume'),
        row_heights=[0.6, 0.2, 0.2]
    )
    
    # Price and Bollinger Bands
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Close'], name='Close Price', line=dict(color='blue')),
        row=1, col=1
    )
    
    if 'Bollinger_Upper' in data.columns:
        fig.add_trace(
            go.Scatter(x=data.index, y=data['Bollinger_Upper'], name='Upper Band', 
                      line=dict(color='red', dash='dash')),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=data.index, y=data['Bollinger_Lower'], name='Lower Band', 
                      line=dict(color='red', dash='dash'), fill='tonexty'),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=data.index, y=data['Bollinger_Mid'], name='Middle Band', 
                      line=dict(color='orange')),
            row=1, col=1
        )
    
    # RSI
    if 'RSI_14' in data.columns:
        fig.add_trace(
            go.Scatter(x=data.index, y=data['RSI_14'], name='RSI', line=dict(color='purple')),
            row=2, col=1
        )
        # Add overbought/oversold lines
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
    
    # Volume
    fig.add_trace(
        go.Bar(x=data.index, y=data['Volume'], name='Volume', marker_color='lightblue'),
        row=3, col=1
    )
    
    # Add buy/sell signals if available
    if 'Signal' in data.columns:
        buy_signals = data[data['Signal'] == 'Buy']
        sell_signals = data[data['Signal'] == 'Sell']
        
        if not buy_signals.empty:
            fig.add_trace(
                go.Scatter(x=buy_signals.index, y=buy_signals['Close'], 
                          mode='markers', name='Buy Signal', 
                          marker=dict(color='green', size=10, symbol='triangle-up')),
                row=1, col=1
            )
        
        if not sell_signals.empty:
            fig.add_trace(
                go.Scatter(x=sell_signals.index, y=sell_signals['Close'], 
                          mode='markers', name='Sell Signal', 
                          marker=dict(color='red', size=10, symbol='triangle-down')),
                row=1, col=1
            )
    
    fig.update_layout(
        title=f'{ticker} Technical Analysis',
        xaxis_rangeslider_visible=False,
        height=800
    )
    
    return fig

def plot_portfolio_performance_plotly(equity_curve, trades, initial_capital):
    """
    Create an interactive Plotly chart showing portfolio performance
    """
    # Create equity curve DataFrame
    equity_df = pd.DataFrame({
        'Date': range(len(equity_curve)),
        'Equity': equity_curve
    })
    
    fig = go.Figure()
    
    # Plot equity curve
    fig.add_trace(
        go.Scatter(x=equity_df['Date'], y=equity_df['Equity'], 
                  name='Portfolio Value', line=dict(color='blue'))
    )
    
    # Add buy/sell markers
    buy_trades = [t for t in trades if t['action'] == 'Buy']
    sell_trades = [t for t in trades if t['action'] == 'Sell']
    
    if buy_trades:
        buy_dates = [i for i, t in enumerate(trades) if t['action'] == 'Buy']
        buy_values = [equity_curve[i] for i in buy_dates]
        fig.add_trace(
            go.Scatter(x=buy_dates, y=buy_values, mode='markers', 
                      name='Buy', marker=dict(color='green', size=10, symbol='triangle-up'))
        )
    
    if sell_trades:
        sell_dates = [i for i, t in enumerate(trades) if t['action'] == 'Sell']
        sell_values = [equity_curve[i] for i in sell_dates]
        fig.add_trace(
            go.Scatter(x=sell_dates, y=sell_values, mode='markers', 
                      name='Sell', marker=dict(color='red', size=10, symbol='triangle-down'))
        )
    
    # Add initial capital line
    fig.add_hline(y=initial_capital, line_dash="dash", line_color="gray", 
                  annotation_text="Initial Capital")
    
    fig.update_layout(
        title='Portfolio Performance',
        xaxis_title='Trading Days',
        yaxis_title='Portfolio Value ($)',
        height=600
    )
    
    return fig

def plot_batch_analysis_results_plotly(results_summary):
    """
    Create interactive Plotly charts for batch analysis results
    """
    df = pd.DataFrame(results_summary)
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Returns Distribution', 'Accuracy vs Returns', 
                       'Top Performers', 'Trade Count Distribution'),
        specs=[[{"type": "histogram"}, {"type": "scatter"}],
               [{"type": "bar"}, {"type": "histogram"}]]
    )
    
    # Returns distribution
    fig.add_trace(
        go.Histogram(x=df['total_return'], name='Returns', nbinsx=20),
        row=1, col=1
    )
    
    # Accuracy vs Returns scatter
    fig.add_trace(
        go.Scatter(x=df['accuracy'], y=df['total_return'], mode='markers',
                  text=df['ticker'], name='Stocks'),
        row=1, col=2
    )
    
    # Top performers
    top_performers = df.nlargest(10, 'total_return')
    fig.add_trace(
        go.Bar(x=top_performers['ticker'], y=top_performers['total_return'],
               name='Top Returns'),
        row=2, col=1
    )
    
    # Trade count distribution
    fig.add_trace(
        go.Histogram(x=df['total_trades'], name='Trade Count', nbinsx=20),
        row=2, col=2
    )
    
    fig.update_layout(
        title='Batch Analysis Results',
        height=800,
        showlegend=False
    )
    
    return fig