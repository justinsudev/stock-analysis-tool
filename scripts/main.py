import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.analysis import calculate_moving_average, calculate_volatility, compare_stocks, forecast_trend, calculate_rsi, calculate_bollinger_bands, generate_trade_signals, backtest_signals
from scripts.visualization import plot_stock_data, plot_stock_comparison, plot_forecast
from scripts.data_fetch import fetch_stock_data, fetch_multiple_stocks, get_sp500_tickers
from scripts.portfolio import Portfolio, create_portfolio_from_signals
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

        print(data.head())  # Display data preview
        plot_stock_data(data, ticker)
    except Exception as e:
        print(f"Error: {e}")

def compare_stocks_mode():
    # Strip whitespace from tickers
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
    
    # Validate polynomial degree
    degree = max(1, min(4, degree))  # Limit between 1 and 4
    
    try:
        # Get historical data up to today
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)  # Use 1 year of historical data
        
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

def technical_analysis_mode():
    """
    New mode for technical analysis with RSI, Bollinger Bands, and trade signals
    """
    ticker = input("Enter stock ticker symbol (e.g., AAPL): ").upper()
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    try:
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        
        if data.empty:
            raise ValueError(f"No data found for {ticker}")
        
        # Generate technical indicators and signals
        data = generate_trade_signals(data)
        
        # Backtest the signals
        results = backtest_signals(data)
        
        print(f"\n=== Technical Analysis Results for {ticker} ===")
        print(f"Initial Capital: ${results['initial_capital']:,.2f}")
        print(f"Final Capital: ${results['final_capital']:,.2f}")
        print(f"Total Return: {results['total_return_pct']:.2f}%")
        print(f"Total Trades: {results['total_trades']}")
        print(f"Profitable Trades: {results['profitable_trades']}")
        print(f"Accuracy: {results['accuracy_pct']:.2f}%")
        
        # Show recent signals
        recent_data = data.tail(10)
        print(f"\nRecent Signals (Last 10 days):")
        for idx, row in recent_data.iterrows():
            signal = row['Signal']
            price = row['Close']
            rsi = row.get('RSI_14', 'N/A')
            print(f"{idx.strftime('%Y-%m-%d')}: {signal} at ${price:.2f} (RSI: {rsi:.1f if rsi != 'N/A' else 'N/A'})")
        
        # Create interactive Plotly charts
        from scripts.visualization import plot_technical_indicators_plotly, plot_portfolio_performance_plotly
        
        # Technical indicators chart
        tech_fig = plot_technical_indicators_plotly(data, ticker)
        tech_fig.write_html(f"data/{ticker}_technical_analysis.html")
        print(f"\nTechnical analysis chart saved as: data/{ticker}_technical_analysis.html")
        
        # Portfolio performance chart
        if results['trades']:
            portfolio_fig = plot_portfolio_performance_plotly(
                results['equity_curve'], results['trades'], results['initial_capital']
            )
            portfolio_fig.write_html(f"data/{ticker}_portfolio_performance.html")
            print(f"Portfolio performance chart saved as: data/{ticker}_portfolio_performance.html")
        
    except Exception as e:
        print(f"Error: {e}")

