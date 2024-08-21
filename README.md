# US Stock Ticker Analysis

Streamline your access to US stock market data. This tool provides an easy way to retrieve comprehensive lists of US stock tickers, ideal for testing trading systems or conducting technical analysis.

## Key Features
- Data retrieval from NYSE, NASDAQ, and AMEX exchanges
- Intelligent data cleaning for liquid and relevant companies
- Filtering by exchange, sector, and market capitalization
- Top N stocks ranking by market cap
- Export filtered lists as .txt or .csv files
- User-friendly Streamlit interface for interactive data exploration

## How It Works
The program uses web scraping to extract current stock information from the Nasdaq website, ensuring up-to-date data for your analysis.

## Usage

### Jupyter Notebook
Explore `tickers_jupyter.ipynb` for in-depth examples and analysis.

### Streamlit App
Run the interactive interface via Terminal:
```sh
streamlit run ticker_streamlit.py
```

## Project Structure
- `tickers.py`: Core functionality for data operations
- `tickers_jupyter.ipynb`: Tutorial and exploration notebook
- `tickers_streamlit.py`: Interactive Streamlit application

