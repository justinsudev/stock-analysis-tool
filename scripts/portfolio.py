import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class Portfolio:
    """
    Portfolio management class for tracking positions, trades, and performance
    """
    
    def __init__(self, initial_capital=10000, name="Default Portfolio"):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.name = name
        self.positions = {}  # {ticker: {'shares': float, 'avg_price': float}}
        self.trades = []     # List of trade dictionaries
        self.cash = initial_capital
        self.portfolio_history = []
        
    def add_trade(self, ticker, action, shares, price, date=None):
        """
        Add a trade to the portfolio
        action: 'buy' or 'sell'
        """
        if date is None:
            date = datetime.now()
            
        trade = {
            'date': date,
            'ticker': ticker,
            'action': action,
            'shares': shares,
            'price': price,
            'value': shares * price
        }
        
        if action.lower() == 'buy':
            # Update cash
            self.cash -= trade['value']
            
            # Update position
            if ticker in self.positions:
                # Add to existing position
                total_shares = self.positions[ticker]['shares'] + shares
                total_cost = (self.positions[ticker]['shares'] * self.positions[ticker]['avg_price'] + 
                            shares * price)
                self.positions[ticker] = {
                    'shares': total_shares,
                    'avg_price': total_cost / total_shares
                }
            else:
                # New position
                self.positions[ticker] = {
                    'shares': shares,
                    'avg_price': price
                }
                
        elif action.lower() == 'sell':
            # Update cash
            self.cash += trade['value']
            
            # Update position
            if ticker in self.positions:
                self.positions[ticker]['shares'] -= shares
                if self.positions[ticker]['shares'] <= 0:
                    del self.positions[ticker]
                    
        self.trades.append(trade)
        self._update_portfolio_value()
        
    def get_portfolio_value(self, current_prices):
        """
        Calculate current portfolio value based on current prices
        current_prices: dict of {ticker: current_price}
        """
        total_value = self.cash
        
        for ticker, position in self.positions.items():
            if ticker in current_prices:
                total_value += position['shares'] * current_prices[ticker]
                
        return total_value
    
    def _update_portfolio_value(self):
        """
        Update portfolio history
        """
        # This would be called with current market prices in a real implementation
        pass
    
    def get_performance_metrics(self, current_prices):
        """
        Calculate portfolio performance metrics
        """
        current_value = self.get_portfolio_value(current_prices)
        total_return = (current_value - self.initial_capital) / self.initial_capital * 100
        
        # Calculate trade statistics
        buy_trades = [t for t in self.trades if t['action'].lower() == 'buy']
        sell_trades = [t for t in self.trades if t['action'].lower() == 'sell']
        
        profitable_trades = 0
        total_trades = min(len(buy_trades), len(sell_trades))
        
        for i in range(total_trades):
            if sell_trades[i]['price'] > buy_trades[i]['price']:
                profitable_trades += 1
        
        accuracy = (profitable_trades / total_trades * 100) if total_trades > 0 else 0
        
        return {
            'initial_capital': self.initial_capital,
            'current_value': current_value,
            'total_return_pct': total_return,
            'total_trades': total_trades,
            'profitable_trades': profitable_trades,
            'accuracy_pct': accuracy,
            'cash': self.cash,
            'positions': self.positions
        }
    
    def get_position_summary(self, current_prices):
        """
        Get summary of current positions
        """
        summary = []
        
        for ticker, position in self.positions.items():
            current_price = current_prices.get(ticker, 0)
            market_value = position['shares'] * current_price
            unrealized_pnl = market_value - (position['shares'] * position['avg_price'])
            unrealized_pnl_pct = (unrealized_pnl / (position['shares'] * position['avg_price'])) * 100 if position['avg_price'] > 0 else 0
            
            summary.append({
                'ticker': ticker,
                'shares': position['shares'],
                'avg_price': position['avg_price'],
                'current_price': current_price,
                'market_value': market_value,
                'unrealized_pnl': unrealized_pnl,
                'unrealized_pnl_pct': unrealized_pnl_pct
            })
            
        return summary
    
    def save_portfolio(self, filename=None):
        """
        Save portfolio data to JSON file
        """
        if filename is None:
            # Create absolute path to data directory
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            data_dir = os.path.join(project_root, 'data')
            filename = os.path.join(data_dir, f"{self.name}_portfolio.json")
            
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        data = {
            'name': self.name,
            'initial_capital': self.initial_capital,
            'cash': self.cash,
            'positions': self.positions,
            'trades': self.trades
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
            
    def load_portfolio(self, filename):
        """
        Load portfolio data from JSON file
        """
        with open(filename, 'r') as f:
            data = json.load(f)
            
        self.name = data['name']
        self.initial_capital = data['initial_capital']
        self.cash = data['cash']
        self.positions = data['positions']
        self.trades = data['trades']
        
        # Convert date strings back to datetime objects
        for trade in self.trades:
            if isinstance(trade['date'], str):
                trade['date'] = datetime.fromisoformat(trade['date'].replace('Z', '+00:00'))

def create_portfolio_from_signals(data, ticker, initial_capital=10000):
    """
    Create a portfolio based on trade signals from analysis
    """
    portfolio = Portfolio(initial_capital=initial_capital, name=f"{ticker}_Portfolio")
    
    position = 0
    shares = 0
    
    for idx, row in data.iterrows():
        signal = row['Signal']
        price = row['Close']
        
        if signal == 'Buy' and position == 0:
            # Buy signal when not in position - use available cash
            shares = portfolio.cash / price
            if shares > 0:  # Only trade if we have enough cash
                portfolio.add_trade(ticker, 'buy', shares, price, idx)
                position = 1
            
        elif signal == 'Sell' and position == 1:
            # Sell signal when in position - sell all shares
            if shares > 0:
                portfolio.add_trade(ticker, 'sell', shares, price, idx)
                position = 0
                shares = 0
    
    return portfolio 