from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from datetime import datetime, timedelta

# Add the scripts directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from analysis import generate_trade_signals, backtest_signals, calculate_rsi, calculate_bollinger_bands
from data_fetch import fetch_stock_data, fetch_multiple_stocks, get_sp500_tickers
from portfolio import Portfolio, create_portfolio_from_signals
import yfinance as yf
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze-stock', methods=['POST'])
def analyze_stock():
    """Analyze a single stock with technical indicators"""
    try:
        data = request.json
        ticker = data['ticker'].upper()
        start_date = data['startDate']
        end_date = data['endDate']
        
        # Fetch stock data
        stock_data = fetch_stock_data(ticker, start_date, end_date)
        
        # Generate technical indicators and signals
        stock_data = generate_trade_signals(stock_data)
        
        # Backtest the signals
        results = backtest_signals(stock_data)
        
        # Prepare chart data
        chart_data = {
            'dates': stock_data.index.strftime('%Y-%m-%d').tolist(),
            'prices': stock_data['Close'].tolist(),
            'rsi': stock_data.get('RSI_14', []).tolist(),
            'bb_upper': stock_data.get('Bollinger_Upper', []).tolist(),
            'bb_lower': stock_data.get('Bollinger_Lower', []).tolist(),
            'bb_mid': stock_data.get('Bollinger_Mid', []).tolist(),
            'volume': stock_data['Volume'].tolist(),
        }
        
        # Get recent signals
        recent_signals = []
        for idx, row in stock_data.tail(10).iterrows():
            recent_signals.append({
                'date': idx.strftime('%Y-%m-%d'),
                'signal': row['Signal'],
                'price': row['Close'],
                'rsi': row.get('RSI_14', None)
            })
        
        return jsonify({
            'ticker': ticker,
            'results': results,
            'chart_data': chart_data,
            'recent_signals': recent_signals
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/batch-analysis', methods=['POST'])
def batch_analysis():
    """Perform batch analysis on multiple stocks"""
    try:
        data = request.json
        analysis_type = data.get('analysisType', 'sp500')
        start_date = data['startDate']
        end_date = data['endDate']
        
        # Get tickers based on analysis type
        if analysis_type == 'sp500':
            tickers = get_sp500_tickers()[:100]  # Limit for demo
        elif analysis_type == 'custom':
            tickers = [t.strip().upper() for t in data['customTickers'].split(',')]
        else:
            tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA']  # Default
        
        # Fetch data for all stocks
        stock_data, failed_tickers = fetch_multiple_stocks(tickers, start_date, end_date)
        
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
                
            except Exception as e:
                print(f"Error analyzing {ticker}: {e}")
                continue
        
        # Calculate summary statistics
        if results_summary:
            returns = [r['total_return'] for r in results_summary]
            accuracies = [r['accuracy'] for r in results_summary if r['total_trades'] > 0]
            
            summary = {
                'total_stocks': len(tickers),
                'analyzed_stocks': len(results_summary),
                'average_return': sum(returns) / len(returns) if returns else 0,
                'average_accuracy': sum(accuracies) / len(accuracies) if accuracies else 0,
                'best_performer': max(results_summary, key=lambda x: x['total_return'])['ticker'] if results_summary else None,
                'worst_performer': min(results_summary, key=lambda x: x['total_return'])['ticker'] if results_summary else None,
                'results': results_summary
            }
        else:
            summary = {
                'total_stocks': len(tickers),
                'analyzed_stocks': 0,
                'average_return': 0,
                'average_accuracy': 0,
                'best_performer': None,
                'worst_performer': None,
                'results': []
            }
        
        return jsonify(summary)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/portfolio/create', methods=['POST'])
def create_portfolio():
    """Create a portfolio from trade signals"""
    try:
        data = request.json
        ticker = data['ticker'].upper()
        start_date = data['startDate']
        end_date = data['endDate']
        initial_capital = float(data['initialCapital'])
        
        # Fetch stock data
        stock_data = fetch_stock_data(ticker, start_date, end_date)
        
        # Generate signals
        stock_data = generate_trade_signals(stock_data)
        
        # Create portfolio
        portfolio = create_portfolio_from_signals(stock_data, ticker, initial_capital)
        
        # Get current price for performance calculation
        current_price = stock_data['Close'].iloc[-1]
        current_prices = {ticker: current_price}
        
        # Get performance metrics
        metrics = portfolio.get_performance_metrics(current_prices)
        
        # Save portfolio
        portfolio.save_portfolio()
        
        return jsonify({
            'portfolio_name': portfolio.name,
            'metrics': metrics,
            'trades': portfolio.trades
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/portfolio/<portfolio_name>', methods=['GET'])
def get_portfolio(portfolio_name):
    """Get portfolio data"""
    try:
        # Use absolute path relative to the project root
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        os.makedirs(data_dir, exist_ok=True)
        filename = os.path.join(data_dir, f"{portfolio_name}_portfolio.json")
        
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
        
        return jsonify({
            'portfolio': {
                'name': portfolio.name,
                'initial_capital': portfolio.initial_capital,
                'cash': portfolio.cash,
                'trades': portfolio.trades
            },
            'metrics': metrics,
            'positions': positions
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/portfolio/<portfolio_name>/trade', methods=['POST'])
def add_trade(portfolio_name):
    """Add a trade to a portfolio"""
    try:
        data = request.json
        # Use absolute path relative to the project root
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        os.makedirs(data_dir, exist_ok=True)
        filename = os.path.join(data_dir, f"{portfolio_name}_portfolio.json")
        
        portfolio = Portfolio()
        portfolio.load_portfolio(filename)
        
        portfolio.add_trade(
            data['ticker'],
            data['action'],
            float(data['shares']),
            float(data['price'])
        )
        
        portfolio.save_portfolio(filename)
        
        return jsonify({'message': 'Trade added successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000) 