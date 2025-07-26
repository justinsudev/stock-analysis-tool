import yfinance as yf
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def fetch_stock_data(ticker, start_date, end_date):
    """
    Fetch historical stock data for a given ticker and date range.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    if data.empty:
        raise ValueError("No data found. Check the ticker or date range.")
    return data

def fetch_multiple_stocks(tickers, start_date, end_date, max_workers=10):
    """
    Fetch data for multiple stocks efficiently using parallel processing.
    Returns a dictionary with ticker as key and DataFrame as value.
    """
    results = {}
    failed_tickers = []
    
    def fetch_single_stock(ticker):
        try:
            data = fetch_stock_data(ticker, start_date, end_date)
            return ticker, data
        except Exception as e:
            return ticker, None
    
    print(f"Fetching data for {len(tickers)} stocks...")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ticker = {executor.submit(fetch_single_stock, ticker): ticker for ticker in tickers}
        
        for future in as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                ticker, data = future.result()
                if data is not None:
                    results[ticker] = data
                else:
                    failed_tickers.append(ticker)
            except Exception as e:
                failed_tickers.append(ticker)
    
    elapsed_time = time.time() - start_time
    print(f"Completed in {elapsed_time:.2f} seconds")
    print(f"Successfully fetched: {len(results)} stocks")
    print(f"Failed: {len(failed_tickers)} stocks")
    
    return results, failed_tickers

def get_sp500_tickers():
    """
    Get S&P 500 tickers for testing batch analysis.
    Returns a list of ticker symbols.
    """
    # This is a sample list - in production you'd fetch from a reliable source
    sp500_tickers = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'JPM', 'JNJ',
        'V', 'PG', 'UNH', 'HD', 'MA', 'DIS', 'PYPL', 'BAC', 'ADBE', 'CRM',
        'KO', 'PFE', 'ABT', 'TMO', 'AVGO', 'COST', 'PEP', 'ABBV', 'MRK', 'TXN',
        'LLY', 'ACN', 'DHR', 'NEE', 'VZ', 'CMCSA', 'ADP', 'BMY', 'PM', 'RTX',
        'QCOM', 'T', 'UNP', 'LOW', 'SPGI', 'INTU', 'ISRG', 'UPS', 'GILD', 'CAT',
        'AMGN', 'MS', 'BLK', 'GS', 'AXP', 'DE', 'PLD', 'SCHW', 'AMT', 'ADI',
        'TJX', 'MDLZ', 'GE', 'DUK', 'SO', 'NOC', 'EOG', 'AON', 'SLB', 'CME',
        'ITW', 'USB', 'PGR', 'ZTS', 'HON', 'TGT', 'MMC', 'ETN', 'ICE', 'SHW',
        'BDX', 'CI', 'APD', 'KLAC', 'FISV', 'AIG', 'SRE', 'VRTX', 'CTAS', 'BIIB',
        'HUM', 'AEP', 'NSC', 'TRV', 'PSA', 'ALL', 'ALGN', 'PAYX', 'ROST', 'MCD',
        'ORLY', 'IDXX', 'BLL', 'ADSK', 'WBA', 'ILMN', 'A', 'ADI', 'BKNG', 'CDW',
        'CHTR', 'CMI', 'COO', 'CPRT', 'CTSH', 'DAL', 'DOV', 'EA', 'EBAY', 'EFX',
        'ES', 'ETSY', 'EXC', 'EXPD', 'FAST', 'FB', 'FDX', 'FIS', 'FLT', 'FTNT',
        'GD', 'GPN', 'GRMN', 'HAS', 'HCA', 'HES', 'HIG', 'HLT', 'HOLX', 'HPQ',
        'HSIC', 'HWM', 'IBM', 'INCY', 'INFO', 'IP', 'IPG', 'IQV', 'IR', 'ISRG',
        'JBHT', 'JKHY', 'JNPR', 'KEY', 'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX',
        'KO', 'KR', 'L', 'LH', 'LKQ', 'LLY', 'LMT', 'LNT', 'LOW', 'LRCX', 'LUMN',
        'LUV', 'LW', 'LYB', 'LYV', 'MA', 'MAA', 'MAR', 'MAS', 'MCD', 'MCK', 'MDLZ',
        'MET', 'MGM', 'MHK', 'MKC', 'MLM', 'MMC', 'MMM', 'MNST', 'MO', 'MOS',
        'MPC', 'MRK', 'MRNA', 'MS', 'MSFT', 'MTB', 'MTCH', 'MTD', 'MU', 'NCLH',
        'NDAQ', 'NDSN', 'NEE', 'NFLX', 'NI', 'NOC', 'NOV', 'NRG', 'NSC', 'NTAP',
        'NTRS', 'NUE', 'NVDA', 'NVR', 'NWL', 'NWS', 'NWSA', 'NXPI', 'O', 'ODFL',
        'OKE', 'OMC', 'ORCL', 'ORLY', 'OTIS', 'OXY', 'PAYC', 'PAYX', 'PCAR', 'PCG',
        'PEAK', 'PEG', 'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKG',
        'PLD', 'PM', 'PNC', 'PNR', 'POOL', 'PPG', 'PPL', 'PRU', 'PSA', 'PSX',
        'PTC', 'PVH', 'PWR', 'PXD', 'PYPL', 'QCOM', 'QRVO', 'RCL', 'RE', 'REG',
        'RF', 'RHI', 'RJF', 'RL', 'RMD', 'ROK', 'ROL', 'ROP', 'ROST', 'RSG',
        'RTX', 'SBAC', 'SBNY', 'SBUX', 'SCHW', 'SEDG', 'SEE', 'SHW', 'SIVB', 'SJM',
        'SLB', 'SNA', 'SNPS', 'SO', 'SPG', 'SRE', 'STE', 'STT', 'STX', 'STZ',
        'SWK', 'SWKS', 'SYF', 'SYK', 'SYY', 'T', 'TAP', 'TDG', 'TDY', 'TECH',
        'TEL', 'TER', 'TFC', 'TFX', 'TGT', 'TMO', 'TMUS', 'TPR', 'TRMB', 'TROW',
        'TRV', 'TSCO', 'TSLA', 'TSN', 'TT', 'TTC', 'TTWO', 'TXN', 'TXT', 'TYL',
        'UAL', 'UDR', 'UHS', 'ULTA', 'UNH', 'UNP', 'UPS', 'URI', 'USB', 'V',
        'VFC', 'VIAC', 'VLO', 'VMC', 'VNO', 'VNT', 'VRSK', 'VRSN', 'VRTX', 'VTR',
        'VTRS', 'VZ', 'WAB', 'WAT', 'WBA', 'WDC', 'WEC', 'WELL', 'WFC', 'WHR',
        'WM', 'WMB', 'WMT', 'WRB', 'WRK', 'WST', 'WTW', 'WY', 'WYNN', 'XEL',
        'XLNX', 'XOM', 'XRAY', 'XYL', 'YUM', 'ZBRA', 'ZION', 'ZTS'
    ]
    return sp500_tickers
