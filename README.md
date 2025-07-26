# Stock Analysis Tool

A Python-based tool for analyzing stock market data, comparing multiple stocks, and forecasting future trends using machine learning techniques.

## Note
This project was originally programmed and hosted on Glitch (an online IDE). It has since been exported from Glitch and imported to Github.

## Features

- **Single Stock Analysis**: Analyze individual stocks with moving averages and volatility metrics
- **Stock Comparison**: Compare price trends of multiple stocks over a specified time period
- **Stock Forecasting**: Predict future stock prices using polynomial regression with configurable complexity
  - Includes confidence intervals based on historical volatility
  - Visual representation of forecasts with price ranges
  - Customizable forecast period and curve complexity

## Prerequisites

Python 3.7 or higher is required. The following Python packages are needed:

```bash
pip install pandas numpy matplotlib yfinance scikit-learn
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stock-analysis-tool.git
cd stock-analysis-tool
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv stock-env
source stock-env/bin/activate  # On Windows use: stock-env\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script:
```bash
python scripts/main.py
```

### Options

1. **Analyze a Single Stock**
   - Enter stock ticker (e.g., AAPL)
   - Specify date range
   - View price trends and moving averages

2. **Compare Multiple Stocks**
   - Enter multiple stock tickers separated by commas
   - Specify date range
   - Compare price trends on a single chart

3. **Forecast Stock Trends**
   - Enter stock ticker
   - Specify number of days to forecast
   - Choose polynomial degree (2-4) for curve complexity
   - View forecast with confidence intervals

## Project Structure

```
stock-analysis-tool/
├── scripts/
│   ├── __init__.py
│   ├── main.py          # Main application script
│   ├── analysis.py      # Analysis functions
│   └── visualization.py # Plotting functions
├── requirements.txt
└── README.md
```

## Example Usage

### Single Stock Analysis
```python
Enter stock ticker symbol (e.g., AAPL): AAPL
Enter start date (YYYY-MM-DD): 2023-01-01
Enter end date (YYYY-MM-DD): 2024-01-01
```

### Stock Comparison
```python
Enter stock tickers separated by commas (e.g., AAPL,MSFT,TSLA): AAPL,MSFT
Enter start date (YYYY-MM-DD): 2023-01-01
Enter end date (YYYY-MM-DD): 2024-01-01
```

### Stock Forecasting
```python
Enter stock ticker symbol (e.g., AAPL): AAPL
Enter number of days to forecast: 30
Enter polynomial degree (2-4, higher = more curve): 2
```

## Features in Detail

### Moving Average Analysis
- Calculates 10-day moving average
- Shows price trends and volatility

### Stock Comparison
- Visualizes multiple stocks on the same chart
- Normalizes prices for fair comparison
- Handles missing data and invalid tickers

### Stock Forecasting
- Uses polynomial regression for curve fitting
- Provides confidence intervals based on historical volatility
- Supports different degrees of polynomial fitting (2-4)
- Shows forecast range with upper and lower bounds

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Uses YFinance for stock data retrieval
- Built with scikit-learn for machine learning functionality
- Visualization powered by Matplotlib

## Disclaimer

This tool is for educational and research purposes only. Do not use it for actual investment decisions. Always consult with a qualified financial advisor before making investment decisions.
