import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

##### INPUT #####

request_url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'

## Parameters for the request
params = {
    'id' : 'bitcoin',
    'vs_currency' : 'usd',
    'days' : 365,
    'interval' : 'daily'
    }

## Request
r = requests.get(
    request_url,
    params=params,
    verify=True
    )

## Getting the status code
status_code = r.status_code


##### DATA TRANSFORMATION #####

## Checking if request was succesful, if it failed it shows an error message
if status_code == 200:
    print('Request was succesful')
    
    ## Convert response data to Pandas dataframe
    response_data = r.json()
    response_df_prices = pd.json_normalize(
        response_data,
        record_path='prices'
        )
    
    response_df_volumes = pd.json_normalize(
        response_data,
        record_path='total_volumes'
        )
    
    ## Merging both dataframes on 'date' to join the data in one dataframe
    btc_df = pd.merge(
        response_df_prices,
        response_df_volumes,
        how='inner',
        on=0
        )
    
    ## Changing columns names
    btc_df = btc_df.rename(
        columns={
            0 : 'Date',
            '1_x' : 'Price',
            '1_y' : 'Volume'
            }
        )
    
    ## Formatting date column to change the format
    btc_df['Date'] = pd.to_datetime(
        btc_df['Date'],
        unit='ms',
        origin='unix'
        )
    
    
    ##### OUTPUT #####
    
    #### Creating the figure and a pair of twin axes.
    #### Both axes will share the x axis, in which Date data will be shown.
    fig, ax1 = plt.subplots(
        figsize=(11,6)
        )
    
    ## Setting the data, label, color and line width for axes 1
    ax1.plot(
        btc_df['Date'],
        btc_df['Price'],
        label='USD',
        color='blue',
        lw=2
        )
    
    ## Making the axes twins
    ax2 = ax1.twinx()
    
    ## Setting the data, label and color for axes 2
    ax2.bar(
        btc_df['Date'],
        btc_df['Volume'],
        label='Vol',
        color='#D39507'
        )
    
    #### Customizing the chart
    
    ## Setting y limits for axes. 
    ## As it shows price of an asset, bottom limit will be 0
    ## Ax2 limit will be expanded to make volume bars look small.
    ax1.set_ylim(
        bottom=0,
        top=max(btc_df['Price']*1.11)
        )
    ax2.set_ylim(
        bottom=0,
        top=max(btc_df['Volume']*5)
        )
    
    ##Removing top and right spines
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    
    ## Removing tick marks and labels for volume
    ax2.set(yticklabels=[])
    ax2.tick_params(right=False)
    
    ## Grids will make it easier to read
    ax1.yaxis.grid(
        color='black',
        linestyle='dashed',
        alpha=0.7
        )
    ax1.xaxis.grid(
        color='black',
        linestyle='dashed',
        alpha=0.3
        )
    
    ## Formatting the x axis ticks to show months
    fmt_monthly_xticks = mdates.MonthLocator(interval=1)
    ax1.xaxis.set_major_locator(fmt_monthly_xticks)
    
    ## Rotating x axis labels
    xlabels=ax1.get_xticklabels()
    plt.setp(
        xlabels,
        rotation=45
        )
    
    ## Adding a title for each axis
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    
    ## Customizing legends
    ax1.legend(
        loc='upper right',
        fancybox=True
        )
    ax2.legend(
        loc='lower right',
        frameon=False,
        fontsize='small',
        handlelength=0,
        handletextpad=0
        )
    
    ## Adding Title, source and copyright
    ax1.set_title(
        'Bitcoin - Daily Close',
        fontsize=16
        )
    ax1.text(-0.06, -0.2,'Source: CoinGecko - Plot: JuanBernal8',
             size=10,
             transform=ax1.transAxes
             )
    
else:
    print('Error')


