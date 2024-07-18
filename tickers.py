import os
import csv
import requests
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union

_EXCHANGE_LIST = {'NYSE', 'NASDAQ', 'AMEX'}

_SECTORS_LIST = {'Basic Materials', 'Consumer Discretionary',
                'Consumer Staples', 'Energy', 'Finance',
                'Health Care', 'Industrials', 'Miscellaneous', 
                'Real Estate', 'Technology', 'Telecommunications',
                'Utilities'
                }

# these headers are necessary to make the request to the API and not get blocked
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


def fetch_exchange_data(exchange: str) -> pd.DataFrame:
    """
    send customized request to the url and return the dataset via pd.DataFrame
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


def get_combined_df(NYSE:bool = True, NASDAQ:bool = True, AMEX:bool = True) -> pd.DataFrame:
    """
    download one dataset from each exchange and return the combined dataset
    : param NYSE: bool, whether to include NYSE stocks
    : param NASDAQ: bool, whether to include NASDAQ stocks
    : param AMEX: bool, whether to include AMEX stocks
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
    new_order = ['symbol', 'name', 'exchange', 'marketCap', 'sector', 'industry', 'lastsale','volume', 'ipoyear','country','url']
    result_df = result_df[new_order]
    return result_df.sort_values(by='symbol').reset_index(drop=True)


