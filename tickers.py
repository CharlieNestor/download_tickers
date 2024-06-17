import os
import csv
import requests
import pandas as pd
import numpy as np
from pathlib import Path

_EXCHANGE_LIST = {'NYSE', 'NASDAQ', 'AMEX'}

_SECTORS_LIST = {'Basic Materials', 'Consumer Discretionary',
                'Consumer Staples', 'Energy', 'Finance',
                'Health Care', 'Industrials', 'Miscellaneous', 
                'Real Estate', 'Technology', 'Telecommunications',
                'Utilities'
                }

headers = {
    'authority': 'api.nasdaq.com',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',  # defines client making request as a browser
    'origin': 'https://www.nasdaq.com',
    'referer': 'https://www.nasdaq.com/',
    'accept-language': 'en-US,en;q=0.9',
}

def params(exchange):
    return (
        ('letter', '0'),            # it will return all tickers
        ('exchange', exchange),
        ('download', 'true'),
    )


def fetch_exchange_data(exchange):
    """
    send customized request to the url and output the dataset via pd.DataFrame
    """
    r = requests.get('https://api.nasdaq.com/api/screener/stocks', headers=headers, params=params(exchange))
    if r.status_code==200:
        data = r.json()['data']
        df = pd.DataFrame(data['rows'], columns=data['headers'])
        df.loc[:,'exchange'] = exchange
        df_filtered = df[~df['symbol'].str.contains("\.|\^")]
        return df_filtered
    else:
        print(f"Failed to fetch data: {r.status_code}")


def get_combined_df(NYSE=True, NASDAQ=True, AMEX=True):
    """
    download DataFrames from all 3 exchanges and output a single DataFrame concatenated 
    and sorted by ticker
    """
    df_list = []
    if NYSE:
        df_list.append(fetch_exchange_data('nyse'))
    if NASDAQ:
        df_list.append(fetch_exchange_data('nasdaq'))
    if AMEX:
        df_list.append(fetch_exchange_data('amex'))
    result_df = pd.concat(df_list, ignore_index=True)
    # select only specific columns from the dataset
    new_order = ['symbol', 'name', 'exchange', 'marketCap', 'sector', 'industry', 'lastsale','ipoyear','country','url']
    result_df = result_df[new_order]
    return result_df.sort_values(by='symbol').reset_index(drop=True)


def getDownloadPath():
    # Determine the home directory
    home = str(Path.home())

    # Path to the Downloads folder
    if os.name == 'nt':  # For Windows
        downloads_path = os.path.join(home, 'Downloads')
    else:  # For macOS and Linux
        downloads_path = os.path.join(home, 'Downloads')
    return downloads_path


class Tickers():
    """
    Class that handle the ticker dataset.
    Download and store the dataset in 2 DataFrames: 
    - original_dataset for a clean copy
    - data for a modifiable copy
    Keep the updated version of ticker list in ticker_list; apply different methods to filter the dataset and 
    download the ticker_list as .csv file in Download folder.
    """

    def __init__(self):
        self.original_dataset = get_combined_df()
        self.max_cap = self.calculate_max()
        self.data = self.original_dataset.copy()
        self.tickers_list = self.get_tickers()
        

    def reset_data(self):
        self.data = self.original_dataset.copy()

    def get_tickers(self):
        return self.data['symbol'].to_list()
    
    def update_tickers(self):
        # generally, first we modify self.data, then we update the ticker list
        self.tickers_list = self.get_tickers()

    def calculate_max(self):
        """
        returns the highest market capitalization (in USD Millions) of the stocks in the dataset
        """
        self.original_dataset = self.original_dataset[self.original_dataset['marketCap']!='']
        # convert to marketCap to float number and to USD Millions
        self.original_dataset.loc[:,'marketCap'] = np.round(self.original_dataset.loc[:,'marketCap'].astype(float) / 1000000,2)
        return self.original_dataset['marketCap'].astype(float).max() 


    def get_biggest_n_tickers(self, top_n):
        """
        filter the self.data to obtain only the top_n stocks by market capitalization
        """
        if top_n>=len(self.data):
            self.data = self.data.sort_values('marketCap', ascending=False)
        else:
            self.data = self.data.sort_values('marketCap', ascending=False).iloc[:top_n,:]
        self.update_tickers()
    
    
    def apply_filters(self, exchange=None, sectors = None, mktcap_min=None, mktcap_max=None):
        """
        apply filters to self.data; the dataset is modified inplace
        """
        # there might be a conflict if self.data is already filtered 
        # the solution here is simply to reset the previous filters and apply ONLY the new ones
        # this can be changed and / or optimized
        if len(self.data)!=len(self.original_dataset):
            self.reset_data()

        if exchange is not None:
            if isinstance(exchange, (str,list)):
                if isinstance(exchange,str):
                    exchange = [exchange.upper()]
                else:
                    exchange = [el.upper() for el in exchange]
                if not _EXCHANGE_LIST.issuperset(set(exchange)):
                    raise ValueError('Some exchange included are invalid')
            else: 
                raise ValueError('Exchanges should be either a string or a list')
            exchange = [x.lower() for x in exchange]
            self.data = self.data[self.data['exchange'].isin(exchange)]

        if sectors is not None:
            if isinstance(sectors, (str,list)):
                if isinstance(sectors,str):
                    sectors = [sectors]
                if not _SECTORS_LIST.issuperset(set(sectors)):
                    raise ValueError('Some sectors included are invalid')
            else:
                raise ValueError('Sectors should be either a string or a list')
            self.data = self.data[self.data['sector'].isin(sectors)]

        if (mktcap_max is not None) or (mktcap_min is not None):
            
            if mktcap_min is not None:
                self.data = self.data[self.data['marketCap'] > mktcap_min]
            if mktcap_max is not None:
                self.data = self.data[self.data['marketCap'] < mktcap_max]
        
        self.update_tickers()


    def save_tickers(self, filename='tickers.csv'):
        """
        save the ticker list as .csv file in the Download folder
        """
        tickers2save = self.tickers_list
        tickers2save.sort()
        full_path = os.path.join(getDownloadPath(), filename)
        with open(full_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            for ticker in tickers2save:
                writer.writerow([ticker])
    