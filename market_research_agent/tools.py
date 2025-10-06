import yfinance as yf
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Stock price tool

@tool
def get_stock_price(ticker: str) -> str:
    """Get the latest stock price by ticker symbol.

       Args:
           ticker: The stock ticker symbol (e.g., 'AAPL' for Apple).
       """

    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    print(f" \n \n stock price print {stock}")
    if data.empty:
        return f"Could not retrieve stock data for {ticker}"
    price = round(data["Close"].iloc[-1], 2)
    return f"The latest closing price of {ticker} is ${price}"

# Simple crypto price (via yfinance too)

@tool
def get_crypto_price(symbol: str) -> str:
    """Get the latest crypto price by ticker symbol.

       Args:
           symbol: The crypto ticker symbol (e.g., 'BTC-USD' for Bitcoin).
       """
    crypto = yf.Ticker(symbol)
    data = crypto.history(period="1d")
    if data.empty:
        return f"Could not retrieve price for {symbol}"
    price = round(data["Close"].iloc[-1], 2)
    return f"The latest closing price of {symbol} is ${price}"

# Sentiment analysis using Tavily search
search_tool = TavilySearchResults(
    max_results=3,
    tavily_api_key=TAVILY_API_KEY
)

@tool
def analyze_sentiment(query: str) -> str:
    """Analyzes the sentiment of recent news for a given stock or crypto.

    Args:
        query: The stock or crypto ticker symbol to search for news.
    """

    results = search_tool.run(query)
    text = " ".join([r["content"] for r in results if "content" in r])
    if "buy" in text.lower():
        return "Sentiment looks positive (Buy signals detected)."
    elif "sell" in text.lower():
        return "Sentiment looks negative (Sell signals detected)."
    else:
        return "Sentiment is neutral or unclear."

TOOLS = [get_stock_price, get_crypto_price,analyze_sentiment, search_tool]