import streamlit as st
import tickers as tk


def main():

    if 'ticker_data' not in st.session_state:
        # st.session_state is a dictionary-like object that allows to store
        # and persist across re-runs. 
        # every time that and update (button, slider) happens, streamlit re runs the whole file.
        # ticker data is the instance that will keep the updates across the runs
        st.session_state.ticker_data = tk.Tickers()

    if 'original_data' not in st.session_state:
        # original data is the instance that is permanent across runs but will never be updated
        st.session_state.original_data = tk.Tickers()

    # initialize session state for selections and slider if they don't exist
    if 'selected_exch' not in st.session_state:
        st.session_state.selected_exch = []
    if 'selected_sectors' not in st.session_state:
        st.session_state.selected_sectors = []
    if 'mktcap_range' not in st.session_state:
        st.session_state.mktcap_range = (1, 10)  # Default range

    # Reset function
    def reset_selections():
        st.session_state.selected_exch = []
        st.session_state.selected_sectors = []
        st.session_state.mktcap_range = (1, 10)  # Reset to default range


    ticker_data = st.session_state.ticker_data
    original_data = st.session_state.original_data

    mapping = {i+1:item for i, item in enumerate(tk.generate_mktcap_values(original_data.max_cap)) }


    st.title("US Listed Stock Tickers")
    st.write('###')         # defines the spacing: more #, less space inbetween

    # Show the original dataset
    st.dataframe(original_data.data)
    st.write(f'There are {len(original_data.data)} stocks in the original dataset.')

    # Sidebar title
    st.sidebar.header('Filter the Dataset')
    st.sidebar.write('####')

    # Exchange Widget in sidebar
    exchanges = ["AMEX", "NASDAQ", "NYSE"]
    st.sidebar.subheader('Exchanges')
    selected_exch = st.sidebar.multiselect('Select one or more Exchanges', exchanges, key='selected_exch')

    # Sector Widget in sidebar
    sectors = ['Basic Materials', 'Consumer Discretionary', 'Consumer Staples', 'Energy', 'Finance',
                'Health Care', 'Industrials', 'Miscellaneous', 'Real Estate', 'Technology', 
                'Telecommunications', 'Utilities']
    st.sidebar.subheader('Sectors')
    selected_sectors = st.sidebar.multiselect('Select one or more sectors', sectors, key='selected_sectors')

    # Market Capitalization Slider in sidebar
    st.sidebar.subheader('Market Capitalization')
    #mktcap_range = st.sidebar.slider('Qualitative increasing scale', min_value=1, max_value=10, value=(1,10))
    mktcap_range = st.sidebar.slider('Qualitative increasing scale', min_value=1, max_value=10, key='mktcap_range')

    # Reset button
    st.sidebar.button('Reset Selections', on_click=reset_selections)

    # Apply Filters button in sidebar
    st.sidebar.subheader('Apply the filters')
    result_apply = st.sidebar.button('Apply')
    if result_apply:
        ticker_data.apply_filters(
                    exchange=selected_exch or None, 
                    sectors=selected_sectors or None, 
                    mktcap_min=mapping[mktcap_range[0]], 
                    mktcap_max=mapping[mktcap_range[1]])

        st.subheader('Result of filters')
        st.write(f'The new dataset contains {len(ticker_data.data)} stocks after the filtering.')
        st.write(f'The lowest value of capitalization of the selected range is USD {mapping[mktcap_range[0]]} millions; \
                the highest value of capitalization of the selected range is USD {mapping[mktcap_range[1]]} millions.')
        st.write(ticker_data.tickers_list)

    # User input for top n stock
    st.sidebar.subheader('Top k stocks in terms of Market Cap')
    top_stocks = st.sidebar.number_input(label='number of stocks', min_value=1, max_value=1000, value=None)
    top_button = st.sidebar.button('Select Top Stocks')
    if top_button:
        if top_stocks:
            ticker_data.get_biggest_n_tickers(top_stocks)

    # Download button 
    st.sidebar.subheader('Download the Ticker List')
    result_down = st.sidebar.button('Download')
    if result_down:
        ticker_data.save_tickers(csvformat=False)
        st.write(f'{len(ticker_data.data)} tickers have been downloaded.')
        st.write(ticker_data.tickers_list)

    # Checkbox to show the filtered dataset
    st.write('######')
    filtered_check = st.checkbox('Show the filtered dataset')
    if filtered_check:
        st.write(ticker_data.data)
        st.write(f'There are {len(ticker_data.data)} stocks in the filtered dataset.')


if __name__ == '__main__':

    main()

