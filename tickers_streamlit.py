import numpy as np
import pandas as pd
import streamlit as st
import tickers as tick


def generate_mktcap_values(max_value):
    """
    input: max value of market cap in the dataset (in USD Millions)
    output: list of 10 values int/float representing a scale between min value (=0) and max value (=max_value)
    the scale between 0 and max_value is in log scale because there are few companies with huge capitalization and
    the majority instead has "normal" values. hence the log.
    """
    # round the max value to the next 100k (which means 100 billions)
    max_value_rounded = np.ceil(max_value / 100_000) * 100_000
    log_values = np.logspace(0, np.log10(max_value_rounded), num=10)
    values = list(np.concatenate(([0], log_values[1:])))
    # just different roundings depending on the values
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

if 'ticker_data' not in st.session_state:
    # st.session_state is a dictionary-like object that allows to store
    # and persist across re-runs. 
    # every time that and update (button, slider) happens, streamlit re runs the whole file.
    # ticker data is the instance that will keep the updates across the runs
    st.session_state.ticker_data = tick.Tickers()

if 'original_data' not in st.session_state:
    # original data is the instance that is permanent across runs but will never be updated
    st.session_state.original_data = tick.Tickers()

ticker_data = st.session_state.ticker_data
original_data = st.session_state.original_data

mapping = {i+1:item for i, item in enumerate(generate_mktcap_values(original_data.max_cap)) }


st.title("US Listed Stock Tickers")
st.write('###')         # defines the spacing: more #, less space inbetween

# Show the original dataset
st.dataframe(original_data.data)
st.write(f'There are {len(original_data.data)} stocks in the original dataset.')

# Sidebar title
st.sidebar.header('Filter the Dataset')
st.sidebar.write('####')

# Exchange Widget in sidebar
exchanges = ("AMEX", "NASDAQ", "NYSE")
st.sidebar.subheader('Exchanges')
selected_exch = st.sidebar.multiselect('Select one or more Exchanges', exchanges)

# Sector Widget in sidebar
sectors = ('Basic Materials', 'Consumer Discretionary', 'Consumer Staples', 'Energy', 'Finance',
            'Health Care', 'Industrials', 'Miscellaneous', 'Real Estate', 'Technology', 
            'Telecommunications', 'Utilities')
st.sidebar.subheader('Sectors')
selected_sectors = st.sidebar.multiselect('Select one or more sectors', sectors)

# Market Capitalization Slider in sidebar
st.sidebar.subheader('Market Capitalization')
mktcap_range = st.sidebar.slider('Qualitative increasing scale', min_value=1, max_value=10, value=(1,10))

# Apply Filters button in sidebar
st.sidebar.subheader('Apply the filters to the dataset')
result_apply = st.sidebar.button('Apply')
if result_apply:
    ticker_data.apply_filters(exchange=selected_exch, sectors=selected_sectors, 
                              mktcap_min=mapping[mktcap_range[0]], mktcap_max=mapping[mktcap_range[1]])
    if mktcap_range is not None:
        st.subheader('Result of filters')
        st.write(f'The new dataset contains {len(ticker_data.data)} stocks after the filtering.')
        st.write(f'The lowest value of capitalization of the selected range is USD {mapping[mktcap_range[0]]} millions; \
                 the highest value of capitalization of the selected range is USD {mapping[mktcap_range[1]]} millions.')
    st.write(ticker_data.tickers_list)

# User input for top n stock
st.sidebar.subheader('Filter the top stocks in terms of Market Cap')
top_stocks = st.sidebar.number_input(label='number of stocks', min_value=1, max_value=1000, value=None)
top_button = st.sidebar.button('Select Top Stocks')
if top_button:
    if top_stocks:
        ticker_data.get_biggest_n_tickers(top_stocks)

# Download button 
st.sidebar.subheader('Download the Ticker List')
result_down = st.sidebar.button('Download')
if result_down:
    ticker_data.save_tickers()
    st.write(f'{len(ticker_data.data)} tickers have been downloaded.')
    st.write(ticker_data.tickers_list)

# Checkbox to show the filtered dataset
st.write('######')
filtered_check = st.checkbox('Show the filtered dataset')
if filtered_check:
    st.write(ticker_data.data)
    st.write(f'There are {len(ticker_data.data)} stocks in the filtered dataset.')

