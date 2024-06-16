# US Stock Ticker Analysis

This project retrieves and processes data for US-listed stocks from the NYSE, NASDAQ, and AMEX exchanges. Finding, selecting, and filtering a valid list of US stock tickers can be challenging due to the vast number of stocks and limited availability of up-to-date and searchable sources. This project simplifies that process by providing functionality to filter the data by various criteria, visualize it using Streamlit and download it in a CSV file.


## Features
- Fetch stock data from NYSE, NASDAQ, and AMEX exchanges.
- Filter stocks by exchange, sector, and market capitalization.
- View the top N stocks by market capitalization.
- Save the filtered list of tickers as a CSV file.
- Interactive Streamlit interface for filtering and visualizing data.

## Usage

### Running the Streamlit App
To start the Streamlit app, run the following command in the Terminal:
```sh
streamlit run ticker_streamlit.py

