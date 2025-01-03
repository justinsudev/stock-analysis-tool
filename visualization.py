import matplotlib.pyplot as plt

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
    
    plt.plot(data.index, data['Close'], label='Historical', color='blue')
    
    plt.plot(future_dates, forecast, label='Forecast', color='red', linestyle='--')
    
    if upper_bound is not None and lower_bound is not None:
        plt.fill_between(future_dates, lower_bound, upper_bound, 
                        color='red', alpha=0.1, label='Confidence Interval')
    
    plt.title("Stock Price Forecast")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    
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
