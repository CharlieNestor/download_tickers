# US Stock Ticker Analysis

Have you ever needed to test a trading system or perform technical analysis, but didn't know which data to use? With the US market being the most capitalized and liquid in the world, it's a logical approach to focus on US stocks. However, identifying the right stocks and their tickers can be daunting. \
This project was created to bridge that gap by providing a simple way to retrieve comprehensive lists of US stock tickers. \
The program accesses the Nasdaq website to scrape the necessary information and obtain all the tickers for AMEX, NYSE, NASDAQ exchanges. \
It provides functionalities to clean, filter the data by various criteria and download the ticker list in a .txt or .csv file. \
It also includes a Streamlit integration, ensuring user-friendly access and usage of the program, making data retrieval and analysis seamless.

## Why This Project?
While we are familiar with popular tickers like 'GOOG', 'AAPL', and 'NVDA', finding others isn't straightforward. This project simplifies the process of identifying and retrieving tickers for US stocks, which can then be used for various trading and analysis purposes.


## Features
- Fetch stock data from NYSE, NASDAQ, and AMEX exchanges.
- Clean the dataset to keep only liquid and relevant companies.
- Filter stocks by exchange, sector, and market capitalization.
- View the top N stocks by market capitalization.
- Save the filtered list of tickers as a .txt or .csv file.
- Interactive Streamlit interface for filtering and visualizing data.

## Usage

### Example Usage in Jupyter Notebook

The Jupyter notebook file (tickers_jupyter.ipynb) provides examples on how to use the Tickers class to fetch, filter, and save ticker data. This is particularly useful for understanding the capabilities of the methods and for performing exploratory analysis.

### Running the Streamlit App
To start the Streamlit app, run the following command in the Terminal:
```sh
streamlit run ticker_streamlit.py
```

## File Structure

*tickers.py*: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contains the main classes and methods for fetching, cleaning, filtering, and saving ticker data. \
*tickers_jupyter.ipynb*: &nbsp; Jupyter notebook demonstrating how to use the methods provided in tickers.py. Useful for understanding the workflow and performing custom analyses. \
*tickers_streamlit.py*: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Implements the Streamlit app, providing an interactive interface for users to filter and visualize stock data.