def batch_analysis_mode():
    """
    New mode for batch analysis of multiple stocks
    """
    print("Batch Analysis Mode")
    print("1. Analyze S&P 500 stocks")
    print("2. Analyze custom list of stocks")
    
    choice = input("Select option (1 or 2): ")
    
    if choice == "1":
        tickers = get_sp500_tickers()
        print(f"Analyzing {len(tickers)} S&P 500 stocks...")
    elif choice == "2":
        ticker_input = input("Enter stock tickers separated by commas: ")
        tickers = [ticker.strip().upper() for ticker in ticker_input.split(",")]
    else:
        print("Invalid choice")
        return
    
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    
    try:
        # Fetch data for all stocks
        stock_data, failed_tickers = fetch_multiple_stocks(tickers, start_date, end_date)
        
        if not stock_data:
            print("No data fetched successfully")
            return
        
        print(f"\nAnalyzing {len(stock_data)} stocks...")
        
        # Analyze each stock
        results_summary = []
        for ticker, data in stock_data.items():
            try:
                # Generate signals and backtest
                data_with_signals = generate_trade_signals(data)
                backtest_result = backtest_signals(data_with_signals)
                
                results_summary.append({
                    'ticker': ticker,
                    'total_return': backtest_result['total_return_pct'],
                    'accuracy': backtest_result['accuracy_pct'],
                    'total_trades': backtest_result['total_trades'],
                    'final_capital': backtest_result['final_capital']
                })
                
                print(f"{ticker}: {backtest_result['total_return_pct']:.2f}% return, {backtest_result['accuracy_pct']:.2f}% accuracy")
                
            except Exception as e:
                print(f"Error analyzing {ticker}: {e}")
                continue
        
        # Summary statistics
        if results_summary:
            returns = [r['total_return'] for r in results_summary]
            accuracies = [r['accuracy'] for r in results_summary if r['total_trades'] > 0]
            
            print(f"\n=== Batch Analysis Summary ===")
            print(f"Stocks analyzed: {len(results_summary)}")
            print(f"Average return: {sum(returns)/len(returns):.2f}%")
            print(f"Average accuracy: {sum(accuracies)/len(accuracies):.2f}%" if accuracies else "No trades executed")
            print(f"Best performer: {max(results_summary, key=lambda x: x['total_return'])['ticker']}")
            print(f"Worst performer: {min(results_summary, key=lambda x: x['total_return'])['ticker']}")
            
            # Create interactive Plotly chart for batch results
            from scripts.visualization import plot_batch_analysis_results_plotly
            batch_fig = plot_batch_analysis_results_plotly(results_summary)
            batch_fig.write_html("data/batch_analysis_results.html")
            print(f"\nBatch analysis results chart saved as: data/batch_analysis_results.html")
        
    except Exception as e:
        print(f"Error: {e}")

