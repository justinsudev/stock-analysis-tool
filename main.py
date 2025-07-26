import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.analysis import calculate_moving_average, calculate_volatility, compare_stocks, forecast_trend
from scripts.visualization import plot_stock_data, plot_stock_comparison, plot_forecast
import yfinance as yf

def analyze_single_stock():
    ticker = input("Enter stock ticker symbol (e.g., AAPL): ").upper()
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    try:
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        data = calculate_moving_average(data)
        data = calculate_volatility(data)

        print(data.head()) 
        plot_stock_data(data, ticker)
    except Exception as e:
        print(f"Error: {e}")

def compare_stocks_mode():
    tickers = [ticker.strip() for ticker in input("Enter stock tickers separated by commas (e.g., AAPL,MSFT,TSLA): ").split(",")]
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    try:
        comparison_df = compare_stocks(tickers, start_date, end_date)
        print("\nStock price comparison:")
        print(comparison_df.head())
        plot_stock_comparison(comparison_df, tickers)
    except Exception as e:
        print(f"Error: {e}")

def forecast_mode():
    """
    Enhanced forecast mode with polynomial regression
    """
    ticker = input("Enter stock ticker symbol (e.g., AAPL): ").upper()
    days_to_forecast = int(input("Enter number of days to forecast: "))
    degree = int(input("Enter polynomial degree (2-4, higher = more curve): "))
    
    degree = max(1, min(4, degree))  
    
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)  
        
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        
        if data.empty:
            raise ValueError(f"No data found for {ticker}")
        
        forecast, future_dates, upper_bound, lower_bound = forecast_trend(
            data, days_to_forecast, degree=degree
        )
        
        print(f"\nForecast for next {days_to_forecast} days:")
        for date, price, upper, lower in zip(future_dates, forecast, upper_bound, lower_bound):
            print(f"{date.strftime('%Y-%m-%d')}: ${price:.2f} (Range: ${lower:.2f} - ${upper:.2f})")
            
        plot_forecast(data, forecast, future_dates, upper_bound, lower_bound)
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("Welcome to the Stock Analysis Tool!")
    print("1. Analyze a Single Stock")
    print("2. Compare Multiple Stocks")
    print("3. Forecast Stock Trends")

    choice = input("Select an option (1, 2, or 3): ")
    if choice == "1":
        analyze_single_stock()
    elif choice == "2":
        compare_stocks_mode()
    elif choice == "3":
        forecast_mode()
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
