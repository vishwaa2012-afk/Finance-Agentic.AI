from langchain_core.tools import tool
from duckduckgo_search import DDGS
import yfinance as yf

from rag import retrieve_documents

@tool
def retrieve_financial_document(query: str) -> str:
    """Retrieve relevant passages from the user's uploaded financial documents,
    such as an annual report or mutual fund factsheet.

    Use this for historical or reported financial metrics, risk factors,
    fund holdings, expense ratios, strategy, and management commentary.

    Units depend on the source document and are usually stated in the text,
    for example INR crore, USD million, or percent. Always preserve the exact
    unit and reporting period found in the passage.
    """
    try:
        docs = retrieve_documents(query, k=4)

        if not docs:
            return "NO_DOCUMENT_MATCH: The uploaded documents do not contain relevant information."

        parts = []
        for i, doc in enumerate(docs, 1):
            parts.append(
                f"[DOCUMENT {i}] source={doc.metadata.get('source_file')} "
                f"page={doc.metadata.get('page')}\n{doc.page_content}"
            )

        return "\n\n".join(parts)

    except Exception as e:
        return f"DOCUMENT_RETRIEVAL_ERROR: {str(e)}"


@tool
def get_stock_snapshot(ticker: str) -> str:
    """Get a live stock snapshot for a publicly traded ticker.

    Args:
        ticker: Yahoo Finance ticker symbol. Examples: RELIANCE.NS for Reliance
            Industries on NSE, TCS.NS for Tata Consultancy Services on NSE,
            AAPL for Apple on NASDAQ.

    Returns:
        Current/last traded price, currency, previous close, day change,
        percent change, market cap, and 1-month performance.

    Currency is returned explicitly. Indian NSE tickers are typically in INR;
    US tickers are typically in USD.
    """
    try:
        ticker = ticker.strip().upper()
        stock = yf.Ticker(ticker)

        fast = stock.fast_info
        price = fast.get("last_price") or fast.get("lastPrice")
        previous_close = fast.get("previous_close") or fast.get("previousClose")
        market_cap = fast.get("market_cap") or fast.get("marketCap")
        currency = fast.get("currency") or "UNKNOWN"

        if price is None:
            return f"NO_LIVE_DATA: Could not retrieve a current price for {ticker}. Verify the ticker symbol."

        change = None
        change_percent = None

        if previous_close:
            change = price - previous_close
            change_percent = (change / previous_close) * 100

        history = stock.history(period="1mo")
        month_performance = None

        if not history.empty and len(history) > 1:
            first_close = history["Close"].iloc[0]
            month_performance = ((price - first_close) / first_close) * 100

        return (
            f"LIVE_MARKET_DATA for {ticker}\n"
            f"Last price: {price:.2f} {currency}\n"
            f"Previous close: {previous_close:.2f} {currency}\n"
            f"Day change: {change:.2f} {currency} ({change_percent:.2f}%)\n"
            f"Market cap: {market_cap} {currency}\n"
            f"1-month price change: {month_performance:.2f}%\n"
            f"Source: Yahoo Finance via yfinance; data may be delayed."
        )

    except Exception as e:
        return f"LIVE_DATA_ERROR: Could not fetch data for {ticker}. Reason: {str(e)}"


@tool
def get_recent_market_news(query: str) -> str:
    """Search the public web for recent market news about a company, sector,
    fund, or financial event.

    Use this only when the user asks about recent events, market sentiment,
    announcements, or news that would not be in a static annual report.

    Returns headlines, snippets, and URLs. Treat results as unverified web
    information, not official filings.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))

        if not results:
            return "NO_NEWS_FOUND: No recent web results were found."

        lines = ["RECENT_WEB_NEWS (unverified, live web source):"]
        for i, item in enumerate(results, 1):
            lines.append(
                f"{i}. {item.get('title')}\n"
                f"Snippet: {item.get('body')}\n"
                f"URL: {item.get('href')}"
            )

        return "\n\n".join(lines)

    except Exception as e:
        return f"NEWS_TOOL_ERROR: {str(e)}"