def portfolio_management_mode():
    """
    New mode for portfolio management
    """
    print("Portfolio Management Mode")
    print("1. Create portfolio from trade signals")
    print("2. View existing portfolio")
    print("3. Add manual trade")
    print("4. Portfolio performance analysis")
    
    choice = input("Select option (1-4): ")
    
    if choice == "1":
        # Create portfolio from signals
        ticker = input("Enter stock ticker symbol: ").upper()
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        initial_capital = float(input("Enter initial capital: "))
        
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(start=start_date, end=end_date)
            
            if data.empty:
                raise ValueError(f"No data found for {ticker}")
            
            # Generate signals
            data = generate_trade_signals(data)
            
            # Create portfolio
            portfolio = create_portfolio_from_signals(data, ticker, initial_capital)
            
            # Get current price for performance calculation
            current_price = data['Close'].iloc[-1]
            current_prices = {ticker: current_price}
            
            # Get performance metrics
            metrics = portfolio.get_performance_metrics(current_prices)
            
            print(f"\n=== Portfolio Created ===")
            print(f"Portfolio Name: {portfolio.name}")
            print(f"Initial Capital: ${metrics['initial_capital']:,.2f}")
            print(f"Current Value: ${metrics['current_value']:,.2f}")
            print(f"Total Return: {metrics['total_return_pct']:.2f}%")
            print(f"Total Trades: {metrics['total_trades']}")
            print(f"Accuracy: {metrics['accuracy_pct']:.2f}%")
            print(f"Cash: ${metrics['cash']:,.2f}")
            
            # Save portfolio
            portfolio.save_portfolio()
            print(f"Portfolio saved as: data/{portfolio.name}_portfolio.json")
            
        except Exception as e:
            print(f"Error: {e}")
    
    elif choice == "2":
        # View existing portfolio
        portfolio_name = input("Enter portfolio name (without _portfolio.json): ")
        filename = f"data/{portfolio_name}_portfolio.json"
        
        try:
            portfolio = Portfolio()
            portfolio.load_portfolio(filename)
            
            print(f"\n=== Portfolio: {portfolio.name} ===")
            print(f"Initial Capital: ${portfolio.initial_capital:,.2f}")
            print(f"Cash: ${portfolio.cash:,.2f}")
            print(f"Total Trades: {len(portfolio.trades)}")
            
            if portfolio.positions:
                print(f"\nCurrent Positions:")
                for ticker, position in portfolio.positions.items():
                    print(f"  {ticker}: {position['shares']:.2f} shares @ ${position['avg_price']:.2f}")
            
        except Exception as e:
            print(f"Error: {e}")
    
    elif choice == "3":
        # Add manual trade
        portfolio_name = input("Enter portfolio name (without _portfolio.json): ")
        filename = f"data/{portfolio_name}_portfolio.json"
        
        try:
            portfolio = Portfolio()
            portfolio.load_portfolio(filename)
            
            ticker = input("Enter ticker symbol: ").upper()
            action = input("Enter action (buy/sell): ").lower()
            shares = float(input("Enter number of shares: "))
            price = float(input("Enter price per share: "))
            
            portfolio.add_trade(ticker, action, shares, price)
            portfolio.save_portfolio(filename)
            
            print("Trade added successfully!")
            
        except Exception as e:
            print(f"Error: {e}")
    
    elif choice == "4":
        # Portfolio performance analysis
        portfolio_name = input("Enter portfolio name (without _portfolio.json): ")
        filename = f"data/{portfolio_name}_portfolio.json"
        
        try:
            portfolio = Portfolio()
            portfolio.load_portfolio(filename)
            
            # Get current prices for all positions
            current_prices = {}
            for ticker in portfolio.positions.keys():
                try:
                    stock = yf.Ticker(ticker)
                    current_price = stock.info.get('regularMarketPrice', 0)
                    current_prices[ticker] = current_price
                except:
                    current_prices[ticker] = 0
            
            metrics = portfolio.get_performance_metrics(current_prices)
            positions = portfolio.get_position_summary(current_prices)
            
            print(f"\n=== Portfolio Performance ===")
            print(f"Portfolio: {portfolio.name}")
            print(f"Initial Capital: ${metrics['initial_capital']:,.2f}")
            print(f"Current Value: ${metrics['current_value']:,.2f}")
            print(f"Total Return: {metrics['total_return_pct']:.2f}%")
            print(f"Cash: ${metrics['cash']:,.2f}")
            
            if positions:
                print(f"\nCurrent Positions:")
                for pos in positions:
                    print(f"  {pos['ticker']}: {pos['shares']:.2f} shares")
                    print(f"    Avg Price: ${pos['avg_price']:.2f}")
                    print(f"    Current Price: ${pos['current_price']:.2f}")
                    print(f"    Market Value: ${pos['market_value']:,.2f}")
                    print(f"    Unrealized P&L: ${pos['unrealized_pnl']:,.2f} ({pos['unrealized_pnl_pct']:.2f}%)")
            
        except Exception as e:
            print(f"Error: {e}")
    
    else:
        print("Invalid choice")

def main():
    print("Welcome to the Stock Analysis Tool!")
    print("1. Analyze a Single Stock")
    print("2. Compare Multiple Stocks")
    print("3. Forecast Stock Trends")
    print("4. Technical Analysis with Signals")
    print("5. Batch Analysis (Multiple Stocks)")
    print("6. Portfolio Management")

    choice = input("Select an option (1-6): ")
    if choice == "1":
        analyze_single_stock()
    elif choice == "2":
        compare_stocks_mode()
    elif choice == "3":
        forecast_mode()
    elif choice == "4":
        technical_analysis_mode()
    elif choice == "5":
        batch_analysis_mode()
    elif choice == "6":
        portfolio_management_mode()
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()