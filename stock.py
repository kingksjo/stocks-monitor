import requests

# API URL for stock data
STOCKS_API_URL = "https://www.alphavantage.co/query"

def search_for_stock(keywords, api_key):
    name_response = requests.get(f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keywords}&apikey={api_key}")
    name_response.raise_for_status()
    name_data = name_response.json()
    for match in name_data["bestMatches"]:
        if match["4. region"] == "United States":
            return match["2. name"]

def fetch_stock_data(symbol, api_key):
    """
    Fetch stock price data for the given symbol.
    
    Args:
        symbol (str): Stock ticker symbol.
        api_key (str): API key for Alpha Vantage.

    Returns:
        dict: JSON response from the API.
    """
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key,
    }
    response = requests.get(STOCKS_API_URL, params=params)
    response.raise_for_status()
    return response.json()

def calculate_percentage_change(stock_data):
    """
    Calculate the percentage change between the latest two closing prices.
    
    Args:
        stock_data (dict): Stock price data from Alpha Vantage API.

    Returns:
        float: Percentage change between the two most recent closing prices.
    """
    try:
        time_series = stock_data["Time Series (Daily)"]
        dates = list(time_series.keys())
        current = float(time_series[dates[0]]["4. close"])
        previous = float(time_series[dates[1]]["4. close"])
        return ((current - previous) / previous) * 100
    except (KeyError, IndexError, ValueError):
        return None


