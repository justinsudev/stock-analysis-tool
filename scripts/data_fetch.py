import yfinance as yf
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def fetch_stock_data(ticker, start_date, end_date):
    """
    Fetch historical stock data for a given ticker and date range.
    """
    if not ticker or not isinstance(ticker, str):
        raise ValueError("Ticker must be a non-empty string")
    
    if not start_date or not end_date:
        raise ValueError("Start date and end date must be provided")
    
    try:
        stock = yf.Ticker(ticker.upper())
        data = stock.history(start=start_date, end=end_date)
        
        if data.empty:
            raise ValueError(f"No data found for {ticker}. Check the ticker or date range.")
        
        # Validate that we have the required columns
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        return data
        
    except Exception as e:
        if "No data found" in str(e):
            raise
        else:
            raise ValueError(f"Error fetching data for {ticker}: {str(e)}")

def fetch_multiple_stocks(tickers, start_date, end_date, max_workers=10):
    """
    Fetch data for multiple stocks efficiently using parallel processing.
    Returns a dictionary with ticker as key and DataFrame as value.
    """
    if not tickers:
        raise ValueError("Tickers list cannot be empty")
    
    if not start_date or not end_date:
        raise ValueError("Start date and end date must be provided")
    
    # Validate and clean tickers
    clean_tickers = []
    for ticker in tickers:
        if ticker and isinstance(ticker, str):
            clean_tickers.append(ticker.upper().strip())
    
    if not clean_tickers:
        raise ValueError("No valid tickers provided")
    
    results = {}
    failed_tickers = []
    
    def fetch_single_stock(ticker):
        try:
            data = fetch_stock_data(ticker, start_date, end_date)
            return ticker, data
        except Exception as e:
            print(f"Failed to fetch {ticker}: {str(e)}")
            return ticker, None
    
    print(f"Fetching data for {len(clean_tickers)} stocks...")
    start_time = time.time()
    
    # Limit max_workers to reasonable number
    max_workers = min(max_workers, len(clean_tickers), 20)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ticker = {executor.submit(fetch_single_stock, ticker): ticker for ticker in clean_tickers}
        
        for future in as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                ticker, data = future.result()
                if data is not None:
                    results[ticker] = data
                else:
                    failed_tickers.append(ticker)
            except Exception as e:
                print(f"Exception for {ticker}: {str(e)}")
                failed_tickers.append(ticker)
    
    elapsed_time = time.time() - start_time
    print(f"Completed in {elapsed_time:.2f} seconds")
    print(f"Successfully fetched: {len(results)} stocks")
    print(f"Failed: {len(failed_tickers)} stocks")
    
    if failed_tickers:
        print(f"Failed tickers: {', '.join(failed_tickers[:10])}{'...' if len(failed_tickers) > 10 else ''}")
    
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
        'ORLY', 'IDXX', 'BLL', 'ADSK', 'WBA', 'ILMN', 'A', 'BKNG', 'CDW',
        'CHTR', 'CMI', 'COO', 'CPRT', 'CTSH', 'DAL', 'DOV', 'EA', 'EBAY', 'EFX',
        'ES', 'ETSY', 'EXC', 'EXPD', 'FAST', 'FDX', 'FIS', 'FLT', 'FTNT',
        'GD', 'GPN', 'GRMN', 'HAS', 'HCA', 'HES', 'HIG', 'HLT', 'HOLX', 'HPQ',
        'HSIC', 'HWM', 'IBM', 'INCY', 'INFO', 'IP', 'IPG', 'IQV', 'IR',
        'JBHT', 'JKHY', 'JNPR', 'KEY', 'KHC', 'KIM', 'KMB', 'KMI', 'KMX',
        'KR', 'L', 'LH', 'LKQ', 'LMT', 'LNT', 'LRCX', 'LUMN',
        'LUV', 'LW', 'LYB', 'LYV', 'MAA', 'MAR', 'MAS', 'MCK',
        'MET', 'MGM', 'MHK', 'MKC', 'MLM', 'MMM', 'MNST', 'MO', 'MOS',
        'MPC', 'MRNA', 'MTB', 'MTCH', 'MTD', 'MU', 'NCLH',
        'NDAQ', 'NDSN', 'NI', 'NOV', 'NRG', 'NTAP',
        'NTRS', 'NUE', 'NVR', 'NWL', 'NWS', 'NWSA', 'NXPI', 'O', 'ODFL',
        'OKE', 'OMC', 'ORCL', 'OTIS', 'OXY', 'PAYC', 'PCAR', 'PCG',
        'PEAK', 'PEG', 'PFG', 'PH', 'PHM', 'PKG',
        'PNC', 'PNR', 'POOL', 'PPG', 'PPL', 'PRU', 'PSX',
        'PTC', 'PVH', 'PWR', 'PXD', 'QRVO', 'RCL', 'RE', 'REG',
        'RF', 'RHI', 'RJF', 'RL', 'RMD', 'ROK', 'ROL', 'ROP', 'RSG',
        'SBAC', 'SBNY', 'SBUX', 'SEDG', 'SEE', 'SIVB', 'SJM',
        'SNA', 'SNPS', 'SPG', 'STE', 'STT', 'STX', 'STZ',
        'SWK', 'SWKS', 'SYF', 'SYK', 'SYY', 'TAP', 'TDG', 'TDY', 'TECH',
        'TEL', 'TER', 'TFC', 'TFX', 'TMUS', 'TPR', 'TRMB', 'TROW',
        'TSCO', 'TSN', 'TT', 'TTC', 'TTWO', 'TXT', 'TYL',
        'UAL', 'UDR', 'UHS', 'ULTA', 'URI', 'VFC', 'VIAC', 'VLO', 'VMC', 'VNO', 'VNT', 'VRSK', 'VRSN', 'VTR',
        'VTRS', 'WAB', 'WAT', 'WDC', 'WEC', 'WELL', 'WFC', 'WHR',
        'WM', 'WMB', 'WMT', 'WRB', 'WRK', 'WST', 'WTW', 'WY', 'WYNN', 'XEL',
        'XLNX', 'XOM', 'XRAY', 'XYL', 'YUM', 'ZBRA', 'ZION'
    ]
    return sp500_tickers