def getDownloadPath() -> str:
    """
    retrieve the path of Downloads folder in your system
    """
    # determine the home directory
    home = str(Path.home())

    # path to the Downloads folder
    if os.name == 'nt':  # For Windows
        downloads_path = os.path.join(home, 'Downloads')
    else:  # for macOS and Linux
        downloads_path = os.path.join(home, 'Downloads')
    return downloads_path


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    filter the DataFrame step by step according to the specified criteria.
    : param df: pd.DataFrame, the original dataset
    """
    # eliminate tickers with no value for marketCap or volume
    # needs this step before converting to int
    df = df[(df['marketCap'] != '') & (df['volume'] != '')]
    
    # change marketCap and volume to int values
    df.loc[:, 'marketCap'] = df['marketCap'].astype(float).astype(int)
    df.loc[:, 'volume'] = df['volume'].astype(int)
    
    # eliminate tickers with name containing '%'
    df = df[~df['name'].str.contains('%')]
    
    # eliminate tickers with name containing 'Warrant'
    df = df[~df['name'].str.contains('Warrant')]
    
    # eliminate tickers with name containing 'Rate'
    df = df[~df['name'].str.contains('Rate')]
    
    # eliminate tickers with name containing only 'Fund'
    df = df[~df['name'].str.contains('Fund ')]
    
    # eliminate tickers with name containing only 'Bond'
    df = df[~df['name'].str.contains('Bond ')]
    
    # eliminate tickers with less than 10k volumes and whose marketCap is 0
    df = df[~((df['volume'] < 10000) & (df['marketCap'] == 0))]
    
    # eliminate tickers with less than 10k volumes and in its name contains 'Trust'
    df = df[~((df['volume'] < 10000) & (df['name'].str.contains('Trust')))]
    
    # eliminate tickers with less than 1Mio marketCap and in its name contains 'Fund'
    df = df[~((df['marketCap'] < 1000000) & (df['name'].str.contains('Fund')))]
    
    return df


def generate_mktcap_values(max_value: float) -> list:
    """
    generates a list of 10 values in log scale between 0 and max_value
    : param max_value: float, max value of market cap in the dataset (in USD Millions)
    : return: list of 10 values int/float representing a scale between min value (=0) and max value (=max_value)
    the scale between 0 and max_value is in log scale because there are few companies with huge capitalization and
    the majority instead has "normal" values. hence the log.
    """
    # round the max value to the next 100k (which means 100 billions)
    max_value_rounded = np.ceil(max_value / 100_000) * 100_000
    log_values = np.logspace(0, np.log10(max_value_rounded), num=10)
    values = list(np.concatenate(([0], log_values[1:])))
    # round the values to the nearest 100, 1000, 10000, 100000
    for i in range(len(values)):
        if values[i]<1000:
            values[i] = float(np.round(values[i],1))
        elif values[i]<10_000:
            values[i] = int(np.floor(values[i]/100)*100)
        elif values[i]<100_000:
            values[i] = int(np.floor(values[i]/1000)*1000)
        elif values[i]<1_000_000:
            values[i] = int(np.floor(values[i]/10000)*10000)
        else:
            values[i] = int(np.ceil(values[i]/100_000)*100_000)
    return values


class Tickers():
    """
    Class that handles the ticker dataset.
    Download and store the dataset in 2 DataFrames: 
    - original_dataset for a clean copy
    - data for a modifiable copy
    The updated version of ticker list is stored in ticker_list; apply different methods to filter the dataset and 
    download the ticker_list as .csv file in Downloads folder.
    """

    def __init__(self):
        self.original_dataset = clean_dataset(get_combined_df())    # download the dataset and clean it
        self.data = self.original_dataset.copy()                    # copy the original dataset to the modifiable one
        self.max_cap = self.calculate_max()
        self.tickers_list = self.get_tickers()
        

    def reset_data(self) -> None:
        self.data = self.original_dataset.copy()

    def get_tickers(self) -> list:
        return self.data['symbol'].to_list()
    
    def update_tickers(self) -> None:
        # generally, first modify self.data, then update the ticker list
        self.tickers_list = self.get_tickers()

    def calculate_max(self) -> float:
        """
        returns the highest market capitalization (in USD Millions) of the stocks in the dataset
        : return: float, the highest market capitalization in the dataset
        """
        # convert the marketCap field to float number and to USD Millions
        self.original_dataset.loc[:,'marketCap'] = np.round(self.original_dataset.loc[:,'marketCap'].astype(float) / 1000000,2)
        return self.original_dataset['marketCap'].max()


    def get_biggest_n_tickers(self, top_n:int) -> None:
        """
        filter the self.data to obtain only the top_n stocks by market capitalization
        : param top_n: int, number of top stocks to keep
        """
        if top_n>=len(self.data):
            self.data = self.data.sort_values('marketCap', ascending=False)
        else:
            self.data = self.data.sort_values('marketCap', ascending=False).iloc[:top_n,:]
        self.update_tickers()
    
    
    def apply_filters(self, exchange:Union[str, list] = None, sectors:Union[str, list] = None, mktcap_min=None, mktcap_max=None) -> None:
        """
        apply filters to self.data. the dataset is modified inplace
        : param exchange: str or list of str, exchanges to filter by
        : param sectors: str or list of str, sectors to filter by
        : param mktcap_min: int/float, minimum market capitalization to filter by
        : param mktcap_max: int/float, maximum market capitalization to filter by
        """
        # there might be a conflict if self.data is already filtered 
        # the solution here is simply to reset the previous filters and apply directly the new filters
        # this can be changed and / or optimized
        self.reset_data()

        # filter by exchange
        if exchange and isinstance(exchange, (str, list)) and any(exchange):
            if isinstance(exchange, str):
                exchange = [exchange.upper()]
            else:
                exchange = [x.upper() for x in exchange]
            if not set(exchange).issubset(set(_EXCHANGE_LIST)):
                raise ValueError('Some exchange included are invalid')
            exchange = [x.lower() for x in exchange]
            self.data = self.data[self.data['exchange'].isin(exchange)]

        # filter by sectors
        if sectors and isinstance(sectors, (str, list)) and any(sectors):
            if isinstance(sectors, str):
                sectors = [sectors]
            if not set(sectors).issubset(set(_SECTORS_LIST)):
                raise ValueError('Some sectors included are invalid')
            self.data = self.data[self.data['sector'].isin(sectors)]

        # filter by market cap
        if mktcap_min is not None:
            self.data = self.data[self.data['marketCap'] >= mktcap_min]
        if mktcap_max is not None:
            self.data = self.data[self.data['marketCap'] <= mktcap_max]
        
        self.update_tickers()


    def save_tickers(self, filename:str ='tickers.txt', csvformat:bool = False) -> None:
        """
        save the ticker list as .txt or .csv file in the Downloads folder
        : param filename: str, name of the file to save
        : param csvformat: bool, whether to save the file in .csv format or not
        """
        tickers2save = self.tickers_list
        tickers2save.sort()
        # the filepath leads to the Downloads folder
        full_path = os.path.join(getDownloadPath(), filename)

        if csvformat:
            # save the tickers in a csv file
            filename = 'tickers.csv'
            full_path = os.path.join(getDownloadPath(), filename)
            with open(full_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(tickers2save)
        else:
            # save the tickers in a txt file
            with open(full_path, mode='w') as file:
                for ticker in tickers2save:
                    file.write(f"{ticker}\n")
    