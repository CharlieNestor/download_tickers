# US Stock Ticker Analysis

Have you ever needed to test a trading system or perform technical analysis, but didn't know which data to fetch? With the US market being the most capitalized and liquid in the world, it's a logical approach to focus on US stocks. However, identifying the right stocks and their tickers can be daunting. \ 
While we are familiar with popular tickers like 'GOOG', 'AAPL', and 'NVDA', finding others isn't straightforward. This project was created to bridge that gap by providing a simple way to retrieve comprehensive lists of US stock tickers. \
This program accesses the Nasdaq website to scrape the necessary information and obtain all the tickers for AMEX, NYSE, NASDAQ exchanges. \
It provides the functionalities to filter the data by various criteria and download it in a CSV file. It also adds a Streamlit integration, ensuring user-friendly access and usage of the program, making data retrieval and analysis seamless.


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

