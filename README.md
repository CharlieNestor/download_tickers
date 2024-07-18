# US Stock Ticker Analysis

Unlock the power of US stock market data with ease. This project provides a streamlined solution for retrieving comprehensive lists of US stock tickers, essential for testing trading systems and performing technical analysis. By focusing on the world's most capitalized and liquid market, this tool is suitable for investors, analysts, and researchers.

## Why This Project?
While tickers like 'GOOG', 'AAPL', and 'NVDA' are household names, accessing a broader range of stock symbols can be challenging. Our project simplifies this process, making it effortless to identify and retrieve tickers for US stocks across major exchanges.

## Key Features
- Data retrieval from NYSE, NASDAQ, and AMEX exchanges
- Intelligent data cleaning for liquid and relevant companies
- Advanced filtering by exchange, sector, and market capitalization
- Top N stocks ranking by market cap
- Export functionality: Save filtered lists as .txt or .csv files
- User-friendly Streamlit interface for interactive data exploration

## How It Works
Our program leverages web scraping techniques to extract up-to-date stock information directly from the Nasdaq website. This ensures you always have access to the most current data for your analysis needs.

## Usage

### Jupyter Notebook
Explore `tickers_jupyter.ipynb` for in-depth examples of using the Tickers class. This notebook is ideal for understanding method capabilities and conducting exploratory analysis.

### Streamlit App
Experience our interactive interface by running in the Terminal:
```sh
streamlit run ticker_streamlit.py
```

## Project Structure
- `tickers.py`: Core functionality for data operations
- `tickers_jupyter.ipynb`: Tutorial and exploration notebook
- `tickers_streamlit.py`: Interactive Streamlit application

