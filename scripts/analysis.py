import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

def calculate_moving_average(data, window=10):
    """
    Calculate the moving average for the stock's closing price.
    """
    data[f'{window}-day MA'] = data['Close'].rolling(window=window).mean()
    return data

def calculate_volatility(data):
    """
    Calculate daily percentage change as a measure of volatility.
    """
    data['Daily Change %'] = data['Close'].pct_change() * 100
    return data

def compare_stocks(tickers, start_date, end_date):
    """
    Compare stocks with improved error handling
    """
    data = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            stock_data = stock.history(start=start_date, end=end_date)
            if stock_data.empty:
                print(f"Warning: No data found for {ticker}")
                continue
            data[ticker] = stock_data['Close']
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            continue
    
    if not data:
        raise ValueError("No valid data found for any of the provided tickers")
    
    comparison_df = pd.DataFrame(data)
    return comparison_df

def forecast_trend(data, days_to_forecast, degree=2):
    """
    Forecast stock price trends using polynomial regression
    
    Parameters:
    data: DataFrame with stock data
    days_to_forecast: int, number of days to forecast
    degree: int, degree of polynomial (2 for quadratic, 3 for cubic, etc.)
    """
    # Prepare training data
    X = np.arange(len(data)).reshape(-1, 1)
    y = data['Close'].values
    
    # Create polynomial regression model
    model = make_pipeline(
        PolynomialFeatures(degree, include_bias=False),
        LinearRegression()
    )
    
    # Fit model
    model.fit(X, y)
    
    # Generate future dates
    last_date = data.index[-1]
    future_dates = [last_date + timedelta(days=x+1) for x in range(days_to_forecast)]
    
    # Predict future values
    future_X = np.arange(len(data), len(data) + days_to_forecast).reshape(-1, 1)
    forecast = model.predict(future_X)
    
    # Calculate confidence bands (based on historical volatility)
    volatility = data['Close'].pct_change().std()
    confidence_interval = y[-1] * volatility * np.sqrt(np.arange(1, days_to_forecast + 1))
    upper_bound = forecast + confidence_interval
    lower_bound = forecast - confidence_interval
    
    return forecast, future_dates, upper_bound, lower_bound

def calculate_rsi(data, window=14):
    """
    Calculate the Relative Strength Index (RSI) for the stock's closing price.
    """
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    data[f'RSI_{window}'] = 100 - (100 / (1 + rs))
    return data

def calculate_bollinger_bands(data, window=20, num_std=2):
    """
    Calculate Bollinger Bands for the stock's closing price.
    """
    rolling_mean = data['Close'].rolling(window=window).mean()
    rolling_std = data['Close'].rolling(window=window).std()
    data['Bollinger_Mid'] = rolling_mean
    data['Bollinger_Upper'] = rolling_mean + (rolling_std * num_std)
    data['Bollinger_Lower'] = rolling_mean - (rolling_std * num_std)
    return data

def generate_trade_signals(data, rsi_window=14, bb_window=20, bb_num_std=2):
    """
    Generate trade signals based on RSI and Bollinger Bands.
    Returns a DataFrame with a new 'Signal' column: 'Buy', 'Sell', or 'Hold'.
    """
    data = calculate_rsi(data, window=rsi_window)
    data = calculate_bollinger_bands(data, window=bb_window, num_std=bb_num_std)
    signals = []
    for idx, row in data.iterrows():
        rsi = row.get(f'RSI_{rsi_window}', None)
        close = row['Close']
        upper = row.get('Bollinger_Upper', None)
        lower = row.get('Bollinger_Lower', None)
        signal = 'Hold'
        if rsi is not None and rsi < 30:
            signal = 'Buy'
        elif rsi is not None and rsi > 70:
            signal = 'Sell'
        elif upper is not None and close > upper:
            signal = 'Sell'
        elif lower is not None and close < lower:
            signal = 'Buy'
        signals.append(signal)
    data['Signal'] = signals
    return data

def backtest_signals(data, initial_capital=10000):
    """
    Backtest trade signals to evaluate accuracy and returns.
    Returns a dictionary with performance metrics.
    """
    if 'Signal' not in data.columns:
        data = generate_trade_signals(data)
    
    # Initialize tracking variables
    position = 0  # 0 = no position, 1 = long position
    capital = initial_capital
    shares = 0
    trades = []
    equity_curve = []
    
    for idx, row in data.iterrows():
        signal = row['Signal']
        price = row['Close']
        
        # Execute trades based on signals
        if signal == 'Buy' and position == 0:
            # Buy signal when not in position
            shares = capital / price
            capital = 0
            position = 1
            trades.append({
                'date': idx,
                'action': 'Buy',
                'price': price,
                'shares': shares
            })
        elif signal == 'Sell' and position == 1:
            # Sell signal when in position
            capital = shares * price
            shares = 0
            position = 0
            trades.append({
                'date': idx,
                'action': 'Sell',
                'price': price,
                'capital': capital
            })
        
        # Calculate current equity
        current_equity = capital + (shares * price)
        equity_curve.append(current_equity)
    
    # Calculate final capital if still in position
    if position == 1:
        final_price = data['Close'].iloc[-1]
        capital = shares * final_price
    
    # Calculate performance metrics
    total_return = (capital - initial_capital) / initial_capital * 100
    buy_trades = [t for t in trades if t['action'] == 'Buy']
    sell_trades = [t for t in trades if t['action'] == 'Sell']
    
    # Calculate accuracy (profitable trades / total trades)
    profitable_trades = 0
    total_trades = min(len(buy_trades), len(sell_trades))
    
    for i in range(total_trades):
        buy_price = buy_trades[i]['price']
        sell_price = sell_trades[i]['price']
        if sell_price > buy_price:
            profitable_trades += 1
    
    accuracy = (profitable_trades / total_trades * 100) if total_trades > 0 else 0
    
    return {
        'initial_capital': initial_capital,
        'final_capital': capital,
        'total_return_pct': total_return,
        'total_trades': total_trades,
        'profitable_trades': profitable_trades,
        'accuracy_pct': accuracy,
        'trades': trades,
        'equity_curve': equity_curve
    }